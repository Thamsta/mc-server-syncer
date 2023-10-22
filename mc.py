import os
import stat


tmp_dir = '.tmp'
sync_dir = '.sync'
plugin_dir = 'plugins'
worlds = ['world', 'world_nether', 'world_the_end']
ignored_file_endings = ['.jar', '.zip', '.py', '.timestamp']
timestamp_file = 'last_server_startup.timestamp'


def make_dir_accessible(target):
    for f in os.listdir(target):
        fullname = os.path.join(target, f)
        os.chmod(fullname, stat.S_IWRITE)
        if os.path.isdir(fullname):
            cleanup_dir(fullname)


def cleanup_dir(target):
    for f in os.listdir(target):
        fullname = os.path.join(target, f)
        os.chmod(fullname, stat.S_IWRITE)
        if os.path.isfile(fullname):
            os.remove(fullname)
        if os.path.isdir(fullname):
            cleanup_dir(fullname)
            os.rmdir(fullname)


def delete_tmp_dir():
    if os.path.exists(tmp_dir):
        print('deleting tmp dir...')
        cleanup_dir(tmp_dir)
        os.chmod(tmp_dir, stat.S_IWRITE)
        os.rmdir(tmp_dir)


def cleanup_tmp_dir():
    delete_tmp_dir()
    print('creating tmp dir...')
    os.mkdir(tmp_dir)


def file_ending_is_ok(file):
    for ending in ignored_file_endings:
        if file.endswith(ending):
            return False

    return True


def is_file(file):
    return os.path.isfile(file)