import unittest
from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):

    def setUp(self):
        self.fine = DuckFine("M001")

    def test_new_account_owes_nothing(self):
        self.assertEqual(self.fine.total_owed, 0.0)

    def test_member_id_is_stored(self):
        self.assertEqual(self.fine.member_id, "M001")

    def test_no_fee_when_returned_on_time(self):
        self.assertEqual(self.fine.charge(0), 0.0)

    def test_charge_returns_a_fee_for_a_late_duck(self):
        self.assertEqual(self.fine.charge(5), 1.50)

    def test_deluxe_duck_costs_more(self):
        self.assertTrue(self.fine.charge(5, deluxe=True) > 0)

    def test_negative_days_raises(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)

    # Tests added after mutation testing, one per requirement the suite missed.

    def test_fine_is_capped_at_five_dollars(self):
        # 20 days late: 18 chargeable days * $0.50 = $9.00, capped at $5.00
        self.assertEqual(self.fine.charge(20), 5.00)

    def test_fines_accumulate_against_the_member_account(self):
        # 5 days late = $1.50, 4 days late = $1.00, so $2.50 owed in total
        self.fine.charge(5)
        self.fine.charge(4)
        self.assertEqual(self.fine.total_owed, 2.50)

    def test_deluxe_duck_fee_is_exactly_double(self):
        # 5 days late: 3 chargeable days * $0.50 = $1.50, doubled = $3.00
        self.assertEqual(self.fine.charge(5, deluxe=True), 3.00)


if __name__ == "__main__":
    unittest.main()
