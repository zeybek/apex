import unittest

from routing import select_primary


class RoutingTests(unittest.TestCase):
    def test_selects_preferred_primary_when_all_regions_are_healthy(self) -> None:
        healthy = {"us-east-1", "us-west-2", "eu-west-1"}
        self.assertEqual(select_primary(healthy), "us-east-1")

    def test_requires_a_healthy_region(self) -> None:
        with self.assertRaises(ValueError):
            select_primary(set())


if __name__ == "__main__":
    unittest.main()
