import argparse
import os
from java_compile_cfr import decompile_file


def extract_patch_file(patchfile, rawfile):

    patchfile_class_lists = []
    patchfile_jar_lists = []
    for root, dirs, files in os.walk(patchfile):
        # print('[+] {}'.format(root))

        for filename in files:
            if '.jar' in filename or '.jar' in root:
                # print('[+][+] {}'.format(os.path.join(root, filename)))
                temp_filename_lists = root.split(os.sep)

                for temp_filename in temp_filename_lists:
                    if ".jar" in temp_filename:
                        patchfile_jar_lists.append(temp_filename)
                        # print('[+][+] {}'.format(temp_filename))

            elif '.class' in filename:
                # print('[-][-] {}'.format(os.path.join(root, filename)))
                patchfile_class_lists.append(filename)

    patchfile_jar_lists = list(set(patchfile_jar_lists))
    print(patchfile_jar_lists)
    print(patchfile_class_lists)

    patch_old_jar_lists = []

    for root, dirs, files in os.walk(rawfile):
        # print('[+] {}'.format(root))

        for filename in files:
            if filename in patchfile_class_lists:
                print('[-][-] {}'.format(os.path.join(root, filename)))
            elif filename in patchfile_jar_lists:
                print('[+][+] {}'.format(os.path.join(root, filename)))
                patch_old_jar_lists.append(os.path.join(root, filename))

    if not os.path.exists(os.path.join(patchfile, 'old_patch_file')):
        os.makedirs(os.path.join(patchfile, 'old_patch_file'))

    for item in patch_old_jar_lists:
        decompile_file(item, os.path.join(patchfile, '../', 'old_patch_file'))


if __name__ == '__main__':
    # source_jar_file='/Users/admin/vulnerablity/weblogic/weblogic_patch_dir/p30729380_122140_Generic/122143'
    # destination_file = '/Users/admin/vulnerablity/weblogic/weblogic_patch_dir/p30729380_122140_Generic/source_code/'

    # /Users/admin/vulnerablity/weblogic/weblogic_patch_dir/p31537019_122140_Generic/31537019/ /Users/admin/vulnerablity/weblogic/project/weblogic122104_raw/
    parser = argparse.ArgumentParser()

    # parser.add_argument("echo", help="echo the string you use here")
    parser.add_argument("patchfile", help="input patchfile")
    parser.add_argument("rawfile", help="input the compare rawfile")
    args = parser.parse_args()

    extract_patch_file(args.patchfile, args.rawfile)