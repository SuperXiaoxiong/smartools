import argparse
import os
import subprocess
import common



from check_jar_md5 import *


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
    :param source_jar_file: the intput file with jar list
    :param destination_file: file will be decompile to destination_file/src
    :return:
    '''

    with open(source_jar_file, 'r') as f:
        for filename in f:
            filename = filename.strip()
            if '.jar' in filename or '.class' in filename:
                try:
                    excute_command(
                        'java -jar {} {} --outputdir {} '.format(common.CONFIG.get('decompile_cfr_tool'), filename, os.path.join(destination_file, "src")))

                except Exception as e:
                    print('error: {} in  {}'.format(e, filename))

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






def list_all_package(pathname, output):
    target_jar_list, target_jar_dir_list = common.get_target_jar_with_dir(pathname)
    print("共有包{}个".format(len(target_jar_list)))
    print("共有包路径{}个".format(len(target_jar_dir_list)))
    with open(os.path.join(output, "list_all_package"), 'w') as f_all:
        for item in target_jar_list:
            f_all.write(item)
            f_all.write("\n")

    print("the package list is set to {}".format(os.path.join(output, "list_all_package")))
    return target_jar_list, target_jar_dir_list


def list_all_class(pathname, output):

    with open(os.path.join(output, "list_all_class"), 'w') as f_all_class:
        for root, dirs, files in os.walk(pathname):
            # print('[+] {}'.format(root))

            for filename in files:
                # print('[+][+] {}'.format(os.path.join(root, filename)))
                if '.class' in filename:
                    f_all_class.write(os.path.join(root, filename))
                    f_all_class.write("\n")

    print("the class file list is set to {}".format(os.path.join(output, "list_all_class")))



def list_decompile_package(pathname, output):
    target_jar_list = []
    with open(os.path.join(output, "list_all_package"), 'r') as f_all:
        for line in f_all:
            target_jar_list.append(line.strip())

    decompile_list = []

    with open(os.path.join(output, "list_all_package_detail"), 'w') as f_detail:
        with open(os.path.join(output, "list_decompile_package"), 'w') as f_decompile:
            for filename in target_jar_list:
                checksum = mkhash(filename)
                try:
                    artifact = lookup(checksum)
                    if artifact:
                        f_detail.writelines(DEP_FMT.format(artifact['g'], artifact['a'], artifact['v']))
                        f_detail.write("\n")
                        f_detail.flush()
                    else:
                        decompile_list.append(filename)
                        f_decompile.write(filename)
                        f_decompile.write("\n")
                        f_decompile.flush()
                except Exception as e:
                    print('search {} occur error {}'.format(filename, e))


    print("the decompile file list is set to {}".format(os.path.join(output, "list_decompile_package")))

    return decompile_list




if __name__ == '__main__':
    common.config_path('/Users/admin/work/workspace/src/smartools/java_decompile/config.ini')

    parser = argparse.ArgumentParser()

    parser.add_argument("jarfile", help="input the jarfile string or the dir that include jarfile")
    parser.add_argument("output", help="input the output dir")
    parser.add_argument("-la", "--list_all_package", help="list all package")
    parser.add_argument("-ls", "--list_all_class", help="list all class")
    parser.add_argument("-lu", "--list_decompile_package", help="list decompile package")
    parser.add_argument("-d", "--decompile", help="list decompile package")

    args = parser.parse_args()

    '''
    outputdir/list_all_package 输出所有jar包列表
    outputdir/list_all_class 输出所有class包列表
    outputdir/list_all_package_detail 输出能够匹配到md5所有jar包的详细信息
    outputdir/list_decompile_package 输出不能匹配到md5 jar 包列表
    outputdir/src/ 输出反编译源码 
    '''

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    if not os.path.exists(os.path.join(args.outputdir, "src")):
        os.makedirs(os.path.join(args.outputdir, "src"))

    if args.list_all_package == '1':
        list_all_package(args.jarfile, args.output)

    if args.list_decompile_package == '1':
        list_decompile_package(args.jarfile, args.output)

    if args.decompile == '1':
        decompile_file(args.jarfile, args.output)


    # if not os.path.exists(args.outputdir):
    #     os.makedirs(args.outputdir)

    # decompile_file(args.jarfile, args.outputdir)