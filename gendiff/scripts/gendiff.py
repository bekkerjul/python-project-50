import argparse


def main():
    parser = argparse.AgrumentParser(prog='gendiff', description = 'Compares two configuration files and shows a difference')
    parser.add_argument('first_file')
    parser.add_argument('second_file')

    args = parser.parse_args()

    print(f'Comparing files: {args.first_file} and {args.second_file}')


if __name__ == '__main__':
    main()