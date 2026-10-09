"""
price_check.py - free card price lookups (no AI, no API key).

Checks eBay sold, TCGplayer market and PriceCharting for every card in cards.txt
and suggests a list price using Matt's rules. Results go to prices.csv (opens in Excel).

Setup (one time): install Python from python.org and tick "Add to PATH". No extra packages.

Use:
  1. Put one card per line in cards.txt, e.g.  Espurr 095/088 Perfect Order
  2. Double-click run_prices.bat
  3. Open prices.csv (or upload it to Claude)

Rules applied:
  - eBay sold median decides the price; TCGplayer market is the reference.
  - Floor: 95% of TCGplayer market (may dip up to $0.50 under, only to land a clean price).
  - Round up to a price ending in 9 cents (3.51 -> 3.59).
  - Shows what each price nets after eBay fees (13.25% + $0.40) and the $0.78 envelope.
"""

import csv
import html
import json
import math
import os
import re
import statistics
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
FEE_PCT, FEE_FLAT, ENVELOPE = 0.1325, 0.40, 0.78
MIN_PRICE = 1.79  # never price a card below this
EBAY_COMPS = 10  # how many recent sold listings to use


def get(url, body=None, extra=None):
    headers = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    if extra:
        headers.update(extra)
    data = json.dumps(body).encode() if body is not None else None
    if data:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def money(s):
    m = re.search(r"\$\s*([\d,]+\.\d{2})", s)
    return float(m.group(1).replace(",", "")) if m else None


def card_number(q):
    m = re.search(r"([A-Z]*\d+)\s*/\s*([A-Z]*\d+)", q, re.I)
    return m.group(1).lstrip("0").lower() if m else None


# ---------- eBay sold ----------
def ebay_sold(q):
    url = ("https://www.ebay.com/sch/i.html?" + urllib.parse.urlencode(
        {"_nkw": q, "LH_Sold": 1, "LH_Complete": 1, "_sop": 13, "_ipg": 60}))
    page = get(url)
    m = re.search(r'<ul[^>]*class="[^"]*srp-results[^"]*"[^>]*>(.*)</ul>', page, re.S)
    if not m:
        return None, 0, "no results block (eBay may have blocked the request)"
    body = m.group(1)
    num = card_number(q)
    prices = []
    for li in re.split(r"<li[\s>]", body)[1:]:
        text = html.unescape(re.sub(r"<[^>]+>", " ", li))
        low = text.lower()
        if "shop on ebay" in low or not re.search(r"sold\s+\w{3}\s+\d", low):
            continue
        if any(w in low for w in ("psa", "cgc", "bgs", "graded", " lot", "choose", "pick your")):
            continue  # raw singles only
        if num and num not in re.sub(r"\b0+(\d)", r"\1", low):
            continue
        pm = re.search(r'class="[^"]*(?:s-item__price|s-card__price)[^"]*"[^>]*>(.*?)</span>', li, re.S)
        p = money(html.unescape(pm.group(1))) if pm else money(text)
        if p and " to " not in (pm.group(1) if pm else ""):
            prices.append(p)
        if len(prices) >= EBAY_COMPS:
            break
    if not prices:
        return None, 0, "no matching raw sold listings"
    return round(statistics.median(prices), 2), len(prices), ""


