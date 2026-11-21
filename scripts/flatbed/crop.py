"""Cut each card out of a flatbed page, straighten it, pad an even border.
usage: python crop.py page.jpg outprefix
"""
import sys, cv2, numpy as np

CARD_W, CARD_H = 1488, 2079   # 63 x 88 mm at 600 dpi
PAD = 60

def find_cards(img):
    blur = cv2.GaussianBlur(img, (0, 0), 3)
    bg = np.median(blur[:60, :60].reshape(-1, 3), axis=0)
    diff = np.abs(blur.astype(int) - bg).max(axis=2)
    m = (diff > 18).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cn, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    CW, CH = 1490, 2068
    out = []
    for c in cn:
        k = int(round(cv2.contourArea(c) / (CW * CH)))
        if k < 1: continue
        if k == 1:
            rects = [cv2.minAreaRect(c)]
        else:
            blob = np.zeros(m.shape, np.uint8); cv2.drawContours(blob, [c], -1, 1, -1)
            ys, xs = np.nonzero(blob[::4, ::4]); pts = np.float32(np.c_[xs, ys] * 4)
            _, lab, _ = cv2.kmeans(pts, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.5), 8, cv2.KMEANS_PP_CENTERS)
            rects = [cv2.minAreaRect(pts[lab.ravel() == i]) for i in range(k)]
        for (cx, cy), (w, h), a in rects:
            if w > h: w, h, a = h, w, a - 90
            if abs(w - CW) > 60 or abs(h - CH) > 80:
                w, h = CW, CH
            out.append(((cx, cy), (w, h), a))
    return out

def refine(grad, r, CW=1490, CH=2068):
    """Snap a fixed-size card rectangle onto the strongest border edges."""
    (cx, cy), _, a = r
    t = np.linspace(-0.5, 0.5, 120)
    # perimeter sample points in card coordinates (excluding rounded corners)
    tt = t[np.abs(t) < 0.44]
    px = np.r_[tt * CW, tt * CW, np.full_like(tt, -CW / 2), np.full_like(tt, CW / 2)]
    py = np.r_[np.full_like(tt, -CH / 2), np.full_like(tt, CH / 2), tt * CH, tt * CH]
    H, W = grad.shape
    best = (-1, cx, cy, a)
    for da in np.arange(-1.5, 1.51, 0.25):
        th = np.deg2rad(a + da); c, s = np.cos(th), np.sin(th)
        rx = px * c - py * s; ry = px * s + py * c
        for dx in range(-48, 49, 4):
            xs = (rx + cx + dx).astype(int)
            for dy in range(-48, 49, 4):
                ys = (ry + cy + dy).astype(int)
                ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H)
                sc = grad[ys[ok], xs[ok]].sum()
                if sc > best[0]:
                    best = (sc, cx + dx, cy + dy, a + da)
    _, bx, by, ba = best
    return ((bx, by), (CW, CH), ba)

def warp(img, r):
    box = cv2.boxPoints(r)
    s = box.sum(1); d = np.diff(box, axis=1).ravel()
    tl, br = box[np.argmin(s)], box[np.argmax(s)]
    tr, bl = box[np.argmin(d)], box[np.argmax(d)]
    src = np.float32([tl, tr, br, bl])
    w = np.linalg.norm(tr - tl); h = np.linalg.norm(bl - tl)
    if w > h:  # card lying sideways: rotate corner order
        src = np.float32([bl, tl, tr, br])
    dst = np.float32([[0, 0], [CARD_W, 0], [CARD_W, CARD_H], [0, CARD_H]])
    M = cv2.getPerspectiveTransform(src, dst)
    card = cv2.warpPerspective(img, M, (CARD_W, CARD_H), flags=cv2.INTER_CUBIC,
                               borderMode=cv2.BORDER_REPLICATE)
    return card

def finish(card):
    card = cv2.GaussianBlur(card, (0, 0), 1.2)
    sharp = cv2.addWeighted(card, 1.4, cv2.GaussianBlur(card, (0, 0), 2), -0.4, 0)
    return cv2.copyMakeBorder(sharp, PAD, PAD, PAD, PAD, cv2.BORDER_CONSTANT, value=(245, 245, 245))

if __name__ == '__main__':
    img = cv2.imread(sys.argv[1])
    g = cv2.cvtColor(cv2.GaussianBlur(img, (0, 0), 2), cv2.COLOR_BGR2GRAY).astype(np.float32)
    grad = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    grad = cv2.GaussianBlur(grad, (0, 0), 3)
    rects = [refine(grad, r) for r in find_cards(img)]
    # order rows top->bottom, then left->right
    rects.sort(key=lambda r: r[0][1])
    rows = [rects[i:i + 3] for i in range(0, len(rects), 3)]
    k = 0
    for row in rows:
        for r in sorted(row, key=lambda r: r[0][0]):
            k += 1
            cv2.imwrite(f'{sys.argv[2]}_{k:02d}_x{int(r[0][0])}_y{int(r[0][1])}.jpg',
                        finish(warp(img, r)), [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(len(rects), 'cards')
