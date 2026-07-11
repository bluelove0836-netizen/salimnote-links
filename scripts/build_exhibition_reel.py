#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import textwrap
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "reels" / "exhibition-12912-high-discount" / "manifest.json"
OUT_DIR = MANIFEST_PATH.parent / "output"
W = 1080
H = 1920
FPS = 30
PER_SLIDE = 2.8

FONT_REGULAR = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_BOLD = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and Path(FONT_BOLD).exists() else FONT_REGULAR
    return ImageFont.truetype(path, size)


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def fit_text(text: str, width: int = 18) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def download_image(url: str, target: Path) -> Path:
    if target.exists() and target.stat().st_size > 5_000:
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, str(target))
    return target


def cover_crop(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    src_w, src_h = img.size
    dst_w, dst_h = size
    src_ratio = src_w / src_h
    dst_ratio = dst_w / dst_h
    if src_ratio > dst_ratio:
        new_h = dst_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = dst_w
        new_h = int(new_w / src_ratio)
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - dst_w) // 2
    top = (new_h - dst_h) // 2
    return resized.crop((left, top, left + dst_w, top + dst_h))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def draw_text_block(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, fnt, fill, spacing: int = 8):
    draw.multiline_text((x, y), text, font=fnt, fill=fill, spacing=spacing)


def render_intro_slide(data: dict, out: Path) -> Path:
    img = Image.new("RGB", (W, H), "#f4eee5")
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((56, 72, W - 56, H - 72), radius=44, fill="#fbf7f1", outline="#eadfce", width=3)
    draw.ellipse((760, 120, 1060, 420), fill="#e4c8a8")
    draw.ellipse((40, 1320, 340, 1620), fill="#dbcfc0")

    draw_text_block(draw, 112, 164, "살림노트", font(38, True), "#b85d41")
    draw_text_block(draw, 112, 256, "오늘의집 기획전에서\n할인율 높은 살림템만\n빠르게 추렸어요", font(78, True), "#2f241d", 10)
    draw_text_block(draw, 112, 560, data["subtitle"], font(34), "#74675c")

    badge_y = 700
    for idx, label in enumerate(["할인율 상위", "살림템 위주", "링크는 프로필"]):
        x1 = 112 + idx * 270
        x2 = x1 + 224
        draw.rounded_rectangle((x1, badge_y, x2, badge_y + 72), radius=36, fill="#efe2d3")
        draw_text_block(draw, x1 + 30, badge_y + 20, label, font(26, True), "#6b5849")

    draw.rounded_rectangle((112, 1380, W - 112, 1650), radius=36, fill="#fffaf5", outline="#e4d7c7", width=2)
    draw_text_block(draw, 156, 1438, "기획전 전체 링크까지 같이 넣어둘게요", font(40, True), "#2f241d")
    draw_text_block(draw, 156, 1518, "릴스 보고 바로 전체 딜 확인할 수 있게 연결합니다.", font(28), "#74675c")

    draw_text_block(draw, 112, 1730, "1/7", font(26, True), "#a28d78")
    img.save(out)
    return out


def render_product_slide(item: dict, index: int, total: int, out: Path, image_path: Path) -> Path:
    canvas = Image.new("RGB", (W, H), "#f5efe6")
    product = Image.open(image_path).convert("RGB")
    bg = cover_crop(product, (W, H)).filter(ImageFilter.GaussianBlur(18))
    overlay = Image.new("RGBA", (W, H), (245, 239, 230, 155))
    canvas.paste(bg, (0, 0))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")

    card = Image.new("RGBA", (W - 96, H - 144), (255, 250, 244, 235))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle((0, 0, card.width - 1, card.height - 1), radius=42, fill=(255, 250, 244, 235), outline=(233, 221, 205, 255), width=2)
    canvas.paste(card, (48, 72), rounded_mask(card.size, 42))

    clipped = cover_crop(product, (W - 176, 820))
    canvas.paste(clipped, (88, 132), rounded_mask(clipped.size, 32))

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((88, 980, 320, 1056), radius=38, fill="#bf5c3f")
    draw_text_block(draw, 132, 1001, item["hook"], font(34, True), "white")

    draw_text_block(draw, 88, 1110, fit_text(item["name"], 15), font(58, True), "#2f241d", 10)
    draw_text_block(draw, 88, 1328, item["priceText"], font(66, True), "#2f241d")
    draw_text_block(draw, 88, 1416, fit_text(item["reason"], 22), font(30), "#6f6257", 10)

    draw.rounded_rectangle((88, 1578, W - 88, 1688), radius=30, fill="#efe5d9")
    draw_text_block(draw, 126, 1610, "기획전 링크는 프로필 상단에 넣어둘게요", font(30, True), "#7a6553")

    draw_text_block(draw, 88, 1750, f"{index}/{total}", font(26, True), "#a28d78")
    img = canvas.convert("RGB")
    img.save(out)
    return out