# ---------- TCGplayer ----------
def tcg_market(q):
    url = ("https://mp-search-api.tcgplayer.com/v1/search/request?"
           + urllib.parse.urlencode({"q": q, "isList": "false"}))
    body = {"algorithm": "sales_synonym_v2", "from": 0, "size": 5,
            "filters": {"term": {"productLineName": ["pokemon"]}, "range": {}, "match": {}},
            "listingSearch": {"context": {"cart": {}}, "filters": {"term": {"sellerStatus": "Live", "channelId": 0},
                              "range": {"quantity": {"gte": 1}}, "exclude": {"channelExclusion": 0}}},
            "context": {"cart": {}, "shippingCountry": "US", "userProfile": {}},
            "settings": {"useFuzzySearch": True, "didYouMean": {}}, "sort": {}}
    data = json.loads(get(url, body, {"Origin": "https://www.tcgplayer.com",
                                      "Referer": "https://www.tcgplayer.com/"}))
    hits = data.get("results", [{}])[0].get("results", [])
    num = card_number(q)
    for h in hits:
        name = f'{h.get("productName", "")} {h.get("customAttributes", {}).get("number", "")}'.lower()
        if num and num not in re.sub(r"\b0+(\d)", r"\1", name):
            continue
        if h.get("marketPrice"):
            return float(h["marketPrice"]), f'{h.get("productName")} ({h.get("setName")})'
    return None, "no match"


# ---------- PriceCharting ----------
def pricecharting(q):
    url = "https://www.pricecharting.com/search-products?" + urllib.parse.urlencode({"q": q, "type": "prices"})
    page = get(url)
    m = re.search(r'id="used_price".*?class="price[^"]*"[^>]*>\s*([^<]+)<', page, re.S)
    if m:
        return money(m.group(1))
    # landed on a results list: take the first row's loose price
    m = re.search(r'<td class="price numeric used_price">\s*<span class="js-price">([^<]+)<', page)
    return money(m.group(1)) if m else None


# ---------- pricing rules ----------
def end_in_9(p):
    cents = math.ceil(round(p * 100, 4))
    while cents % 10 != 9:
        cents += 1
    return cents / 100


def suggest(ebay, tcg):
    if tcg is None and ebay is None:
        return None, "no data"
    if tcg is None:
        return max(end_in_9(ebay), MIN_PRICE), "eBay only - check TCG by hand"
    floor = 0.95 * tcg
    base = max(ebay if ebay is not None else tcg, floor)
    price = end_in_9(base)
    # allowed dip: up to $0.50 under the floor, only to land a cleaner price (.99 / .49)
    for clean in (math.floor(base) - 0.01, math.floor(base) + 0.49):
        if floor - 0.50 <= clean < price and clean > 0 and str(f"{clean:.2f}").endswith("9"):
            price = clean
            break
    note = []
    if price < MIN_PRICE:
        price = MIN_PRICE
        note.append("raised to $1.79 minimum")
    if ebay is None:
        note.append("no eBay comps - priced off TCG")
    return round(price, 2), "; ".join(note)


def main():
    src = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "cards.txt")
    with open(src, encoding="utf-8") as f:
        cards = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    rows = []
    for i, q in enumerate(cards, 1):
        print(f"[{i}/{len(cards)}] {q}")
        row = {"card": q}
        for key, fn in (("ebay", ebay_sold), ("tcg", tcg_market), ("pc", pricecharting)):
            try:
                row[key] = fn(q)
            except Exception as e:
                row[key] = None
                row[key + "_err"] = str(e)[:80]
            time.sleep(1.5)  # be polite, avoid blocks
        ebay, n, ebay_note = row["ebay"] if row["ebay"] else (None, 0, row.get("ebay_err", ""))
        tcg, tcg_match = row["tcg"] if row["tcg"] else (None, row.get("tcg_err", ""))
        price, note = suggest(ebay, tcg)
        rows.append({
            "Card": q, "eBay sold median": ebay, "eBay comps": n,
            "TCG market": tcg, "TCG match": tcg_match, "PriceCharting": row["pc"],
            "95% floor": round(0.95 * tcg, 2) if tcg else None,
            "Suggested price": price,
            "Net after fees": round(price * (1 - FEE_PCT) - FEE_FLAT - (ENVELOPE if price < 20 else 0), 2) if price else None,
            "Notes": "; ".join(x for x in (note, ebay_note, row.get("pc_err", "")) if x),
        })
    out = os.path.join(HERE, "prices.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
