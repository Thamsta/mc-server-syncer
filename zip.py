import os
import shutil
import time
import mc
from datetime import datetime

indent = '   '


def copy_all():
    print('copying worlds and files into', mc.tmp_dir)
    copy_worlds()
    copy_files()
    copy_plugin_files()


def copy_worlds():
    for world in mc.worlds:
        dst = os.path.join(mc.tmp_dir, world)
        print(indent, 'copying directory', world, 'into', dst)
        shutil.copytree(world, dst)


def copy_files():
    files = [file for file in os.listdir() if (mc.is_file(file) and mc.file_ending_is_ok(file))]
    for file in files:
        print(indent, 'copying file', file, 'into', mc.tmp_dir)
        shutil.copy2(file, mc.tmp_dir)


def copy_plugin_files():
    dirs = [plugin for plugin in os.listdir(mc.plugin_dir) if
            (not mc.is_file(os.path.join(mc.plugin_dir, plugin)) and not plugin.endswith('dynmap'))]
    target = os.path.join(mc.tmp_dir, mc.plugin_dir)
    os.mkdir(target)
    for plugin in dirs:
        plugin_source = os.path.join(mc.plugin_dir, plugin)
        plugin_target = os.path.join(target, plugin)
        print(indent, 'copying plugin directory', plugin_source, 'into', plugin_target)
        shutil.copytree(plugin_source, plugin_target)


def zip_folder():
    filename = 'server_v' + datetime.today().strftime('%Y%m%d')
    print('zipping', mc.tmp_dir, 'as', filename)
    shutil.make_archive(filename, 'zip', mc.tmp_dir)

    full_filename = filename + '.zip'
    dst = mc.sync_dir + os.sep + full_filename
    print('moving', full_filename, 'into', dst)
    if not os.path.exists(mc.sync_dir):
        print(dst, 'does not exist, creating directory')
        os.mkdir(mc.sync_dir)
    shutil.move(full_filename, mc.sync_dir + os.sep + full_filename)


def move_timestamp_file():
    shutil.copy(mc.timestamp_file, mc.sync_dir)


if __name__ == '__main__':
    mc.cleanup_tmp_dir()
    mc.cleanup_dir(mc.sync_dir)
    copy_all()
    zip_folder()
    mc.delete_tmp_dir()
    move_timestamp_file()
