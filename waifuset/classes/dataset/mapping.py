import json
from typing import Dict, Union
from pathlib import Path
from .. import ImageInfo
from ...utils import log_utils as logu, file_utils


def track_rename(image_info: ImageInfo, stem_map: Dict[str, str]):
    stem = image_info.stem
    if stem in stem_map:
        image_info.image_path = image_info.image_path.with_name(stem_map[stem] + image_info.suffix)
    return image_info


def track_image_path(image_info: ImageInfo, tarset):
    img_key = image_info.key
    if img_key in tarset:
        old = image_info.image_path
        new = tarset[img_key]
        new = new.image_path if isinstance(new, ImageInfo) else new
        if old != new:
            image_info.image_path = new
            # print(f"[path] `{logu.blue(img_key)}` `{logu.yellow(old)}` -> `{logu.green(new)}`.")
    return image_info


def track_caption(image_info: ImageInfo, dataset):
    image_key = image_info.key
    if image_key in dataset and dataset[image_key].caption:
        image_info.caption = dataset[image_key].caption
    return image_info


def track_artist(image_info: ImageInfo):
    if not image_info.caption:
        return image_info
    old = image_info.caption.artist
    category = image_info.category
    new = category[3:] if category.startswith('by ') else None
    if old != new:
        image_info.caption.artist = new
        # print(f"[artist] `{logu.blue(image_info.key)}` `{logu.yellow(old)}` -> `{logu.green(new)}`.")
    return image_info


def track_characters(image_info: ImageInfo):
    characters = image_info.caption.get_characters()
    if image_info.caption.characters != characters:
        image_info.caption.characters = characters
        # print(f"[characters] `{logu.blue(image_info.key)}` `{logu.yellow(image_info.caption.characters)}` -> `{logu.green(characters)}`.")
    return image_info


def track_styles(image_info: ImageInfo):
    styles = image_info.caption.get_styles()
    if image_info.caption.styles != styles:
        image_info.caption.styles = styles
        # print(f"[styles] `{logu.blue(image_info.key)}` `{logu.yellow(image_info.caption.styles)}` -> `{logu.green(styles)}`.")
    return image_info


def track_everything(image_info: ImageInfo, dataset):
    image_info = track_image_path(image_info, dataset)
    image_info = track_caption(image_info, dataset)
    image_info = track_artist(image_info)
    image_info = track_characters(image_info)
    return image_info


def change_source(image_info: ImageInfo, new_src_name: str):
    old_src = image_info.source
    image_info.image_path = old_src.parent / new_src_name / image_info.image_path.relative_to(old_src)
    return image_info


def change_ext(image_info: ImageInfo, new_ext: str):
    old_ext = image_info.suffix
    image_info.image_path = image_info.image_path.with_suffix(new_ext)
    return image_info


def change_category(image_info: ImageInfo, new_category: str):
    old_category = image_info.category
    image_info.image_path = image_info.image_path.parent / new_category / image_info.image_path.name
    return image_info
