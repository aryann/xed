import argparse
import os
import re
import shutil
import sys
import tempfile
import textwrap

from typing import List

_RE_FLAGS = re.MULTILINE | re.DOTALL


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
                              data, flags=_RE_FLAGS))

    _handle_file_command(args, replace_one)


def _delete(args):

    def delete_one(read_fp, write_fp):
        data = read_fp.read()
        write_fp.write(re.sub(args.regexp, '', data, flags=_RE_FLAGS))

    _handle_file_command(args, delete_one)


def _handle_file_command(args, func):
    # TODO(aryann): Compile the regexp once.
    files = getattr(args, 'input-file')
    if not files:
        func(read_fp=sys.stdin, write_fp=sys.stdout)
        return

    for file_path in _filter_files(files):
        if args.in_place:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as write_fp, \
                    open(file_path) as read_fp:
                func(read_fp=read_fp, write_fp=write_fp)
            shutil.move(write_fp.name, file_path)
        else:
            with open(file_path) as f:
                func(read_fp=f, write_fp=sys.stdout)


def _search(args):
    files = getattr(args, 'input-file')
    regexp = re.compile(args.regexp, flags=_RE_FLAGS)
    matches = []
    for file in _filter_files(files):
        with open(file) as f:
            if regexp.search(f.read()):
                matches.append(file)
    if matches:
        sys.stdout.write('\n'.join(sorted(matches)))
        sys.stdout.write('\n')


def run(args):
    parser = argparse.ArgumentParser(description=textwrap.dedent("""\
        xed is a command-line tool for performing basic text transformations,
        modeled after the utility sed. xed provides an intuitive interface and
        supports multi-line regular expressions by default.

        For more information, visit https://xed.aryan.app.
        """))

    subparsers = parser.add_subparsers(required=True, dest='command')

    replace_parser = subparsers.add_parser(
        'replace', aliases=['r'],
        description=textwrap.dedent("""\
            Replace input text that matches a regular expression with a
            replacement text. The regular expression format follows the Python 3
            regular expression syntax
            (https://docs.python.org/3/library/re.html#regular-expression-syntax).
            The replacement text may contain references to capture groups.

            The input may either be a list of one or more file paths given as
            positional arguments or standard input if no files are provided. The
            output is written to standard out by default.
            """))
    replace_parser.add_argument(
        'regexp',
        help=textwrap.dedent("""\
            The regular expression. Any text matching this value will be
            replaced. The regular expression may contain newlines.
            """))
    replace_parser.add_argument(
        'replacement',
        help=textwrap.dedent("""\
            The replacement text. This value may contain capture group references.
        """))
    replace_parser.add_argument(
        'input-file', nargs='*',
        help=textwrap.dedent("""\
            Zero or more file paths that will be the subject of the replacement. If
            no files are provided, then the input is consumed from standard in.
            """))
    replace_parser.add_argument(
        '--in-place', '-i', action='store_true', default=False,
        help=textwrap.dedent("""\
            If provided and the input is a set of files, then the files are
            modified with the outcome and nothing is printed to standard out.
            """))
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
