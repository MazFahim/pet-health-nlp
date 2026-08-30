"""
Basic sanity tests for extract_pet_health_info().

Tests 1-2 check input validation and run instantly, no API calls.
Test 3 makes one real Gemini API call to confirm the function still works
end-to-end and returns the expected shape. It is skipped automatically if
GEMINI_API_KEY is not set, so these tests can still run offline.
"""

import os
import unittest

from pet_health_nlp.extractor import extract_pet_health_info


class TestExtractPetHealthInfo(unittest.TestCase):

    def test_empty_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            extract_pet_health_info("")

    def test_non_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            extract_pet_health_info(None)
        with self.assertRaises(ValueError):
            extract_pet_health_info(123)

    @unittest.skipUnless(
        os.environ.get("GEMINI_API_KEY"),
        "GEMINI_API_KEY not set - skipping live API test",
    )
    def test_real_input_returns_expected_shape(self):
        result = extract_pet_health_info(
            "My dog has been scratching his ears and shaking his head."
        )
        self.assertIsInstance(result, dict)
        self.assertIn("condition", result)
        self.assertIn("keywords", result)
        self.assertIsInstance(result["keywords"], list)


if __name__ == "__main__":
    unittest.main()