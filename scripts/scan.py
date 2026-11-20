"""Card scan tool for the Kodak i1150 + SVT setup (cards_by_matthew).

Usage (run from the card-uploader folder on the scanner PC):
  python scripts/scan.py grab  <batch> <pass>     copy new C:\\twain files to scans/<batch>/pass<N>/
  python scripts/scan.py check <folder>           size + clipping report for every scan
  python scripts/scan.py build <batch> [--japanese]
        pairs pass1/pass2 scans of the same card, fills any clipped edge from the
        other pass, deskews, pads a dark margin, smooths print dots, and writes
        scans/<batch>/final/NN-front.jpg / NN-back.jpg + report.txt

Files: SVT writes imageNNNNNNNA.jpg (front, upside down) and ...B.jpg (back).
Japanese vintage backs are also upside down (--japanese).
Needs: pip install opencv-python numpy pillow
"""
import sys, os, shutil, glob, time
import cv2
import numpy as np
from PIL import Image, ImageFilter

TWAIN = r"C:\twain"
MIN_H = 2150          # a full card at 600 dpi is ~2100 px of card + margin; shorter = clipped
PAD = 150             # dark margin around the finished card
BG = (18, 18, 18)


def card_mask(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (7, 7), 0)
    _, m = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2:
        return m
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    return np.where(lab == k, 255, 0).astype(np.uint8)


def clipped_edges(img, tol=3):
    """Which image edges the card touches (= that side is cut off)."""
    m = card_mask(img)
    h, w = m.shape
    edges = []
    if m[:tol].any(): edges.append("top")
    if m[-tol:].any(): edges.append("bottom")
    if m[:, :tol].any(): edges.append("left")
    if m[:, -tol:].any(): edges.append("right")
    return edges


def load(path, flip):
    img = cv2.imread(path)
    return cv2.rotate(img, cv2.ROTATE_180) if flip else img


# ---------------- grab ----------------
def grab(batch, pas):
    dst = os.path.join("scans", batch, f"pass{pas}")
    os.makedirs(dst, exist_ok=True)
    # wait until SVT stops writing (no new file for 60 s)
    last = -1
    while True:
        files = glob.glob(os.path.join(TWAIN, "image*.jpg"))
        newest = max((os.path.getmtime(f) for f in files), default=0)
        if newest == last and time.time() - newest > 60:
            break
        last = newest
        print(f"{len(files)} files in C:\\twain, waiting for scanner to finish...")
        time.sleep(20)
    for f in sorted(files):
        shutil.copy2(f, dst)
    print(f"copied {len(files)} files to {dst}")


# ---------------- check ----------------
def check(folder):
    bad = 0
    for f in sorted(glob.glob(os.path.join(folder, "*.jpg"))):
        img = cv2.imread(f)
        h, w = img.shape[:2]
        e = clipped_edges(img)
        flag = "OK" if (h >= MIN_H and not e) else "CLIPPED"
        bad += flag != "OK"
        print(f"{os.path.basename(f):28s} {w}x{h}  {flag} {','.join(e)}")
    print(f"\n{bad} clipped scan(s)")
    return bad


# ---------------- build ----------------
orb = cv2.ORB_create(4000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


def feats(img):
    g = cv2.cvtColor(cv2.resize(img, None, fx=0.5, fy=0.5), cv2.COLOR_BGR2GRAY)
    return orb.detectAndCompute(g, card_mask(cv2.resize(img, None, fx=0.5, fy=0.5)))


def homography(a, b):
    """Warp matrix taking image b onto image a, plus inlier count."""
    ka, da = a
    kb, db = b
    if da is None or db is None:
        return None, 0
    m = sorted(bf.match(db, da), key=lambda x: x.distance)[:800]
    if len(m) < 12:
        return None, 0
    pb = np.float32([kb[x.queryIdx].pt for x in m]) * 2
    pa = np.float32([ka[x.trainIdx].pt for x in m]) * 2
    H, inl = cv2.findHomography(pb, pa, cv2.RANSAC, 4.0)
    return H, int(inl.sum()) if inl is not None else 0


def merge(a, b, H):
    """Put b (aligned) under a: fill everything a is missing."""
    h, w = a.shape[:2]
    # grow canvas so edges that fell off image a fit
    big = (h + 2 * PAD, w + 2 * PAD)
    T = np.array([[1, 0, PAD], [0, 1, PAD], [0, 0, 1]], float)
    A = cv2.warpPerspective(a, T, big[::-1], borderValue=BG)
    B = cv2.warpPerspective(b, T @ H, big[::-1], borderValue=BG)
    ma = cv2.warpPerspective(card_mask(a), T, big[::-1])
    ma = cv2.erode(ma, np.ones((9, 9), np.uint8))
    mb = cv2.warpPerspective(card_mask(b), T @ H, big[::-1])
    w8 = cv2.GaussianBlur(ma.astype(np.float32) / 255, (61, 61), 0)[..., None]
    out = (A * w8 + B * (1 - w8)).astype(np.uint8)
    return out


def finish(img):
    m = card_mask(img)
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rect = cv2.minAreaRect(max(cnts, key=cv2.contourArea))
    (cx, cy), (rw, rh), ang = rect
    if rw > rh:
        ang += 90 if ang < 0 else -90
        rw, rh = rh, rw
    M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
    rot = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), borderValue=BG)
    x0, y0 = int(cx - rw / 2), int(cy - rh / 2)
    crop = rot[max(0, y0):int(y0 + rh), max(0, x0):int(x0 + rw)]
    out = cv2.copyMakeBorder(crop, PAD, PAD, PAD, PAD, cv2.BORDER_CONSTANT, value=BG)
    # smooth print dots: GaussianBlur 1.5 then UnsharpMask(2, 40%, 3)
    p = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    p = p.filter(ImageFilter.GaussianBlur(1.5)).filter(ImageFilter.UnsharpMask(2, 40, 3))
    return p


