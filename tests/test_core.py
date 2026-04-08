import unittest
import os
import shutil
from repo2prompt.core import get_token_count, rank_files, process_repository

class TestCoreFunctions(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory for tests
        self.test_dir = "temp_test_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create a sample gitignore
        with open(os.path.join(self.test_dir, ".gitignore"), "w", encoding="utf-8") as f:
            f.write("secret.txt\n")
            f.write("ignored_folder/\n")
            
        # Create files to test filtering
        with open(os.path.join(self.test_dir, "secret.txt"), "w", encoding="utf-8") as f:
            f.write("this is a secret")
            
        with open(os.path.join(self.test_dir, "public.txt"), "w", encoding="utf-8") as f:
            f.write("this is public")
            
        os.makedirs(os.path.join(self.test_dir, "ignored_folder"), exist_ok=True)
        with open(os.path.join(self.test_dir, "ignored_folder", "data.txt"), "w", encoding="utf-8") as f:
            f.write("this is ignored")
            
    def tearDown(self):
        # Clean up temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_token_count(self):
        count = get_token_count("Hello world!")
        # "Hello world!" typically encodes to ~3 tokens
        self.assertGreater(count, 0)
        self.assertTrue(isinstance(count, int))
        
    def test_rank_files(self):
        files = [
            ("config.json", "/path/config.json"),
            ("main.py", "/path/main.py"),
            ("README.md", "/path/README.md"),
            ("utils.py", "/path/utils.py")
        ]
        ranked = rank_files(files)
        # README should be first, then main.py, then utils.py, then config.json
        self.assertEqual(ranked[0][0], "README.md")
        self.assertEqual(ranked[1][0], "main.py")
        self.assertEqual(ranked[2][0], "utils.py")
        self.assertEqual(ranked[3][0], "config.json")

    def test_gitignore_filtering(self):
        # Run process_repository and check if secret.txt is filtered out
        chunks = process_repository(self.test_dir, max_tokens_per_chunk=100000)
        self.assertEqual(len(chunks), 1)
        
        output = chunks[0]
        # public.txt should be in the output
        self.assertIn("File: public.txt", output)
        self.assertIn("this is public", output)
        
        # secret.txt should NOT be in the output
        self.assertNotIn("File: secret.txt", output)
        self.assertNotIn("this is a secret", output)
        
        # ignored_folder/data.txt should NOT be in the output
        self.assertNotIn("File: ignored_folder/data.txt", output)
        self.assertNotIn("this is ignored", output)

if __name__ == "__main__":
    unittest.main()
