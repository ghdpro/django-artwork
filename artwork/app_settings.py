"""django-artwork settings"""

from django.conf import settings

# Maximum length of the "stem" part of the image filename
FILENAME_MAX_LENGTH = getattr(settings, 'ARTWORK_FILENAME_MAX_LENGTH', 50)

# Maximum image dimensions. See: https://imagemagick.org/script/command-line-processing.php#geometry
# If set but not a string (like False or None), then the original uploaded image will not be altered in any way
IMAGE_MAX_SIZE = getattr(settings, 'ARTWORK_IMAGE_MAX_SIZE', '2048x2048>')

# Images with width smaller than this size will be considered thumbnails
THUMB_SIZE = getattr(settings, 'ARTWORK_THUMB_SIZE', 200)

# JPEG Quality for images (larger than thumbnails)
JPEG_QUALITY = getattr(settings, 'ARTWORK_JPEG_QUALITY', 85)

# JPEG Quality for thumbnails
THUMB_QUALITY = getattr(settings, 'ARTWORK_THUMB_QUALITY', 80)
