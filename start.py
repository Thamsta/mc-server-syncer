import os
import shutil
import time
import stat
import mc
from datetime import datetime

indent = '   '

CREATE = 0
EXTRACT = 1
NOTHING = 2


# delete
def check_mode():
    synced_timestamp_file = os.path.join(mc.sync_dir, mc.timestamp_file)
    if not os.path.exists(synced_timestamp_file):
        print('no synced timestamp file exists, server can be started', mc.sync_dir)
        return CREATE

    if not os.path.exists(mc.timestamp_file):
        print('no local timestamp file exists, using server from', mc.sync_dir)
        return EXTRACT

    fl = open(mc.timestamp_file, 'r')
    own_timestamp = float(fl.read())
    fl.close()

    fs = open(synced_timestamp_file)
    synced_timestamp = float(fs.read())
    fs.close()

    if own_timestamp == synced_timestamp:
        print('local timestamp is equal to synced timestamp, nothing to do')
        return NOTHING

    if own_timestamp > synced_timestamp:
        print('local timestamp is more recent than synced timestamp, nothing to do')
        return CREATE

    print('synced timestamp is more recent than local timestamp, overwriting local server')
    return EXTRACT


def delete_dir(ind, dir_to_delete):
    if os.path.exists(dir_to_delete):
        print(ind, 'deleting', dir_to_delete)
        mc.cleanup_dir(dir_to_delete)
        os.chmod(dir_to_delete, stat.S_IWRITE)
        os.rmdir(dir_to_delete)


def unzip_files():
    zipfile = [f for f in os.listdir(mc.sync_dir) if f.endswith('.zip')][0]
    shutil.copy(os.path.join(mc.sync_dir, zipfile), mc.tmp_dir)
    shutil.unpack_archive(os.path.join(mc.tmp_dir, zipfile), mc.tmp_dir)


def move_worlds():
    print(indent, 'moving worlds')
    for world in mc.worlds:
        delete_dir(indent + indent, world)
        print(indent + indent, 'moving world', world, 'into root')
        shutil.move(os.path.join(mc.tmp_dir, world), world)


def move_files():
    print(indent, 'moving files')
    files = [file for file in os.listdir(mc.tmp_dir) if (mc.is_file(os.path.join(mc.tmp_dir, file)) and mc.file_ending_is_ok(file))]
    for file in files:
        tmp_file = os.path.join(mc.tmp_dir, file)
        print(indent + indent, 'moving file', tmp_file, 'into root')
        shutil.copy2(tmp_file, os.getcwd())


def move_plugin_dirs():
    print(indent, 'moving plugins')
    source = os.path.join(mc.tmp_dir, mc.plugin_dir)
    plugins = [plugin for plugin in os.listdir(source) if
            (not mc.is_file(os.path.join(mc.plugin_dir, plugin)) and not plugin.endswith('dynmap'))]
    for plugin in plugins:
        plugin_source = os.path.join(source, plugin)
        plugin_target = os.path.join(mc.plugin_dir, plugin)
        delete_dir(indent + indent, plugin_target)
        print(indent + indent, 'moving plugin', plugin, 'from', plugin_source, 'into', plugin_target)
        shutil.copytree(plugin_source, plugin_target)


def move_all_files():
    move_worlds()
    move_files()
    move_plugin_dirs()


def create_timestamp_file():
    print("creating new timestamp file")
    timestamp = time.time()
    f = open(mc.timestamp_file, 'w')
    f.write(str(timestamp))
    f.close()


def find_spigot_server():
    return [file for file in os.listdir() if file.endswith('jar') and file.startswith('spigot-')][0]


if __name__ == '__main__':
    mode = check_mode()
    if mode == EXTRACT:
        print('The local server will now be overridden with the synced server.')
        inp = input('Continue? (Y/n)\n')
        if inp != 'Y':
            print('Aborting..')
            exit()
        print('Continuing..')
        mc.cleanup_tmp_dir()
        unzip_files()
        move_all_files()
        delete_dir('', mc.tmp_dir)
    create_timestamp_file()
    server_name = find_spigot_server()
    print('starting spigot server', server_name)
    os.system('java -jar ' + server_name)
