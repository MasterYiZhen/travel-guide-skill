"""E21 受控视觉样例渲染（作者：yizhen）。

程序渲染 1080×1440 虚构教学页，产出对照页与四类缺陷页，用于检验 rc.9 审核规则。
不是模型生成图；不对应真实文物或旅行候选。缺陷意图记录在 maker-key.md，不发给 Reviewer。
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1440
BG = (246, 240, 228)
INK = (40, 48, 44)
GREEN = (38, 92, 70)
PANEL = (255, 252, 246)
BRONZE = (96, 122, 104)
BRONZE_DARK = (62, 84, 70)
RED = (178, 40, 60)
MAGENTA = (210, 30, 150)

SONG = "/System/Library/Fonts/Songti.ttc"
HEI = "/System/Library/Fonts/STHeiti Medium.ttc"
HEI_L = "/System/Library/Fonts/STHeiti Light.ttc"


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def vessel(d, cx, cy, s, legs=3, ears=2, color=BRONZE, outline=BRONZE_DARK):
    """三足两耳圆腹器：s 为半宽。"""
    bw, bh = s, int(s * 0.78)
    # 足
    leg_x = {3: [-0.62, 0.0, 0.62], 4: [-0.72, -0.24, 0.24, 0.72]}[legs]
    for lx in leg_x:
        x = cx + int(lx * bw)
        d.polygon([(x - int(0.13 * bw), cy + int(0.55 * bh)), (x + int(0.13 * bw), cy + int(0.55 * bh)),
                   (x + int(0.09 * bw), cy + int(1.25 * bh)), (x - int(0.09 * bw), cy + int(1.25 * bh))],
                  fill=color, outline=outline, width=3)
        d.ellipse([x - int(0.12 * bw), cy + int(1.15 * bh), x + int(0.12 * bw), cy + int(1.35 * bh)],
                  fill=outline)
    # 耳
    ear_pos = [-1, 1][:ears] if ears <= 2 else [-1, 1]
    for side in ear_pos:
        ex = cx + side * int(0.72 * bw)
        top = cy - int(1.05 * bh)
        d.rounded_rectangle([ex - int(0.17 * bw), top, ex + int(0.17 * bw), cy - int(0.45 * bh)],
                            radius=int(0.14 * bw), fill=color, outline=outline, width=3)
        d.rounded_rectangle([ex - int(0.08 * bw), top + int(0.12 * bh), ex + int(0.08 * bw), cy - int(0.6 * bh)],
                            radius=int(0.06 * bw), fill=BG, outline=outline, width=2)
    # 腹
    d.ellipse([cx - bw, cy - bh, cx + bw, cy + bh], fill=color, outline=outline, width=4)
    # 口沿
    d.ellipse([cx - int(0.82 * bw), cy - int(0.95 * bh), cx + int(0.82 * bw), cy - int(0.55 * bh)],
              fill=(120, 146, 128), outline=outline, width=4)
    d.ellipse([cx - int(0.66 * bw), cy - int(0.88 * bh), cx + int(0.66 * bw), cy - int(0.62 * bh)],
              fill=BRONZE_DARK)


def station_icon(d, cx, cy, kind, size=56):
    c = GREEN
    if kind == "gate":
        d.rectangle([cx - size // 2, cy - size // 4, cx - size // 2 + 12, cy + size // 2], fill=c)
        d.rectangle([cx + size // 2 - 12, cy - size // 4, cx + size // 2, cy + size // 2], fill=c)
        d.polygon([(cx - size // 2 - 10, cy - size // 4), (cx + size // 2 + 10, cy - size // 4), (cx, cy - size // 2 - 14)], fill=c)
    elif kind == "bronze":
        d.rectangle([cx - size // 2, cy - size // 3, cx + size // 2, cy + size // 2], outline=c, width=5)
        vessel(d, cx, cy + 4, 14, color=c, outline=c)
    elif kind == "pottery":
        d.rectangle([cx - size // 2, cy - size // 3, cx + size // 2, cy + size // 2], outline=c, width=5)
        d.ellipse([cx - 16, cy - 10, cx + 16, cy + 22], fill=c)
        d.rectangle([cx - 9, cy - 20, cx + 9, cy - 6], fill=c)


def arrow(d, x1, x2, y, color=GREEN, w=5):
    d.line([(x1, y), (x2, y)], fill=color, width=w)
    d.polygon([(x2, y), (x2 - 18, y - 11), (x2 - 18, y + 11)], fill=color)


def leader(d, p_from, p_to, color=GREEN):
    d.ellipse([p_from[0] - 9, p_from[1] - 9, p_from[0] + 9, p_from[1] + 9], fill=color)
    mid = (p_to[0], p_from[1])
    d.line([p_from, mid, p_to], fill=color, width=4)


def text(d, xy, s, f, fill=INK, spacing=10):
    d.multiline_text(xy, s, font=f, fill=fill, spacing=spacing)


def render(cfg):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = font(SONG, 78, 1)
    f_sub = font(HEI, 34)
    f_h = font(HEI, 40)
    f_mod_title = font(HEI, 42)
    f_body = font(SONG, 25, 1)
    f_small = font(HEI_L, 26)

    # 标题
    text(d, (250, 40), "虚构展馆测试页", f_title, GREEN)
    text(d, (300, 140), "沿单向路线，练习看懂器物造型", f_sub, INK)

    # 路线
    d.rounded_rectangle([40, 200, 1040, 420], radius=24, fill=PANEL, outline=GREEN, width=3)
    d.rounded_rectangle([40, 200, 260, 262], radius=18, fill=GREEN)
    text(d, (66, 208), "参观路线", f_h, (255, 255, 255))
    stations = [("南门", "gate"), ("青铜展区", "bronze"), ("陶器展区", "pottery"), ("北门", "gate")]
    xs = [150, 400, 650, 900]
    for (name, kind), x in zip(stations, xs):
        d.ellipse([x - 48, 240, x + 48, 336], fill=(226, 236, 228))
        station_icon(d, x, 288, kind)
        tw = d.textlength(name, font=f_sub)
        text(d, (x - tw / 2, 340), name, f_sub, INK)
    if cfg.get("route_arrows", True):
        for a, b in zip(xs[:-1], xs[1:]):
            arrow(d, a + 70, b - 70, 288)
    route_txt = "从南门进入，依次经过青铜展区、陶器展区，最后由北门离开。箭头表示前进方向。" if cfg.get("route_arrows", True) \
        else "从南门进入，依次经过青铜展区、陶器展区，最后由北门离开。"
    text(d, (70, 384), route_txt, f_small, INK)

    # 全貌
    d.rounded_rectangle([40, 430, 330, 486], radius=18, fill=PANEL, outline=GREEN, width=3)
    text(d, (62, 436), "三足器甲 · 全貌", f_h, GREEN)
    vessel(d, 280, 720, 200, legs=3, ears=2)

    # 局部面板
    d.rounded_rectangle([580, 500, 1040, 900], radius=24, fill=PANEL, outline=GREEN, width=3)
    d.rounded_rectangle([600, 430, 1040, 486], radius=18, fill=PANEL, outline=GREEN, width=3)
    detail_title = cfg.get("detail_title", "同一器物 · 双耳局部")
    text(d, (622, 436), detail_title, f_h, GREEN)
    # 放大耳部：两只大耳与口沿
    for side, ex in ((-1, 700), (1, 920)):
        d.rounded_rectangle([ex - 62, 560, ex + 62, 800], radius=54, fill=BRONZE, outline=BRONZE_DARK, width=4)
        d.rounded_rectangle([ex - 30, 600, ex + 30, 740], radius=26, fill=PANEL, outline=BRONZE_DARK, width=3)
    d.ellipse([620, 760, 1000, 880], fill=(120, 146, 128), outline=BRONZE_DARK, width=4)
    d.ellipse([660, 780, 960, 860], fill=BRONZE_DARK)
    if cfg.get("leader", True):
        src = cfg.get("leader_from", (424, 540))  # 右耳
        leader(d, src, (600, 460))

    # 三个观察模块
    mods = [("01", "数足", "先看下方的支撑部件：\n三条足均连接圆腹。\n沿轮廓逐一数清，\n确认总数为三。", "legs"),
            ("02", "看耳", "再看器口两侧：\n左右各有一耳。\n对照全貌与局部，\n找到相同的连接位置。", "ear"),
            ("03", "看腹", "最后观察器身：\n腹部轮廓圆润。\n结合完整外形，\n区分足、耳与腹\n各自的位置。", "belly")]
    if cfg.get("typo"):
        mods[2] = (mods[2][0], mods[2][1], mods[2][2].replace("观察", "观查"), mods[2][3])
    for i, (num, title, body, pic) in enumerate(mods):
        x0 = 40 + i * 340
        d.rounded_rectangle([x0, 940, x0 + 320, 1330], radius=22, fill=PANEL, outline=GREEN, width=3)
        d.rounded_rectangle([x0, 940, x0 + 320, 1010], radius=22, fill=GREEN)
        d.ellipse([x0 + 16, 950, x0 + 68, 1002], fill=PANEL)
        text(d, (x0 + 24, 958), num, font(HEI, 30), GREEN)
        ft, fill = f_mod_title, (255, 255, 255)
        if i == 1 and cfg.get("font_mismatch"):
            ft, fill = font(SONG, 58, 1), MAGENTA
            text(d, (x0 + 84, 936), title, ft, fill)
        else:
            text(d, (x0 + 84, 950), title, ft, fill)
        if cfg.get("module_pics", True):
            if pic == "legs":
                vessel(d, x0 + 160, 1075, 42, legs=cfg.get("legs_small", 3), ears=0)
            elif pic == "ear":
                d.rounded_rectangle([x0 + 134, 1030, x0 + 186, 1120], radius=24, fill=BRONZE, outline=BRONZE_DARK, width=3)
                d.rounded_rectangle([x0 + 148, 1046, x0 + 172, 1100], radius=12, fill=PANEL, outline=BRONZE_DARK, width=2)
                d.ellipse([x0 + 110, 1104, x0 + 210, 1136], fill=(120, 146, 128), outline=BRONZE_DARK, width=3)
            else:
                d.ellipse([x0 + 116, 1040, x0 + 204, 1128], fill=BRONZE, outline=BRONZE_DARK, width=3)
                d.ellipse([x0 + 130, 1030, x0 + 190, 1058], fill=(120, 146, 128), outline=BRONZE_DARK, width=3)
        text(d, (x0 + 20, 1150), body, f_body, INK, spacing=8)

    # 底部边界说明
    text(d, (110, 1372), "虚构测试资料｜仅支持造型观察；本页不提供年代、历史、用途或真实展馆信息。", f_small, INK)

    # 后处理缺陷
    if cfg.get("blur_box"):
        x0, y0, x1, y1 = cfg["blur_box"]
        region = img.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(7))
        img.paste(region, (x0, y0))
    if cfg.get("glyph_scramble"):
        x0, y0, x1, y1 = cfg["glyph_scramble"]
        region = img.crop((x0, y0, x1, y1))
        w, h = region.size
        # 把字符区域切成横条随机错位，形成笔画粘连／错位的异常字形
        strips = [region.crop((0, k, w, min(k + 4, h))) for k in range(0, h, 4)]
        out = Image.new("RGB", (w, h), PANEL)
        for k, s in enumerate(strips):
            out.paste(s, ((k % 3 - 1) * 5, k * 4))
        img.paste(out, (x0, y0))
    for box in cfg.get("patches", []):
        d.rectangle(box, fill=(232, 222, 200))
    return img


CONFIGS = {
    # 对照页：无预设缺陷
    "page-e-control": {},
    # A：可辨认错字（观查）+ 模块 1 正文后两行重度模糊无法辨认 + “置”字字形错乱
    "page-a-text": {"typo": True, "blur_box": (56, 1212, 344, 1282), "glyph_scramble": (838, 1280, 868, 1312)},
    # B：同级标题字体、字号、颜色失调
    "page-b-font": {"font_mismatch": True},
    # C：各自清楚但缺少解释关系：无引线、局部标题泛化、路线无箭头、模块无小图
    "page-c-juxtapose": {"leader": False, "detail_title": "局部图", "route_arrows": False, "module_pics": False},
    # D：补丁遮挡（左耳与模块 2 正文）+ 引线从腹部出发 + 数足小图四足
    "page-d-patch": {"patches": [(650, 640, 705, 720), (398, 1180, 600, 1214)], "leader_from": (300, 760), "legs_small": 4},
}

if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "pages"
    out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, cfg in CONFIGS.items():
        p = out / f"{name}.png"
        render(cfg).save(p)
        manifest.append({"file": p.name, "size": [W, H], "config": cfg})
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print("\n".join(m["file"] for m in manifest))
