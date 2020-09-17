import argparse
import sys


def replace(args):
    pass


def delete(args):
    pass


def delete_lines(args):
    pass


def _add_common_args(parser):
    parser.add_argument('input-file', nargs='*')
    parser.add_argument('--in-place', '-i', action='store_true', default=False)


def main(args):
    parser = argparse.ArgumentParser(description='xed')
    subparsers = parser.add_subparsers(required=True, dest='command')

    replace_parser = subparsers.add_parser('replace', aliases=['r'])
    replace_parser.add_argument('regexp')
    replace_parser.add_argument('replacement')
    _add_common_args(replace_parser)
    replace_parser.set_defaults(func=replace)

    delete_parser = subparsers.add_parser('delete', aliases=['d'])
    delete_parser.add_argument('regexp')
    _add_common_args(delete_parser)
    delete_parser.set_defaults(func=delete)

    delete_lines_parser = subparsers.add_parser('delete-lines', aliases=['dl'])
    delete_lines_parser.add_argument('regexp')
    _add_common_args(delete_lines_parser)
    delete_lines_parser.set_defaults(func=delete_lines)

    args = parser.parse_args(args)
    args.func(args)


if __name__ == '__main__':
    main(sys.argv[1:])
