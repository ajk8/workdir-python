from setuptools import setup

PROJECT_NAME = 'workdir'
GITHUB_USER = 'ajk8'
GITHUB_ROOT = 'https://github.com/{}/{}-python'.format(GITHUB_USER, PROJECT_NAME)

# pull in __version__ variable
with open('{}/_version.py'.format(PROJECT_NAME)) as f:
    exec(f.read())


setup(
    name=PROJECT_NAME,
    version=__version__,
    description='Simple module for easily isolating temporary file I/O',
    author='Adam Kaufman',
    author_email='kaufman.blue@gmail.com',
    url=GITHUB_ROOT,
    download_url='{}/tarball/{}'.format(GITHUB_ROOT, __version__),
    license='MIT',
    packages=[PROJECT_NAME],
    install_requires=[
        'funcy==1.7',
        'dirsync==2.1',
        'six==1.10.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development'
    ],
    keywords='development'
)
