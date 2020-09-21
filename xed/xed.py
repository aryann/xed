import argparse
import io
import os
import re
import sys

from typing import List


def _filter_files(files: List[str]):
    """Selects regular files from the given list."""
    for file in sorted(files):
        if not os.path.isfile(file):
            sys.stderr.write(f'{file}: not a regular file')
            sys.stderr.write('\n')
            continue
        yield file


def _replace(args):

    def replace_one(read_fp, write_fp):
        data = read_fp.read()
        write_fp.write(re.sub(args.regexp, args.replacement,
                              data, flags=re.MULTILINE))

    _handle_file_command(args, replace_one)


def _delete(args):

    def delete_one(read_fp, write_fp):
        data = read_fp.read()
        write_fp.write(re.sub(args.regexp, '', data, flags=re.MULTILINE))

    _handle_file_command(args, delete_one)


def _handle_file_command(args, func):
    # TODO(aryann): Compile the regexp once.
    files = getattr(args, 'input-file')
    if not files:
        func(read_fp=sys.stdin, write_fp=sys.stdout)
        return

    for file_path in _filter_files(files):
        if args.in_place:
            # TODO(aryann): Instead of writing the results into an in-memory
            # buffer, consider writing the results to a temporary file as the
            # input is being processed and swapping the temporary file with the
            # input.
            result = io.StringIO()
            with open(file_path) as f:
                func(read_fp=f, write_fp=result)
            with open(file_path, 'w') as f:
                f.write(result.getvalue())
        else:
            with open(file_path) as f:
                func(read_fp=f, write_fp=sys.stdout)


def _search(args):
    files = getattr(args, 'input-file')
    regexp = re.compile(args.regexp, flags=re.MULTILINE)
    matches = []
    for file in _filter_files(files):
        with open(file) as f:
            if regexp.search(f.read()):
                matches.append(file)
    if matches:
        sys.stdout.write('\n'.join(sorted(matches)))
        sys.stdout.write('\n')


def run(args):
    parser = argparse.ArgumentParser(description='xed')
    subparsers = parser.add_subparsers(required=True, dest='command')

    replace_parser = subparsers.add_parser('replace', aliases=['r'])
    replace_parser.add_argument('regexp')
    replace_parser.add_argument('replacement')
    replace_parser.add_argument('input-file', nargs='*')
    replace_parser.add_argument(
        '--in-place', '-i', action='store_true', default=False)
    replace_parser.set_defaults(func=_replace)

    delete_parser = subparsers.add_parser('delete', aliases=['d'])
    delete_parser.add_argument('regexp')
    delete_parser.add_argument('input-file', nargs='*')
    delete_parser.add_argument(
        '--in-place', '-i', action='store_true', default=False)
    delete_parser.set_defaults(func=_delete)

    search_parser = subparsers.add_parser('search', aliases=['s'])
    search_parser.add_argument('regexp')
    search_parser.add_argument('input-file', nargs='*')
    search_parser.set_defaults(func=_search)

    args = parser.parse_args(args)
    args.func(args)


def cli() -> int:
    try:
        run(sys.argv[1:])
        return 0
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(cli())
