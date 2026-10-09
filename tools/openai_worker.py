"""Runs job files in jobs/ through OpenAI's cheapest model; writes answers to results/.
Job file format: optional first block 'SYSTEM: ...', jobs separated by a line '---'."""
import json, os, pathlib, sys, time, urllib.request, urllib.error
KEY = os.environ["OPENAI_API_KEY"]
API = "https://api.openai.com/v1"
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
    ids = [x["id"] for x in call("/models")["data"]]
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
        blocks = [b.strip() for b in p.read_text().replace("\r\n", "\n").split("\n---\n") if b.strip()]
        system = blocks.pop(0)[7:].strip() if blocks and blocks[0].upper().startswith("SYSTEM:") else ""
        out = []
        for n, job in enumerate(blocks, 1):
            msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": job}]
            ans = "ERROR"
            for a in range(3):
                try:
                    ans = call("/chat/completions", {"model": model, "messages": msgs})["choices"][0]["message"]["content"].strip()
                    break
                except urllib.error.HTTPError as e:
                    ans = f"ERROR {e.code}: {e.read().decode()[:200]}"
                    time.sleep(5 * (a + 1))
            out.append(f"### JOB {n}\n{ans}")
        dest = pathlib.Path("results") / p.name
        dest.write_text(f"MODEL: {model}\n\n" + "\n\n".join(out) + "\n")
        print("wrote", dest)
if __name__ == "__main__":
    main(sys.argv[1:])
