#!/usr/bin/env python3
"""将人物剧照统一处理为透明背景的等尺寸 PNG。

用法：
  python scripts/prepare_character_assets.py --size 768

默认从 assets/raw 读取图片，并输出到 assets/portraits。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image
from rembg import remove


SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


@dataclass(frozen=True)
class Character:
    name: str
    slug: str


CHARACTERS: tuple[Character, ...] = (
    Character("毛猛达", "mao_mengda"),
    Character("陈国庆", "chen_guoqing"),
    Character("姚祺儿", "yao_qier"),
    Character("李九松", "li_jiusong"),
    Character("嫩娘", "nen_niang"),
    Character("朱桢", "zhu_zhen"),
)


def find_source_image(raw_dir: Path, name: str) -> Path | None:
    candidates: list[Path] = []
    for path in raw_dir.iterdir():
        if path.suffix.lower() in SUPPORTED_EXTS and path.is_file() and path.stem.startswith(name):
            candidates.append(path)
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.name)
    return candidates[0]


def iter_existing_sources(raw_dir: Path) -> Iterable[tuple[Character, Path]]:
    for character in CHARACTERS:
        source = find_source_image(raw_dir, character.name)
        if source is None:
            print(f"[SKIP] 未找到原图：{character.name}（请放到 {raw_dir}，文件名以人物名开头）")
            continue
        yield character, source


def remove_background(image_path: Path) -> Image.Image:
    with Image.open(image_path) as src:
        rgba = src.convert("RGBA")
        cutout = remove(rgba)
    if not isinstance(cutout, Image.Image):
        # rembg 某些版本会返回 bytes
        from io import BytesIO

        cutout = Image.open(BytesIO(cutout)).convert("RGBA")
    return cutout


def crop_by_alpha(img: Image.Image) -> Image.Image:
    alpha = img.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return img
    return img.crop(bbox)


def place_on_square(img: Image.Image, size: int) -> Image.Image:
    img = img.copy()
    img.thumbnail((size, size), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - img.width) // 2, (size - img.height) // 2)
    canvas.paste(img, offset, img)
    return canvas


def process_one(source: Path, target: Path, size: int) -> None:
    no_bg = remove_background(source)
    cropped = crop_by_alpha(no_bg)
    squared = place_on_square(cropped, size)
    target.parent.mkdir(parents=True, exist_ok=True)
    squared.save(target, format="PNG")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="批量处理老娘舅人物 PNG 立绘")
    parser.add_argument("--raw-dir", default="assets/raw", help="原图目录")
    parser.add_argument("--output-dir", default="assets/portraits", help="输出目录")
    parser.add_argument("--size", type=int, default=768, help="输出方图边长")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    output_dir = Path(args.output_dir)

    if not raw_dir.exists():
        print(f"原图目录不存在：{raw_dir}")
        return 1

    handled = 0
    for character, source in iter_existing_sources(raw_dir):
        target = output_dir / f"{character.slug}.png"
        process_one(source, target, args.size)
        handled += 1
        print(f"[OK] {character.name}: {source.name} -> {target}")

    print(f"处理完成：{handled} 张")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
