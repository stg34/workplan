import unittest
from file_scanner import FileScanner

class FileScannerTest(unittest.TestCase):
    def test_parse_file_01(self):
        scanner = FileScanner()
        scanner.scan_file('tests/data/data_01.txt')

        self.assertEqual(len(scanner.comments), 1)

        for line in scanner.comments[0]:
            print(line)

    def test_parse_file_02(self):
        scanner = FileScanner()
        scanner.scan_file('tests/data/data_02.txt')

        self.assertEqual(len(scanner.comments), 3)

if __name__ == '__main__':
    unittest.main()