def sides(folder, japanese):
    """Return list of (front, back) images per scanned sheet in a pass folder."""
    out = []
    for fa in sorted(glob.glob(os.path.join(folder, "image*A.jpg"))):
        fb = fa[:-5] + "B.jpg"
        a = load(fa, True)
        b = load(fb, japanese) if os.path.exists(fb) else None
        out.append((os.path.basename(fa)[:-5], a, b))
    return out


def build(batch, japanese=False):
    base = os.path.join("scans", batch)
    p1 = sides(os.path.join(base, "pass1"), japanese)
    p2 = sides(os.path.join(base, "pass2"), japanese) if os.path.isdir(os.path.join(base, "pass2")) else []
    # pass 2 was fed end-for-end: rotate 180 so it lines up with pass 1
    p2 = [(n, cv2.rotate(a, cv2.ROTATE_180), cv2.rotate(b, cv2.ROTATE_180) if b is not None else None) for n, a, b in p2]
    f2 = [(feats(a), feats(b) if b is not None else None) for _, a, b in p2]
    used = set()
    dst = os.path.join(base, "final")
    os.makedirs(dst, exist_ok=True)
    rep = []
    for i, (name, a, b) in enumerate(p1, 1):
        fa = feats(a)
        best, bj, swap = None, -1, False
        for j, (g2a, g2b) in enumerate(f2):
            if j in used:
                continue
            for cand, sw in ((g2a, False), (g2b, True)):  # a card may flip over between passes
                if cand is None:
                    continue
                H, n = homography(fa, cand)
                if H is not None and (best is None or n > best[1]):
                    best, bj, swap = (H, n), j, sw
        note = []
        front, back = a, b
        if best and best[1] >= 40:
            used.add(bj)
            _, a2, b2 = p2[bj]
            if swap:
                a2, b2 = b2, a2
            front = merge(a, a2, best[0])
            if b is not None and b2 is not None:
                Hb, nb = homography(feats(b), feats(b2))
                if Hb is not None and nb >= 40:
                    back = merge(b, b2, Hb)
            note.append(f"paired with pass2 {p2[bj][0]} ({best[1]} matches)")
        else:
            note.append("no pass2 match")
        problems = []
        for side, img in (("front", front), ("back", back)):
            if img is None:
                problems.append(f"{side} missing")
                continue
            fin = finish(img)
            fin.save(os.path.join(dst, f"{i:02d}-{side}.jpg"), quality=95)
            e = clipped_edges(cv2.cvtColor(np.array(fin), cv2.COLOR_RGB2BGR))
            if e:
                problems.append(f"{side} still touches {','.join(e)}")
        rep.append(f"{i:02d} {name}: {'; '.join(note)}; {'RESCAN: ' + '; '.join(problems) if problems else 'OK'}")
    extra = [p2[j][0] for j in range(len(p2)) if j not in used]
    if extra:
        rep.append(f"unmatched pass2 scans (repeat feeds or extra cards): {', '.join(extra)}")
    open(os.path.join(dst, "report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "grab":
        grab(sys.argv[2], sys.argv[3])
    elif cmd == "check":
        sys.exit(1 if check(sys.argv[2]) else 0)
    elif cmd == "build":
        build(sys.argv[2], "--japanese" in sys.argv)
    else:
        print(__doc__)
