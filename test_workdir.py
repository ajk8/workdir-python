import os
import workdir
import logging


def test__set_log_level():
    workdir.options.debug = True
    workdir._set_log_level()
    assert workdir.logger.getEffectiveLevel() == logging.DEBUG
    workdir.options.debug = False
    workdir._set_log_level()
    assert workdir.logger.getEffectiveLevel() == logging.INFO


def test_as_cwd(tmpdir):
    with tmpdir.as_cwd():
        workdir.options.path = 'test_as_cwd'
        os.mkdir(workdir.options.path)
        with workdir.as_cwd():
            assert os.getcwd() == os.path.join(str(tmpdir), workdir.options.path)
        assert os.getcwd() == str(tmpdir)


def test__gitignore_entry_to_regex():
    assert workdir._gitignore_entry_to_regex('__pycache__') == r'__pycache__'
    assert workdir._gitignore_entry_to_regex('*.pyc') == r'.*\.pyc'


def _setup_gitignore_test():
    open('module.py', 'w').close()
    open('module.pyc', 'w').close()
    with open('.gitignore', 'w') as gitignore:
        gitignore.write('*.pyc')


def test_sync_with_gitignore(tmpdir):
    with tmpdir.as_cwd():
        _setup_gitignore_test()
        workdir.options.path = 'test_sync_with_gitignore'
        assert not os.path.exists(workdir.options.path)
        workdir.sync()
        assert os.path.isfile(os.path.join(workdir.options.path, 'module.py'))
        assert not os.path.exists(os.path.join(workdir.options.path, 'module.pyc'))


def test_sync_without_gitignore(tmpdir):
    with tmpdir.as_cwd():
        _setup_gitignore_test()
        workdir.options.path = 'test_sync_without_gitignore'
        assert not os.path.exists(workdir.options.path)
        workdir.sync(exclude_gitignore_entries=False)
        assert os.path.isfile(os.path.join(workdir.options.path, 'module.py'))
        assert os.path.isfile(os.path.join(workdir.options.path, 'module.pyc'))


def test_create(tmpdir):
    with tmpdir.as_cwd():
        workdir.options.path = 'test_create'
        assert not os.path.exists(workdir.options.path)
        workdir.create()
        assert os.path.exists(workdir.options.path)


def test_clean(tmpdir):
    with tmpdir.as_cwd():
        workdir.options.path = 'test_clean'
        workdir.create()
        touchfile = os.path.join(workdir.options.path, 'touchfile')
        touchdir = os.path.join(workdir.options.path, 'touchdir')
        open(touchfile, 'w').close()
        os.mkdir(touchdir)
        assert os.path.isfile(touchfile)
        assert os.path.isdir(touchdir)
        workdir.clean()
        assert not os.path.exists(touchfile)
        assert os.path.isdir(workdir.options.path)


def test_remove(tmpdir):
    with tmpdir.as_cwd():
        workdir.options.path = 'test_remove'
        os.mkdir(workdir.options.path)
        workdir.remove()
        assert not os.path.exists(workdir.options.path)


def test_path_to_file():
    workdir.options.path = 'test_path_to_file'
    assert workdir.path_to_file('myfile') == os.path.join('test_path_to_file', 'myfile')
    assert workdir.path_to_file('mydir', 'myfile') == os.path.join(
        'test_path_to_file', 'mydir', 'myfile'
    )


def test_has_file(tmpdir):
    with tmpdir.as_cwd():
        workdir.options.path = 'test_has_file'
        workdir.create()
        with workdir.as_cwd():
            open('myfile', 'w').close()
        assert workdir.has_file('myfile') is True
        assert workdir.has_file('notthere') is False
