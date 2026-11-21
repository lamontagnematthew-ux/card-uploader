"""Crop a front/back flatbed pair, match cards by mirrored position, write numbered files.
usage: python pairset.py fronts.jpg backs.jpg start_num outdir sheet.jpg
"""
import sys, glob, re, shutil, subprocess, os, tempfile
from PIL import Image

fr, bk, start, outdir, sheet = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
tmp = tempfile.mkdtemp(dir='.')
here = os.path.dirname(os.path.abspath(__file__))
for img, pre in ((fr, 'F'), (bk, 'B')):
    subprocess.run([sys.executable, '-I', os.path.join(here, 'crop.py'), img, f'{tmp}/{pre}'], check=True)
W = Image.open(fr).size[0]
pos = lambda f: tuple(map(int, re.search(r'_x(\d+)_y(\d+)', f).groups()))
F = sorted(glob.glob(f'{tmp}/F_*')); B = sorted(glob.glob(f'{tmp}/B_*'))
os.makedirs(outdir, exist_ok=True)
import numpy as np
from scipy.optimize import linear_sum_assignment
cost = np.array([[(pos(b)[0] - pos(f)[0]) ** 2 + (pos(b)[1] - pos(f)[1]) ** 2 for b in B] for f in F])
ri, ci = linear_sum_assignment(cost)
match = dict(zip(ri, ci))
pairs = []
for i, f in enumerate(F):
    b = B[match[i]]
    n = start + i
    shutil.copy(f, f'{outdir}/B2-{n:02d}-front.jpg'); shutil.copy(b, f'{outdir}/B2-{n:02d}-back.jpg')
    pairs.append((f'{outdir}/B2-{n:02d}-front.jpg', f'{outdir}/B2-{n:02d}-back.jpg'))
print(len(F), 'fronts', len(B), 'backs')
ims = [Image.open(p).resize((200, 280)) for pr in pairs for p in pr]
s = Image.new('RGB', (200 * len(pairs), 560), 'white')
for i, (a, b) in enumerate(pairs):
    s.paste(Image.open(a).resize((200, 280)), (i * 200, 0)); s.paste(Image.open(b).resize((200, 280)), (i * 200, 280))
s.save(sheet, quality=80)
