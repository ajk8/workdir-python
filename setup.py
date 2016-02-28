from setuptools import setup
from imp import find_module, load_module

PROJECT_NAME = 'workdir'
GITHUB_USER = 'ajk8'
GITHUB_ROOT = 'https://github.com/{}/{}-python'.format(GITHUB_USER, PROJECT_NAME)

# pull in __version__ variable
found = find_module('_version', [PROJECT_NAME])
_version = load_module('_version', *found)


setup(
    name=PROJECT_NAME,
    version=_version.__version__,
    description='Simple module for easily isolating temporary file I/O',
    author='Adam Kaufman',
    author_email='kaufman.blue@gmail.com',
    url=GITHUB_ROOT,
    download_url='{}/tarball/{}'.format(GITHUB_ROOT, _version.__version__),
    license='MIT',
    packages=[PROJECT_NAME],
    install_requires=[
        'funcy>=1.4',
        'dirsync>=2.2.1',
        'six'  # this is required by dirsync, but not included there as a dependency
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='development workdir isolate temporary working directory'
)
