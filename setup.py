from distutils.core import setup
from pywebfinger import __version__

long_description = open('README.rst').read()

setup(name="python-webfinger",
    version=str(__version__),
    py_modules=["pywebfinger"],
    description="Simple Python implementation of webfinger client protocol",
    author="Jeremy Carbaugh",
    author_email = "jcarbaugh@gmail.com",
    license='BSD',
    url="http://github.com/jcarbaugh/python-webfinger/",
    long_description=long_description,
    install_requires=["python-xrd"],
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
