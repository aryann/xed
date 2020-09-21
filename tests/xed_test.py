import collections
import contextlib
import io
import os
import tempfile
import textwrap
import unittest

from typing import List

import xed


ModifyTest = collections.namedtuple('ModifyTest', ['initial', 'expected'])
SearchTest = collections.namedtuple('SearchTest', ['content', 'matches'])


class XedTest(unittest.TestCase):

    def run_test_with_files(self, command: List[str], *files: ModifyTest):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as temp_dir, \
                contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            file_paths: List[str] = []
            for i, file in enumerate(files):
                file_paths.append(os.path.join(temp_dir, str(i)))
                with open(file_paths[-1], 'w') as f:
                    f.write(textwrap.dedent(file.initial))

            xed.run(command + file_paths)

            for file, file_path in zip(files, file_paths):
                with open(file_path) as f:
                    actual = f.read()
                self.assertEqual(actual, textwrap.dedent(file.expected))
        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(stderr.getvalue(), '')

    def test_replace(self):
        self.run_test_with_files(
            ['replace', '--in-place', 'a', 'b'],
            ModifyTest(initial='a', expected='b'))
        self.run_test_with_files(
            ['replace', '--in-place', 'a', 'b'],
            ModifyTest(initial='abcabcabc', expected='bbcbbcbbc'))
        self.run_test_with_files(
            ['replace', '--in-place', 'a', 'b'],
            ModifyTest(initial='ccc', expected='ccc'))
        self.run_test_with_files(
            ['replace', '--in-place', '.', 'b'],
            ModifyTest(initial='abcdefg', expected='bbbbbbb'))
        self.run_test_with_files(
            ['replace', '--in-place', 'abc', 'xyz'],
            ModifyTest(initial="""\
                    hello
                    abc
                    world
                    gggabchhh
                    abcggg
                    hhhabc
                    abc
                    """,
                       expected="""\
                    hello
                    xyz
                    world
                    gggxyzhhh
                    xyzggg
                    hhhxyz
                    xyz
                    """))
        self.run_test_with_files(
            ['replace', '--in-place', 'a(.)c', r'x\1y'],
            ModifyTest(initial="""\
                    abc
                    aac
                    acc
                    """,
                       expected="""\
                    xby
                    xay
                    xcy
                    """))
        self.run_test_with_files(
            ['replace', '--in-place', r'abc\nxyz', 'ZZZ'],
            ModifyTest(initial="""\
                    hello
                    abc
                    xyz
                    world
                    """,
                       expected="""\
                    hello
                    ZZZ
                    world
                    """))
        self.run_test_with_files(
            ['replace', '--in-place', 'non-existent-pattern', 'aaa'],
            ModifyTest(initial="""\
                    hello
                    world
                    """,
                       expected="""\
                    hello
                    world
                    """))
        self.run_test_with_files(
            ['replace', '--in-place', '^aaa(\w+)', r'\1'],
            ModifyTest(initial="""\
                    hello
                    aaa
                    aaaworld
                    aaagoodbye
                    aaa123
                    aaworld
                    """,
                       expected="""\
                    hello
                    aaa
                    world
                    goodbye
                    123
                    aaworld
                    """))

    def run_search_test(self,  command: List[str], *files: SearchTest):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as temp_dir, \
                contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            file_paths: List[str] = []
            expected_matches: List[str] = []
            for i, file in enumerate(files):
                file_paths.append(os.path.join(temp_dir, str(i)))
                with open(file_paths[-1], 'w') as f:
                    f.write(textwrap.dedent(file.content))
                if file.matches:
                    expected_matches.append(file_paths[-1])

            xed.run(command + file_paths)

        self.assertEqual(stdout.getvalue(), '\n'.join(
            sorted(expected_matches)) + '\n')
        self.assertEqual(stderr.getvalue(), '')

    def test_search(self):
        self.run_search_test(
            ['search', 'a'],
            SearchTest(content='aaaa', matches=True))
        self.run_search_test(
            ['search', 'b'],
            SearchTest(content='aaaa', matches=False))
        self.run_search_test(
            ['search', 'a'],
            SearchTest(content='aaaa', matches=True),
            SearchTest(content='bbbb', matches=False),
            SearchTest(content='abc', matches=True))
        self.run_search_test(
            ['search', 'hello'],
            SearchTest(content="""\
                aaa
                hello
                bbb
                """, matches=True))
        self.run_search_test(
            ['search', r'bb\ncc'],
            SearchTest(content="""\
                aaa
                bbb
                ccc
                ddd
                """, matches=True))


if __name__ == '__main__':
    unittest.main()
