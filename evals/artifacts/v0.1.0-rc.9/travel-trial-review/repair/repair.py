"""天坛五页候选：首审 4 处字形错误的栅格局部修复（作者：yizhen）。

方法：定位原文字行的实际墨迹范围，用周边底色覆盖整行，再以相近系统字体按原行高、原行宽重绘正确文字。
不改动其他像素；输出新版本文件并记录变更范围。环境没有模型图片编辑能力，此为可用工具内的修复方式。
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HEI_M = "/System/Library/Fonts/STHeiti Medium.ttc"
HEI_L = "/System/Library/Fonts/STHeiti Light.ttc"
HIRA_W6 = ("/System/Library/Fonts/Hiragino Sans GB.ttc", 1)
ROOT = Path(__file__).resolve().parent.parent

# (源文件, 目标文件, 分析框, 正确整行文字, 字体)
FIXES = [
    ("page-01-v3.png", "page-01-v5.png", [((600, 244, 690, 272), "祈年殿院落", HEI_M, 0),
                                          ((634, 1226, 915, 1250), "每周一闭馆，法定节假日期间除外。", HIRA_W6, 0)]),
    # ("page-04-v2.png", "page-04-v3.png", [((24, 916, 540, 948), "声波沿内面连续反射，这些工艺与几何条件共同支", HIRA_W6, 0)]),
    # ("page-05-v3.png", "page-05-v4.png", [((785, 1192, 1040, 1218), "一个人请服务员协助适量点餐。", HIRA_W6, 0)]),
]


def ink_box(a, box, thr=110):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1]
    bg = np.median(sub.reshape(-1, 3), axis=0)
    ink = np.abs(sub - bg).sum(axis=2) > thr
    ys = np.where(ink.sum(axis=1) > 0)[0]
    xs = np.where(ink.sum(axis=0) > 0)[0]
    color = np.median(sub[ink], axis=0)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1), tuple(int(v) for v in bg), tuple(int(v) for v in color)


def fit_font(path, text, target_w, target_h):
    best = None
    path, index = path if isinstance(path, tuple) else (path, 0)
    for size in range(10, 60):
        f = ImageFont.truetype(path, size, index=index)
        l, t, r, b = f.getbbox(text)
        w, h = r - l, b - t
        score = abs(w - target_w) / target_w + abs(h - target_h) / target_h
        if best is None or score < best[0]:
            best = (score, size, f, (l, t, w, h))
    return best


changes = []
for src, dst, fixes in FIXES:
    im = Image.open(ROOT / "images" / src).convert("RGB")
    a = np.asarray(im).astype(int)
    d = ImageDraw.Draw(im)
    for box, text, font_path, stroke in fixes:
        (ix0, iy0, ix1, iy1), bg, color = ink_box(a, box)
        pad = 2
        d.rectangle([ix0 - pad, iy0 - pad, ix1 + pad, iy1 + pad], fill=bg)
        score, size, f, (l, t, w, h) = fit_font(font_path, text, ix1 - ix0, iy1 - iy0)
        # 水平按原行宽等比放置：逐字定位，使整行宽度与原行一致
        n = len(text)
        step = (ix1 - ix0 - (f.getbbox(text[-1])[2] - f.getbbox(text[-1])[0])) / max(n - 1, 1)
        for i, ch in enumerate(text):
            cl, ct, cr, cb = f.getbbox(ch)
            x = ix0 + i * step - cl
            d.text((x, iy0 - t), ch, font=f, fill=color, stroke_width=stroke, stroke_fill=color)
        changes.append({"file": dst, "region": [int(ix0 - pad), int(iy0 - pad), int(ix1 + pad), int(iy1 + pad)], "text": text,
                        "font": Path(font_path[0] if isinstance(font_path, tuple) else font_path).name + (f"#{font_path[1]}" if isinstance(font_path, tuple) else ""), "font_size": size, "stroke_width": stroke, "bg": bg, "ink": color})
    im.save(ROOT / "images" / dst)
    changes.append({"file": dst, "sha256": hashlib.sha256((ROOT / "images" / dst).read_bytes()).hexdigest(),
                    "size": list(im.size)})
(ROOT / "repair" / "changes-03.json").write_text(json.dumps(changes, indent=2, ensure_ascii=False))
print(json.dumps(changes, indent=2, ensure_ascii=False))
