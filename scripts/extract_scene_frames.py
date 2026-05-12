#!/usr/bin/env python3
"""按场景变化自动抽取视频关键帧。

用法示例：
  python scripts/extract_scene_frames.py \
    --input assets/raw_episode.mp4 \
    --output-dir assets/scene_frames

脚本会比较相邻帧的直方图差异，检测到明显变化时导出一张截图。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


SUPPORTED_VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}


@dataclass
class FrameCandidate:
    frame_index: int
    second: float
    score: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="自动提取视频中不同场景的截图")
    parser.add_argument("--input", required=True, help="输入视频路径")
    parser.add_argument("--output-dir", default="assets/scene_frames", help="截图输出目录")
    parser.add_argument("--threshold", type=float, default=0.40, help="场景切换阈值，越小越敏感")
    parser.add_argument("--min-interval", type=float, default=1.5, help="相邻截图最小间隔（秒）")
    parser.add_argument("--max-shots", type=int, default=0, help="最多导出多少张图，0 代表不限制")
    parser.add_argument("--resize-width", type=int, default=480, help="用于检测的缩放宽度（不影响导出图）")
    parser.add_argument("--prefix", default="scene", help="导出文件名前缀")
    parser.add_argument("--jpg-quality", type=int, default=95, help="JPG 质量（1-100）")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    if not input_path.exists() or not input_path.is_file():
        raise ValueError(f"输入视频不存在：{input_path}")

    if input_path.suffix.lower() not in SUPPORTED_VIDEO_EXTS:
        allowed = ", ".join(sorted(SUPPORTED_VIDEO_EXTS))
        raise ValueError(f"不支持的视频格式：{input_path.suffix}，支持：{allowed}")

    if args.threshold <= 0:
        raise ValueError("--threshold 必须大于 0")
    if args.min_interval < 0:
        raise ValueError("--min-interval 不能小于 0")
    if args.max_shots < 0:
        raise ValueError("--max-shots 不能小于 0")
    if args.resize_width < 64:
        raise ValueError("--resize-width 建议 >= 64")
    if not 1 <= args.jpg_quality <= 100:
        raise ValueError("--jpg-quality 必须在 1 到 100")


def frame_signature(frame: np.ndarray, resize_width: int) -> np.ndarray:
    h, w = frame.shape[:2]
    scale = resize_width / max(1, w)
    resized = cv2.resize(frame, (resize_width, max(1, int(h * scale))), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist


def score_scene_change(prev_hist: np.ndarray, curr_hist: np.ndarray) -> float:
    corr = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_CORREL)
    return 1.0 - float(corr)


def save_frame(frame: np.ndarray, out_path: Path, jpg_quality: int) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(out_path), frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
    if not ok:
        raise RuntimeError(f"写入截图失败：{out_path}")


def extract_frames(args: argparse.Namespace) -> int:
    video_path = Path(args.input)
    output_dir = Path(args.output_dir)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频：{video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    if fps <= 0:
        fps = 25.0

    prev_hist: np.ndarray | None = None
    last_saved_second = -1e9
    saved_count = 0
    frame_idx = -1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        second = frame_idx / fps

        curr_hist = frame_signature(frame, args.resize_width)
        if prev_hist is None:
            # 第一帧直接保留，作为片头基准
            out = output_dir / f"{args.prefix}_{saved_count + 1:04d}_{second:08.3f}s.jpg"
            save_frame(frame, out, args.jpg_quality)
            saved_count += 1
            last_saved_second = second
            prev_hist = curr_hist
            continue

        score = score_scene_change(prev_hist, curr_hist)
        enough_gap = (second - last_saved_second) >= args.min_interval
        if score >= args.threshold and enough_gap:
            out = output_dir / f"{args.prefix}_{saved_count + 1:04d}_{second:08.3f}s.jpg"
            save_frame(frame, out, args.jpg_quality)
            print(f"[SHOT] #{saved_count + 1:04d} t={second:8.3f}s score={score:.4f} -> {out.name}")
            saved_count += 1
            last_saved_second = second
            if args.max_shots and saved_count >= args.max_shots:
                break

        prev_hist = curr_hist

    cap.release()
    print(f"提取完成：共导出 {saved_count} 张截图，输出目录：{output_dir}")
    return saved_count


def main() -> int:
    args = parse_args()
    try:
        validate_args(args)
        extract_frames(args)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
