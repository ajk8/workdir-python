import os
import shutil
import dirsync
import logging
import copy
from contextlib import contextmanager
from ._version import __version__  # flake8: noqa

logger = logging.getLogger(__name__)


class _WorkdirOptions(object):
    def __init__(self):
        self._path = None
        self.debug = False
        self.sync_sourcedir = None
        self.sync_exclude_gitignore_entries = True
        self.sync_exclude_regex_list = []

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, abs_or_rel_path):
        self._path = os.path.abspath(abs_or_rel_path)


options = _WorkdirOptions()


def _set_log_level():
    """ Make sure that logging is respecting the debug setting """
    logger.setLevel(logging.DEBUG if options.debug else logging.INFO)


@contextmanager
def as_cwd():
    """ Use workdir.options.path as a temporary working directory """
    _set_log_level()
    owd = os.getcwd()
    logger.debug('entering working directory: ' + options.path)
    os.chdir(os.path.expanduser(options.path))
    yield
    logger.debug('returning to original directory: ' + owd)
    os.chdir(owd)


def _gitignore_entry_to_regex(entry):
    """ Take a path that you might find in a .gitignore file and turn it into a regex """
    ret = entry.strip()
    ret = ret.replace('.', '\.')
    ret = ret.replace('*', '.*')
    return ret


def sync(sourcedir=None, exclude_gitignore_entries=None, exclude_regex_list=None):
    """ Create and populate workdir.options.path, memoized so that it only runs once """
    _set_log_level()
    sourcedir = sourcedir or options.sync_sourcedir or os.getcwd()
    if exclude_gitignore_entries is None:
        exclude_gitignore_entries = options.sync_exclude_gitignore_entries
    exclude_regex_list = exclude_regex_list or copy.copy(options.sync_exclude_regex_list)
    gitignore_path = os.path.join(sourcedir, '.gitignore')
    if exclude_gitignore_entries and os.path.isfile(gitignore_path):
        gitignore_lines = []
        with open(gitignore_path) as gitignore:
            for line in gitignore.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    gitignore_lines.append(_gitignore_entry_to_regex(line))
        exclude_regex_list += gitignore_lines
    dirsync_logger = logging.getLogger('dirsync')
    dirsync_logger.setLevel(logging.INFO if options.debug else logging.FATAL)
    logger.info('syncing {} to {}'.format(sourcedir, options.path))
    logger.debug('excluding {} from sync'.format(exclude_regex_list))
    dirsync.sync(
        sourcedir=sourcedir,
        targetdir=options.path,
        action='sync',
        create=True,
        exclude=exclude_regex_list,
        logger=dirsync_logger
    )


def create():
    """ Create workdir.options.path """
    if not os.path.isdir(options.path):
        logger.info('creating working directory: ' + options.path)
        os.makedirs(options.path)


def clean():
    """ Remove all of the files contained in workdir.options.path """
    if os.path.isdir(options.path):
        logger.info('cleaning working directory: ' + options.path)
        for filename in os.listdir(options.path):
            filepath = os.path.join(options.path, filename)
            if os.path.isdir(filepath):
                shutil.rmtree(os.path.join(options.path, filename))
            else:
                os.remove(filepath)


def remove():
    """ Remove workdir.options.path """
    if os.path.isdir(options.path):
        logger.info('removing working directory: ' + options.path)
        shutil.rmtree(options.path)


def path_to_file(*subpath_parts):
    """ Return a path to a file located in workdir.options.path """
    return os.path.join(options.path, *subpath_parts)


def has_file(*subpath_parts):
    """ Find out whether a file exists in workdir.options.path """
    workdir_path = path_to_file(*subpath_parts)
    return os.path.exists(workdir_path)
