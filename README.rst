django-artwork
==============

django-artwork is a Django app that provides "artwork" support to your Django models.

Imagine the following problem: you have a model that has an ImageField which stores
artwork for that model (like for example in the case of a book: the cover). Now let's
assume multiple people have access to uploading images and replacing existing images.
Now imagine someone uploads new artwork (image) for an existing entry where you are
not happy with how that image looks. It may be low resolution, badly edited, or just
the wrong kind of image altogether. To get the original image back you better hope
you have backups! The original image might be gone (deleted/replaced) or you have to
search the file system for it.

Purpose
-------

django-artwork hopes to address that problem by providing a convenient way to upload
multiple images for every entry in your main model, and a way to pick a "main" image.

And in addition to that, the code will also generate alternative sizes for every image
uploaded to enable *responsive images* support for your site.

Notes
-----

At the moment this package is rather simple, in the sense that it doesn't support any
storage system other than local filesystem storage, and also performs the generation of
alternative image sizes during the response phase (meaning: if this process takes a while,
the site will seem to load very slow for the user).

Support for the former (alternative storage systems) may be added in the future if there
is demand for it, but solving the second issue seems difficult without resorting to using
Celery and ballooning the scope of the project.