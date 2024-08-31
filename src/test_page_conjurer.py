import os
import unittest
import data_constants as tt
from page_conjurer import extract_title, generate_page

class TestPageConjurer(unittest.TestCase):

    def setUp(self):
        with open("./tests/markdown.md", "r", encoding="UTF-8") as block_list:
            self.markdown_content = block_list.read()

    def test_header(self):
        self.assertEqual(extract_title(self.markdown_content), "This is the main header")

    def test_page_gen_simple(self):
        src_path = './tests/MarkdownSimple.md'
        des_path = './tests/result/MarkdownSimple.md'
        template_path = 'template.html'

        page = (generate_page(src_path, template_path, des_path))

        # check the page generation was successful
        self.assertTrue(page)
        with open(des_path, "r", encoding="UTF-8") as file:
            content = file.read()

            # Check some tags exist
            self.assertIn('<html>', content)
            self.assertIn('<title>', content)
            self.assertIn('<div>', content)

    def test_page_generation(self):
        src_path = './tests/markdown.md'
        des_path = './tests/result/markdown.md'
        template_path = 'template.html'

        if os.path.exists(des_path):
            os.remove(des_path)

        self.assertTrue(generate_page(src_path, template_path, des_path))

if __name__ == "__main__":
    unittest.main()