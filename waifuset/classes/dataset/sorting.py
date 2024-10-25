from .. import ImageInfo


def key(image_info: ImageInfo):
    return image_info.key


def stem(image_info: ImageInfo):
    return image_info.stem


def extension(image_info: ImageInfo):
    return image_info.image_path.suffix


def category(image_info: ImageInfo):
    return image_info.category


# def perceptual_hash(image_info: ImageInfo, target=None):
#     if image_info.perceptual_hash is None or target is None:
#         return float('inf')
#     import imagehash
#     if isinstance(target, str):
#         target = imagehash.hex_to_hash(target)
#     return imagehash.hex_to_hash(image_info.perceptual_hash) - target


import imagehash
from typing import List, Optional
from PIL import Image
from pathlib import Path

def calculate_hash(img_path: Path, highfreq_factor: int = 4, hash_size: int = 32, image_scale: int = 64) -> List[imagehash.ImageHash]:
    """计算图像的多种哈希值"""
    img_Image = Image.open(img_path)
    img_phash = imagehash.phash(img_Image, hash_size=hash_size, highfreq_factor=highfreq_factor)
    img_ahash = imagehash.average_hash(img_Image, hash_size=hash_size)
    img_dhash = imagehash.dhash(img_Image, hash_size=hash_size)
    img_whash = imagehash.whash(img_Image, image_scale=image_scale, hash_size=hash_size, mode='db4')
    return [img_phash, img_ahash, img_dhash, img_whash]

def compare_hash(list_imgalpha: List[imagehash.ImageHash], list_imgbeta: List[imagehash.ImageHash]) -> float:
    """计算两个图像之间的相似度"""
    # 计算每种哈希值的相似度分数
    phash_value = 1 - (list_imgalpha[0] - list_imgbeta[0]) / len(list_imgalpha[0].hash) ** 2
    ahash_value = 1 - (list_imgalpha[1] - list_imgbeta[1]) / len(list_imgalpha[1].hash) ** 2
    dhash_value = 1 - (list_imgalpha[2] - list_imgbeta[2]) / len(list_imgalpha[2].hash) ** 2
    whash_value = 1 - (list_imgalpha[3] - list_imgbeta[3]) / len(list_imgalpha[3].hash) ** 2
    # 返回最大相似度分数
    return max(phash_value, ahash_value, dhash_value, whash_value)

def perceptual_hash(image_info: ImageInfo, target: Optional[ImageInfo] = None) -> float:
    """计算两个图像之间的相似度"""
    if not image_info.perceptual_hash or not target:
        return float('inf')

    # 提供了图像路径，则计算哈希值；如果提供了哈希值，则直接使用
    if image_info.image_path:
        current_hash = calculate_hash(image_info.image_path)
    else:
        # image_info.perceptual_hash 是一个包含四种哈希的列表
        current_hash = [imagehash.hex_to_hash(hash_value) for hash_value in image_info.perceptual_hash.split(',')]

    if isinstance(target, ImageInfo):
        if target.image_path:
            target_hash = calculate_hash(target.image_path)
        else:
            target_hash = [imagehash.hex_to_hash(hash_value) for hash_value in target.perceptual_hash.split(',')]
    else:
        return float('inf')  # target既不是ImageInfo对象也不是哈希值，则返回无穷大

    # 计算相似度
    similarity_value = compare_hash(current_hash, target_hash)
    
    return similarity_value


def aesthetic_score(image_info: ImageInfo):
    if image_info.aesthetic_score is None:
        return -float('inf')
    return image_info.aesthetic_score


def original_size(image_info: ImageInfo):
    if image_info.original_size is None:
        return -float('inf')
    width, height = image_info.original_size
    return width * height


def original_width(image_info: ImageInfo):
    if image_info.original_size is None:
        return -float('inf')
    width, height = image_info.original_size
    return width


def original_height(image_info: ImageInfo):
    if image_info.original_size is None:
        return -float('inf')
    width, height = image_info.original_size
    return height


def original_aspect_ratio(image_info: ImageInfo):
    if image_info.original_size is None:
        return -float('inf')
    width, height = image_info.original_size
    return width / height


def caption_length(image_info: ImageInfo):
    if image_info.caption is None:
        return -float('inf')
    return len(image_info.caption)


def has_gen_info(image_info: ImageInfo):
    return len(image_info.gen_info) > 0


def quality(image_info: ImageInfo):
    if image_info.caption is None:
        quality_ = 'normal'
    else:
        quality_ = image_info.caption.quality or 'normal'
    return {
        'horrible': 0,
        'worst': 2,
        'low': 3.5,
        'normal': 5,
        'high': 6.5,
        'best': 8,
        'amazing': 10,
    }.get(quality_, 5)


def quality_or_score(image_info: ImageInfo):
    if image_info.aesthetic_score is not None:
        return aesthetic_score(image_info)
    else:
        return quality(image_info)


def random(image_info: ImageInfo):
    import random
    return random.random()


def safe_rating(image_info: ImageInfo):
    return image_info.safe_rating


LEVEL2KEY = {
    'g': 0,
    's': 1,
    'q': 2,
    'e': 3,
}


def safe_level(image_info: ImageInfo):
    lvl = image_info.safe_level
    return LEVEL2KEY.get(lvl, len(LEVEL2KEY))
