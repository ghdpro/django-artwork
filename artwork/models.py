"""django-artwork models"""

import logging
import subprocess
from pathlib import Path

from django.db import models
from django.utils.text import slugify

from .app_settings import FILENAME_MAX_LENGTH, IMAGE_MAX_SIZE, THUMB_SIZE, JPEG_QUALITY, THUMB_QUALITY

logger = logging.getLogger(__name__)


def artwork_upload_location(instance, filename):
    # Pattern: {MEDIA_ROOT}/{ARTWORK_FOLDER}/{instance.sub_folder()}/{filename}.jpg
    return str(Path(slugify(instance.ARTWORK_FOLDER), str(instance.sub_folder()).lower(),
                    slugify(Path(filename).stem[:FILENAME_MAX_LENGTH])).with_suffix('.jpg'))


def get_artwork_size(size) -> int:
    # Returns `width` aspect from size, regardless whether `size` is an int or a tuple
    if not isinstance(size, tuple):
        size = (size, size)
    return size[0]


def artwork_convert(image, dest: str, size, method: str = 'resize') -> bool:
    # Determine geometry and width
    if isinstance(size, int):
        geometry = f'{size}x{size}'
        width = size
    elif isinstance(size, tuple):
        geometry = f'{size[0]}x{size[1]}'
        width = size[0]
    else:  # Assume original image
        geometry = size
        width = image.width
    cmd = ['magick', 'convert', image.path + '[0]']  # Use only first frame for animated images (ie: GIFs)
    # Resize in "Lab" colorspace using Lanczos filter. See: http://www.imagemagick.org/Usage/resize/#resize_lab
    cmd += ['-colorspace', 'Lab', '-filter', 'Lanczos', f'-{method}', geometry, '-colorspace', 'sRGB']
    cmd += ['-strip']  # strip: remove profiles like EXIF (may contain sensitive GPS information)
    if width <= THUMB_SIZE:
        cmd += ['-unsharp', '0x.5', '-quality', str(THUMB_QUALITY)]
    else:
        cmd += ['-quality', str(JPEG_QUALITY)]
    cmd += [dest]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logger.error(f'Artwork: ImageMagick convert returned exit code '
                     f'{result.returncode}:\n {result.stderr.decode("utf-8")}')
        return False  # FAIL
    logger.info(f'Artwork: saved file "{dest}"')
    return True  # SUCCESS


class ArtworkModel(models.Model):
    image = models.ImageField(upload_to=artwork_upload_location)

    ARTWORK_FOLDER = 'artwork'
    ARTWORK_SIZES = (1200, )

    def __str__(self):
        return str(Path(self.image.path if hasattr(self.image, 'path') else self.image).name)

    def sub_folder(self):
        # Child classes need to override this function
        raise NotImplementedError

    def get_image_path(self, size) -> str:
        """Returns the (local) file path for the image"""
        return str(Path(Path(self.image.path).parent, Path(self.image.path).stem + f'-{get_artwork_size(size)}w.jpg'))

    def get_image_url(self, size) -> str:
        """Returns the URL for the image"""
        return str(Path(Path(self.image.url).parent, Path(self.image.url).stem + f'-{get_artwork_size(size)}w.jpg'))

    def get_image_src(self):
        """Returns the URL for the default image (for 'src' attribute)"""
        # Tip: override this function to return sizes other than the first entry in ARTWORK_SIZES
        return self.get_image_url(self.ARTWORK_SIZES[0])

    def get_image_srcset(self):
        """Returns a list of image URLs for the `srcset` attribute"""
        return ', '.join([f'{self.get_image_url(size)} {size}w' for size in self.ARTWORK_SIZES])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Force original uploaded image to comply to specified image dimensions (if set)
        if isinstance(IMAGE_MAX_SIZE, str):
            artwork_convert(self.image, self.image.path, IMAGE_MAX_SIZE)
        # Alternative image sizes
        if isinstance(self.ARTWORK_SIZES, tuple):
            for size in self.ARTWORK_SIZES:
                artwork_convert(self.image, self.get_image_path(size), size, 'thumbnail')

    class Meta:
        abstract = True
