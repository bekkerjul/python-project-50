import argparse



def make_parser(gendiff):
    print(gendiff)
    parser = argparse.ArgumentParser(prog='gendiff',
                                     description='Compares two'
                                                 'configuration files '
                                                 'and shows a difference')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        help='set format of output', default='default')

    args = parser.parse_args()

    print(f'gendiff {args.first_file} {args.second_file} {args.format}')
    diff_result = gendiff(args.first_file, args.second_file, args.format)
    print(diff_result)
    return parser

