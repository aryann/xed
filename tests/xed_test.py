import collections
import os
import tempfile
import textwrap
import unittest

from typing import List

import xed


File = collections.namedtuple('File', ['initial', 'expected'])


class XedTest(unittest.TestCase):

    def run_test_with_files(self, command: List[str], *files: File):
        with tempfile.TemporaryDirectory() as temp_dir:
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

    def testReplace(self):
        self.run_test_with_files(
            ['replace', '--in-place', 'a', 'b'],
            File(initial='a', expected='b'))
        self.run_test_with_files(
            ['replace', '--in-place', 'a', 'b'],
            File(initial='abcabcabc', expected='bbcbbcbbc'))
        self.run_test_with_files(
            ['replace', '--in-place', 'a', 'b'],
            File(initial='ccc', expected='ccc'))
        self.run_test_with_files(
            ['replace', '--in-place', '.', 'b'],
            File(initial='abcdefg', expected='bbbbbbb'))
        self.run_test_with_files(
            ['replace', '--in-place', 'abc', 'xyz'],
            File(initial="""\
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


if __name__ == '__main__':
    unittest.main()
