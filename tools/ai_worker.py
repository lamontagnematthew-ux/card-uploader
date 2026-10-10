"""Runs job files in jobs/ through OpenAI's cheapest model; writes answers to results/.
Job file format: optional first block 'SYSTEM: ...', jobs separated by a line '---'."""
import base64, json, os, pathlib, sys, time, urllib.request, urllib.error
# Uses free Google Gemini if GEMINI_API_KEY is set, otherwise OpenAI.
GEM = os.environ.get("GEMINI_API_KEY", "").strip()
KEY = GEM or os.environ.get("OPENAI_API_KEY", "").strip()
API = "https://generativelanguage.googleapis.com/v1beta/openai" if GEM else "https://api.openai.com/v1"
def call(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
        method="POST" if body else "GET")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)
def pick_model():
    m = os.environ.get("OPENAI_MODEL", "").strip()
    if m:
        return m
    ids = [x["id"].replace("models/", "") for x in call("/models")["data"]]
    if GEM:
        flash = sorted(i for i in ids if "flash" in i and not any(b in i for b in ("image", "tts", "audio", "live", "exp", "preview")))
        lite = [i for i in flash if "lite" in i]
        return (lite or flash or ids)[-1]
    bad = ("audio", "realtime", "tts", "transcribe", "image", "search", "embedding", "moderation")
    chat = [i for i in ids if i.startswith("gpt") and not any(b in i for b in bad)]
    for tier in ("nano", "mini"):
        hits = sorted(i for i in chat if tier in i)
        if hits:
            return hits[-1]
    return sorted(chat)[-1]
def main(files):
    model = pick_model()
    for f in files:
        p = pathlib.Path(f)
        raw = p.read_text()
        fmodel = model
        if raw.startswith("MODEL:"):
            first, raw = raw.split("\n", 1)
            fmodel = first[6:].strip() or model
        blocks = [b.strip() for b in raw.replace("\r\n", "\n").split("\n---\n") if b.strip()]
        system = blocks.pop(0)[7:].strip() if blocks and blocks[0].upper().startswith("SYSTEM:") else ""
        out = []
        for n, job in enumerate(blocks, 1):
            imgs = [l[6:].strip() for l in job.splitlines() if l.startswith("IMAGE:")]
            text = "\n".join(l for l in job.splitlines() if not l.startswith("IMAGE:"))
            content = text
            if imgs:
                content = [{"type": "text", "text": text}]
                for u in imgs:
                    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
                    data = base64.b64encode(urllib.request.urlopen(req, timeout=60).read()).decode()
                    content.append({"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + data}})
            msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": content}]
            ans = "ERROR"
            for a in range(5):
                try:
                    ans = call("/chat/completions", {"model": fmodel, "messages": msgs})["choices"][0]["message"]["content"].strip()
                    break
                except urllib.error.HTTPError as e:
                    ans = f"ERROR {e.code}: {e.read().decode()[:200]}"
                    time.sleep(15 * (a + 1))
            out.append(f"### JOB {n}\n{ans}")
            if imgs:
                time.sleep(7)  # stay under free-tier rate limit
        dest = pathlib.Path("results") / p.name
        dest.write_text(f"MODEL: {fmodel}\n\n" + "\n\n".join(out) + "\n")
        print("wrote", dest)
if __name__ == "__main__":
    main(sys.argv[1:])
