import unittest

from ohmygut.core.main import main


class TestCase(unittest.TestCase):
    def test_main(self):
        main(articles_directory="", bacteria_catalog="", nutrients_catalog="", sentence_parser="")
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
