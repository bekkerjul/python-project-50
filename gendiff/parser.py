import argparse


def make_parser(format):
    parser = argparse.ArgumentParser(prog='gendiff',
                                     description='Compares two'
                                                 'configuration files '
                                                 'and shows a difference')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        help='set format of output', default='default')

    args = parser.parse_args()

    print(f'gendiff {args.first_file} {args.second_file}')
    diff_result = format(args.first_file, args.second_file)
    print(diff_result)
