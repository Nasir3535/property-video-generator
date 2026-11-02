"""Render portrait MP4 property promos with subtle motion and cross-fade transitions."""
from pathlib import Path
import math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from script_writer import build_scenes

W, H = 540, 960
FPS = 15


def _font(size, bold=False):
    candidates = [
        '/usr/share/fonts/truetype/lato/Lato-Bold.ttf' if bold else '/usr/share/fonts/truetype/lato/Lato-Regular.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def _cover(img: Image.Image, scale: float):
    img = img.convert('RGB')
    target_ratio = W / H
    ratio = img.width / img.height
    if ratio > target_ratio:
        nh = H
        nw = int(nh * ratio)
    else:
        nw = W
        nh = int(nw / ratio)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    # Slow zoom-in around center; crop stays within resized image.
    cw, ch = int(W / scale), int(H / scale)
    left = max(0, (nw - cw) // 2)
    top = max(0, (nh - ch) // 2)
    crop = img.crop((left, top, left + cw, top + ch)).resize((W, H), Image.Resampling.LANCZOS)
    return crop


def _draw_text(img, title, caption, index, total, brand='PROPERTY TOUR'):
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # Top brand chip and bottom cinematic gradient panel.
    d.rounded_rectangle((42, 48, 300, 105), radius=22, fill=(12, 24, 36, 190), outline=(255,255,255,75), width=2)
    d.text((64, 64), brand, font=_font(22, True), fill=(255,255,255,245))
    panel = Image.new('RGBA', (W, 420), (5, 15, 25, 0))
    pix = np.zeros((420, W, 4), dtype=np.uint8)
    for y in range(420):
        pix[y, :, :] = (5, 13, 22, int(20 + 215 * y / 419))
    panel = Image.fromarray(pix, 'RGBA')
    overlay.alpha_composite(panel, (0, H-420))
    d = ImageDraw.Draw(overlay)
    # Wrap long titles without clipping.
    words, lines, line = title.split(), [], ''
    font = _font(52, True)
    for word in words:
        trial = (line + ' ' + word).strip()
        if d.textbbox((0,0), trial, font=font)[2] > W-88 and line:
            lines.append(line); line = word
        else: line = trial
    if line: lines.append(line)
    y = H-350
    for text in lines[:2]:
        d.text((46, y), text, font=font, fill='white', stroke_width=1, stroke_fill=(0,0,0,100)); y += 66
    cap_font = _font(29)
    # caption line wrap
    cap_words, cap_lines, cap_line = caption.split(), [], ''
    for word in cap_words:
        trial = (cap_line + ' ' + word).strip()
        if d.textbbox((0,0), trial, font=cap_font)[2] > W-92 and cap_line:
            cap_lines.append(cap_line); cap_line = word
        else: cap_line = trial
    if cap_line: cap_lines.append(cap_line)
    for text in cap_lines[:2]:
        d.text((48, y+5), text, font=cap_font, fill=(225,235,242,255)); y += 42
    # Progress indicator.
    d.rounded_rectangle((48, H-34, W-48, H-24), radius=5, fill=(255,255,255,80))
    d.rounded_rectangle((48, H-34, 48 + int((W-96)*index/max(total,1)), H-24), radius=5, fill=(222,178,104,255))
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')


def render_video(images, details, output_path, seconds_per_scene=2.2, transition_seconds=0.3):
    images = [Path(x) for x in images if Path(x).exists()]
    if len(images) < 4:
        raise ValueError(f'Please provide at least 4 valid images; received {len(images)}.')
    scenes = build_scenes(details)
    # Use the first images for the opening/features and final image for CTA.
    scene_count = min(len(images), len(scenes))
    images, scenes = images[:scene_count], scenes[:scene_count]
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(out), cv2.VideoWriter_fourcc(*'mp4v'), FPS, (W,H))
    if not writer.isOpened():
        raise RuntimeError('Could not initialize MP4 writer. Check your OpenCV/FFmpeg installation.')
    try:
        rendered = []
        for i, (path, scene) in enumerate(zip(images, scenes)):
            src = Image.open(path).convert('RGB')
            frames = []
            n = int(seconds_per_scene * FPS)
            for f in range(n):
                zoom = 1.0 + 0.045 * (f / max(n-1,1))
                base = _cover(src, zoom)
                frame = _draw_text(base, scene['title'], scene['caption'], i+1, scene_count)
                frames.append(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
            rendered.append(frames)
        fade_n = max(1, int(transition_seconds*FPS))
        for i, frames in enumerate(rendered):
            if i > 0:
                prev = rendered[i-1][-fade_n:]
                curr = frames[:fade_n]
                for j in range(min(len(prev),len(curr))):
                    alpha = (j+1)/(min(len(prev),len(curr))+1)
                    blended = cv2.addWeighted(prev[j], 1-alpha, curr[j], alpha, 0)
                    writer.write(blended)
                frames = frames[fade_n:]
            for frame in frames:
                writer.write(frame)
    finally:
        writer.release()
    if not out.exists() or out.stat().st_size < 100_000:
        raise RuntimeError('Video export failed or produced an unexpectedly small file.')
    return str(out)
