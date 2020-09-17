import argparse
import re
import sys


def _replace(args, read_fp, write_fp):
    data = read_fp.read()
    write_fp.write(re.sub(args.regexp, args.replacement, data))


def _delete(args, read_fp, write_fp):
    data = read_fp.read()
    write_fp.write(re.sub(args.regexp, '', data))


def _delete_lines(args, read_fp, write_fp):
    regexp = re.compile(args.regexp)
    while True:
        line = read_fp.readline()
        if not line:
            break
        if not regexp.search(line):
            write_fp.write(line)


def _handle_command(args, func):
    files = getattr(args, 'input-file')
    if not files:
        func(args, read_fp=sys.stdin, write_fp=sys.stdout)
        return

    for file_path in files:
        with open(file_path) as f:
            func(args, read_fp=f, write_fp=sys.stdout)


def _add_common_args(parser):
    parser.add_argument('input-file', nargs='*')
    parser.add_argument('--in-place', '-i', action='store_true', default=False)


def run(args):
    parser = argparse.ArgumentParser(description='xed')
    subparsers = parser.add_subparsers(required=True, dest='command')

    replace_parser = subparsers.add_parser('replace', aliases=['r'])
    replace_parser.add_argument('regexp')
    replace_parser.add_argument('replacement')
    _add_common_args(replace_parser)
    replace_parser.set_defaults(func=_replace)

    delete_parser = subparsers.add_parser('delete', aliases=['d'])
    delete_parser.add_argument('regexp')
    _add_common_args(delete_parser)
    delete_parser.set_defaults(func=_delete)

    delete_lines_parser = subparsers.add_parser('delete-lines', aliases=['dl'])
    delete_lines_parser.add_argument('regexp')
    _add_common_args(delete_lines_parser)
    delete_lines_parser.set_defaults(func=_delete_lines)

    args = parser.parse_args(args)
    _handle_command(args, func=args.func)


def cli() -> int:
    try:
        run(sys.argv[1:])
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(cli())