def render_end_slide(data: dict, out: Path) -> Path:
    img = Image.new("RGB", (W, H), "#2d241d")
    draw = ImageDraw.Draw(img)
    draw.ellipse((640, 100, 1050, 520), fill="#b76346")
    draw.ellipse((10, 1260, 360, 1610), fill="#5b6c49")
    draw.rounded_rectangle((64, 88, W - 64, H - 88), radius=48, fill="#faf5ef")

    draw_text_block(draw, 128, 220, "더 많은 할인템은", font(50), "#7d6553")
    draw_text_block(draw, 128, 308, "기획전 전체 링크에서\n한 번에 보기", font(84, True), "#2f241d", 12)
    draw_text_block(draw, 128, 620, data["exhibitionTitle"], font(34, True), "#bf5c3f")

    draw.rounded_rectangle((128, 820, W - 128, 1140), radius=40, fill="#f1e5d8")
    draw_text_block(draw, 178, 900, "프로필 링크에서", font(52, True), "#2f241d")
    draw_text_block(draw, 178, 986, "기획전 전체 보기 눌러주세요", font(52, True), "#2f241d")

    draw.rounded_rectangle((128, 1280, W - 128, 1400), radius=36, fill="#bf5c3f")
    draw_text_block(draw, 224, 1316, "bio link • tinyurl.com/29ug2dv6", font(28, True), "white")
    draw_text_block(draw, 128, 1532, "지금 저장해두면 다음 제품 고를 때 훨씬 빨라요.", font(34), "#6f6257")
    draw_text_block(draw, 128, 1710, "7/7", font(26, True), "#a28d78")

    img.save(out)
    return out


def build_video(slides: list[Path], out_mp4: Path) -> Path:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = out_mp4.parent / "_video_tmp"
    tmp_dir.mkdir(exist_ok=True)
    segments: list[Path] = []

    frames = int(PER_SLIDE * FPS)
    for idx, slide in enumerate(slides):
        seg = tmp_dir / f"seg{idx}.mp4"
        vf = f"zoompan=z='min(zoom+0.0007,1.08)':d={frames}:s={W}x{H}:fps={FPS}"
        subprocess.run(
            [
                "ffmpeg", "-y", "-loop", "1", "-i", str(slide), "-t", str(PER_SLIDE),
                "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(seg)
            ],
            check=True,
            capture_output=True,
        )
        segments.append(seg)

    concat = tmp_dir / "list.txt"
    concat.write_text("".join(f"file '{seg}'\n" for seg in segments), encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out_mp4)
        ],
        check=True,
        capture_output=True,
    )

    for seg in segments:
        seg.unlink(missing_ok=True)
    concat.unlink(missing_ok=True)
    tmp_dir.rmdir()
    return out_mp4


def main() -> None:
    data = load_manifest()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = OUT_DIR / "cache"
    slides_dir = OUT_DIR / "slides"
    cache_dir.mkdir(exist_ok=True)
    slides_dir.mkdir(exist_ok=True)

    slide_paths: list[Path] = []
    slide_paths.append(render_intro_slide(data, slides_dir / "slide-1.png"))

    total = len(data["items"]) + 2
    for idx, item in enumerate(data["items"], start=2):
        image_path = download_image(item["imageUrl"], cache_dir / f"{item['id']}.jpg")
        slide_paths.append(render_product_slide(item, idx, total, slides_dir / f"slide-{idx}.png", image_path))

    slide_paths.append(render_end_slide(data, slides_dir / f"slide-{total}.png"))
    build_video(slide_paths, OUT_DIR / "salimnote-exhibition-12912-high-discount-reel.mp4")


if __name__ == "__main__":
    main()
