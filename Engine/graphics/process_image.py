import os
import os.path
import shutil

from PIL import Image, ImageOps

from Enums.colors import BLACK
from settings import SQUAD_BORDER_SIZE, TEMP_SPRITES_PATH


def resize_image(original_image_path: str, x_resize: int, y_resize: int) -> str:
    """Returns path to new image"""
    new_path = os.path.join(
        TEMP_SPRITES_PATH,
        f"_temp_resized_sprite_{os.path.split(original_image_path)[-1]}.png",
    )
    img = Image.open(original_image_path)
    resized_image = img
    resized_image.thumbnail((x_resize, y_resize), Image.Resampling.LANCZOS)
    resized_image.save(new_path)

    return new_path


def add_border_to_image(
    image_path: str, rbg_color: tuple[int] = BLACK, path_suffix: str = ""
) -> str:
    """Creates new image with border, if it does not exist already. Returns path to saved image."""
    new_path = os.path.join(
        TEMP_SPRITES_PATH,
        f"_temp_border_{os.path.split(image_path)[-1]}_{path_suffix}.png",
    )
    # If image exists, do not replace it.
    if os.path.exists(new_path):
        return new_path

    img = Image.open(image_path)
    img_with_border = ImageOps.expand(img, border=SQUAD_BORDER_SIZE, fill=rbg_color)
    img_with_border.thumbnail(img.size, Image.Resampling.LANCZOS)
    img_with_border.save(new_path)

    return new_path


def clear_temp_directory():
    """Clear temp directory with .png icon images."""
    for filename in os.listdir(TEMP_SPRITES_PATH):
        file_path = os.path.join(TEMP_SPRITES_PATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))
