import argparse
import csv
import os
import nist_mirror
import random
import time
import zipfile


import common
import static_analysis
from java_compile_cfr import list_all_package, list_all_class, list_decompile_package, decompile_file


# 关注的文件后缀
special_suffix = ['properties', 'xml', 'tld']
black_file_name = ['pom.xml']


def main(pathname, output_path):

    target_jar_list, target_jar_dir_list = list_all_package(pathname, output_path)
    list_all_class(pathname, output_path)

    # 开启镜像服务
    port_random = random.randint(50000, 59999)
    nist_mirror.start(port_random)
    print("开启nist镜像服务，端口{}".format(port_random))

    # 调用 dependency-check 进行检查
    result_check_name = os.path.join(output_path, 'dependency-check', 'dependency-check-' + str(int(time.time())) + '.html')
    target_jar_dir_str = ' -s '.join(target_jar_dir_list)
    dependency_check(target_jar_dir_str, result_check_name, port_random)
    print("完成dependency_check,输出文件 {}".format(result_check_name))

    decompile_list = list_decompile_package(pathname, output_path)

    print("开始处理特殊文件")
    for item in decompile_list:
        extract_special_file(item, output_path)


    print("开始反编译")
    input("请确认已经检查过所有需要反编译的jar包 {}".format( os.path.join(output_path, "list_decompile_package")))
    decompile_file(os.path.join(output_path, "list_decompile_package"), output_path)

    print("关闭nist镜像服务")
    nist_mirror.stop()

    print("开始进行静态代码分析")
    static_analysis.main(os.path.join(output_path, 'src'), output_path)

    print("完成所有流程")


def extract_special_file(filename, output_path):
    '''
    提取压缩包中的特殊文件，到指定位置
    :param filename:
    :return:
    '''
    output_file = []
    with zipfile.ZipFile(filename, 'r') as zf:
        for name in zf.namelist():
            filename = name.split(os.sep)[-1]
            try:
                if (filename.split('.')[-1] in special_suffix) and (filename not in black_file_name):
                    # print(os.path.join(filename, name))
                    output_file.append(name)
                    if not os.path.exists(os.path.join(output_path, 'special_file')):
                        os.makedirs(os.path.join(output_path, 'special_file'))
                    write_path = os.path.join(output_path, 'special_file')
                    zf.extract(name, write_path)
            except Exception as e:
                print(e)


def dependency_check(target_jar_dir_str, result_check_name, port_random):
    cmd = 'dependency-check -s {} -o {} --cveUrlModified http://127.0.0.1:{}/nvdcve-1.1-modified.json.gz    ' \
          '--cveUrlBase http://127.0.0.1:{}/nvdcve-1.1-%d.json.gz --disableRetireJS '.format(
        target_jar_dir_str, result_check_name, port_random, port_random)
    texts = os.popen(cmd).readlines()
    for line in texts:
        print(line)


def parse_dependency_check_csv(filename):
    '''
    获得所有的jar 包
    :param filename:
    :return:
    '''

    dependency_list = []
    jar_with_all_list = []
    result_list = []
    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for item in reader:
            dependency_list.append(item['DependencyPath'])

    # 去重
    dependency_list = list(set(dependency_list))

    for item in dependency_list:
        '''
            有一些特殊的集合包，需要提取jar包名 xfire-all-1.2.6.jar/META-INF/maven/org.codehaus.xfire/xfire-core/pom.xml
            '''
        if not item.endswith('.jar'):

            jar_with_all_list.append(item)
            jar_path = item.split('.jar{}'.format(os.sep))[0] + '.jar'
            result_list.append(jar_path)
            # print(jar_path)
        else:
            result_list.append(item)
            # print(item)

    return result_list


if __name__ == '__main__':
    '''
    1. 输出目录内的所有 jar 包/class文件 及目录
    2. dependency-check 检查所有的包并输出成html报告模式，不同路径带不同的文件后缀
    3. 获取所有非 maven md5 检出的
    //提取所有特定的xml 文件(路径名(/replace-)+包名) 到 output_path 下
    5. 暂停由用户确认反编译到 output_path 下
    :param pathname:
    :param output_path:
    :return:
    '''
    common.config_path('/Users/admin/work/workspace/src/smartools/java_decompile/config.ini')


    parser = argparse.ArgumentParser()

    parser.add_argument("jarfile", help="input the jarfile string or the dir that include jarfile")
    parser.add_argument("output", help="input the output dir")

    args = parser.parse_args()

    '''
    outputdir/list_all_package 输出所有jar包列表
    outputdir/list_all_class 输出所有class包列表
    outputdir/list_all_package_detail 输出能够匹配到md5所有jar包的详细信息
    outputdir/list_decompile_package 输出不能匹配到md5 jar 包列表
    outputdir/src/ 输出反编译源码 
    outputdir/dependency-check/ 输出反编译源码 
    '''

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if not os.path.exists(os.path.join(args.output, "src")):
        os.makedirs(os.path.join(args.output, "src"))

    if not os.path.exists(os.path.join(args.output, "dependency-check")):
        os.makedirs(os.path.join(args.output, "dependency-check"))

    main(args.jarfile, args.output)

