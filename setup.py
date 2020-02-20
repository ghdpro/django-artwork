from setuptools import setup, find_packages
from artwork import __version__


def read(file):
    with open(file, 'r') as f:
        return f.read()


setup(
    name='django-artwork',
    version='.'.join(str(x) for x in __version__),
    description='A package for the Django Framework that provides functionality for associating multiple images with a model',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    install_requires=[
        'django>=3',
        'Pillow>=7',
    ],
    python_requires='>=3.6',
    author='Gerard Krijgsman',
    author_email='python@visei.com',
    url='https://github.com/ghdpro/django-artwork',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
