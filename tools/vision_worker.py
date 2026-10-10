"""Reads jobs/*.vision.json ([{id,url}]) -> asks free Gemini to read each card photo -> results/<name>.json"""
import base64, json, os, pathlib, sys, time, urllib.request, urllib.error
KEY = os.environ["GEMINI_API_KEY"]
API = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
PROMPT = ("This is a photo of one Pokemon trading card. Read ONLY what is printed on the card. "
          "Reply with JSON only, keys: name, number (as printed, e.g. 096/088 or SVP 073), "
          "card_type (Pokémon, Trainer or Energy), stage (Basic, Stage 1, Stage 2, or empty for Trainers/VSTAR etc. as printed), "
          "hp (number only, empty for Trainers), illustrator (text after 'Illus.'), is_back (true if this is the card back). "
          "Use empty string for anything you cannot read clearly. Never guess.")
def ask(img):
    body = {"model": os.environ.get("VISION_MODEL", "gemini-flash-latest"),
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(img).decode()}}]}],
            "response_format": {"type": "json_object"}}
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(json.load(r)["choices"][0]["message"]["content"])
for f in sys.argv[1:]:
    out = []
    for job in json.loads(pathlib.Path(f).read_text()):
        res = {"id": job["id"]}
        for attempt in range(4):
            try:
                img = urllib.request.urlopen(urllib.request.Request(job["url"], headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
                res.update(ask(img)); break
            except urllib.error.HTTPError as e:
                res["error"] = f"{e.code}"; time.sleep(15 * (attempt + 1))
            except Exception as e:
                res["error"] = str(e)[:120]; time.sleep(10)
        else:
            pass
        if "name" in res: res.pop("error", None)
        out.append(res); print(res); time.sleep(5)
    dest = pathlib.Path("results") / (pathlib.Path(f).stem + ".json")
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False))
