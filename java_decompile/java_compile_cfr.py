import argparse
import os
import zipfile
import subprocess
import configparser


CONFIG = {}
def excute_command(command):
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:
            print('Subprogram output: [{}]'.format(line))
    if p.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')


def decompile_file(source_jar_file, destination_file):
    '''
    :param source_jar_file: the intput jardir
    :param destination_file: out put location of decompile jar package(in ${destination_file}) and (java file in ${destination_file}/source_file)
    :return:
    '''


    if os.path.isdir(source_jar_file):
        for root, dirs, files in os.walk(source_jar_file):
        # print('[+] {}'.format(root))

            for filename in files:
                print('[+][+] {}'.format(os.path.join(root, filename)))

                if '.jar' in filename or '.class' in filename:
                    try:
                        excute_command(
                            'java -jar {} {} --outputdir {} '.format(CONFIG.get('decompile_cfr_tool'), os.path.join(root, filename), destination_file))

                    except Exception as e:
                        print('error: {} in  {}'.format(e, os.path.join(root, filename)))

    elif os.path.isfile(source_jar_file):
        excute_command(
            'java -jar {} {} --outputdir {} '.format(CONFIG.get('decompile_cfr_tool'), source_jar_file, destination_file))
    else:
        return

    '''
    for root, dirs, files in os.walk(destination_file):
        # print('[+] {}'.format(root))

        for filename in files:
            # print('[+][+] {}'.format(filename))
            # print(os.path.join(root, filename))

            if '.jar' in filename:
                try:
                    with zipfile.ZipFile(os.path.join(root, filename), 'r') as zzz:
                        zzz.extractall(path='{}'.format(os.path.join(destination_file, '_source_file')))
                except Exception as e:
                    print('error: {} in  {}'.format(e, os.path.join(root, filename)))
    '''

def config_path(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    global CONFIG

    CONFIG['decompile_tool'] = config.get('decompile_tool', 'location')
    CONFIG['decompile_cfr_tool'] = config.get('decompile_cfr_tool', 'location')
    decompile_options = config.options('decompile_options')
    CONFIG['decompile_options'] = {}
    for item in decompile_options:
        CONFIG['decompile_options'][item] = config.get('decompile_options', item)


config_path('/Users/admin/work/workspace/src/java_decompile/config.ini')

if __name__ == '__main__':
    # source_jar_file='/Users/admin/vulnerablity/weblogic/weblogic_patch_dir/p30729380_122140_Generic/122143'
    # destination_file = '/Users/admin/vulnerablity/weblogic/weblogic_patch_dir/p30729380_122140_Generic/source_code/'

    # /Users/admin/vulnerablity/weblogic/weblogic_patch_dir/p30970477_122140_Generic/30970477/files/ /Users/admin/vulnerablity/weblogic/weblogic_patch_dir/p30970477_122140_Generic/source_code_cfr/
    parser = argparse.ArgumentParser()

    # parser.add_argument("echo", help="echo the string you use here")
    parser.add_argument("jarfile", help="input the jarfile string or the dir that include jarfile")
    parser.add_argument("outputdir", help="input the output dir")
    args = parser.parse_args()
    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    decompile_file(args.jarfile, args.outputdir)