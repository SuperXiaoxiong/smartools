import configparser
import os

CONFIG = {}


def config_path(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    global CONFIG

    CONFIG['decompile_tool'] = config.get('decompile_tool', 'location')
    CONFIG['decompile_cfr_tool'] = config.get('decompile_cfr_tool', 'location')
    CONFIG['semgrep_rule'] = config.get('semgrep_rule', 'location')
    decompile_options = config.options('decompile_options')
    CONFIG['decompile_options'] = {}
    for item in decompile_options:
        CONFIG['decompile_options'][item] = config.get('decompile_options', item)

    CONFIG['nist_data_mirror'] = config.get('nist_data_mirror', 'repository')


def get_target_jar(pathname):
    '''
    递归获取目录下所有jar包
    :param pathname:
    :return:
    '''

    target_jar = []

    for root, dirs, files in os.walk(pathname):
        for filename in files:
            if '.jar' in filename:
                target_jar.append(os.path.join(root, filename))

    return list(set(target_jar))


def get_target_jar_with_dir(pathname):
    '''
    递归获取目录下所有jar包和所有的目录
    :param pathname:
    :return:
    '''
    target_jar = []
    target_jar_dir = []
    for root, dirs, files in os.walk(pathname):
        for filename in files:
            if ('.jar' in filename):
                target_jar.append(os.path.join(root, filename))
                target_jar_dir.append(root)

    return list(set(target_jar)), list(set(target_jar_dir))


