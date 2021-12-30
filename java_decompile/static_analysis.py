import argparse
import os

import common
from java_compile_cfr import excute_command


def main(input_file, output_file):
    try:
        excute_command(
            'semgrep --config {} -o {} {}'.format(common.CONFIG.get('semgrep_rule'), os.path.join(output_file, "semgrep_output"), input_file))

    except Exception as e:
        print('error: {} in  {}'.format(e, input_file))
    print("已完成静态规则处理")


if __name__ == '__main__':
    common.config_path('/Users/admin/work/workspace/src/smartools/java_decompile/config.ini')

    parser = argparse.ArgumentParser()

    parser.add_argument("srcfile", help="input the srcfile dir")
    parser.add_argument("output", help="input the output dir")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    main(args.srcfile, args.output)