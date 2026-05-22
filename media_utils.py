"""
media_utils.py
Utility functions for image processing, Tkinter display preparation,
placeholder creation, and PNG export.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageTk


def resize_cover(image: Image.Image, size: Tuple[int, int] = (600, 600)) -> Image.Image:
    """
    Resizes the cover image to the required square album size.

    Args:
        image: PIL image.
        size: Target size, default 600x600.

    Returns:
        Resized PIL image in RGB mode.
    """
    return image.convert("RGB").resize(size, Image.LANCZOS)


def convert_to_tk_image(image: Image.Image, size: Tuple[int, int] = (300, 300)) -> ImageTk.PhotoImage:
    """
    Converts a PIL image into ImageTk.PhotoImage for Tkinter display.

    Important:
        Keep a reference to the returned PhotoImage in the GUI class,
        otherwise Tkinter may not display it.

    Args:
        image: PIL image.
        size: Display size in the GUI.

    Returns:
        ImageTk.PhotoImage object.
    """
    display_image = image.convert("RGB").resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(display_image)


def create_placeholder_image(
    text: str = "Loading...",
    size: Tuple[int, int] = (600, 600),
    background: str = "#1DB954",
    foreground: str = "white",
) -> Image.Image:
    """
    Creates a simple placeholder image for loading/error states.

    Args:
        text: Text shown in the placeholder.
        size: Placeholder image size.
        background: Background color.
        foreground: Text color.

    Returns:
        PIL image.
    """
    image = Image.new("RGB", size, background)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 38)
    except OSError:
        font = ImageFont.load_default()

    # Compatible text centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2

    draw.text((x, y), text, fill=foreground, font=font)
    return image


def save_cover_png(image: Image.Image, folder_path: str | Path, filename: str = "album_cover.png") -> Path:
    """
    Saves the generated cover image as PNG.

    Args:
        image: PIL image to save.
        folder_path: Selected export folder.
        filename: Output filename.

    Returns:
        Path of the saved PNG file.
    """
    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)

    output_path = folder / filename
    image.convert("RGB").save(output_path, format="PNG")
    return output_path
