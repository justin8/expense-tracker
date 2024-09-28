import unittest
from expense_tracker.parser import autodetect, cardholder, company_detection, transaction_value, match


class TestParser(unittest.TestCase):
    def test_autodetect(self):
        row = ["2024-09-28", "Woolworths", "John Doe", "$50.00"]
        result = autodetect(row)
        self.assertEqual(result[0], "Groceries")
        self.assertEqual(result[1], "Woolworths")

    def test_cardholder(self):
        row = ["2024-09-28", "Woolworths", "John Doe", "$50.00"]
        result = cardholder(row)
        self.assertEqual(result, "John")

    def test_company_detection(self):
        row = ["2024-09-28", "JANG & JANG", "John Doe", "$50.00"]
        result = company_detection(row)
        self.assertIn("Sushi Edo", result)

    def test_transaction_value(self):
        row = ["2024-09-28", "Woolworths", "John Doe", "$50.00"]
        result = transaction_value(row)
        self.assertEqual(result, 50.00)

    def test_match(self):
        pattern = "Woolworths"
        string = "I shopped at Woolworths today"
        result = match(pattern, string)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
