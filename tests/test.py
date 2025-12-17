import unittest

from helper import konwertuj_dok


class TestKonwerter(unittest.TestCase):

    PRZYKLAD = "test_faktura.xml"

    def test_zamien(self):
        d = {
            "NIP": "NIP_SPRZEDAWCA_123",
            "NIP_NABYWCA": "NABYWCA_999",
            "DATA_WYSTAWIENIA": "2022-99-99",
            "NUMER_FAKTURY": "NUMER-222/99/555"
        }
        xml = konwertuj_dok(self.PRZYKLAD, d)
        print(xml)
        self.assertIn("NIP_SPRZEDAWCA_123", xml)
        self.assertIn("NABYWCA_999", xml)
        self.assertIn("2022-99-99", xml)
        self.assertIn("NUMER-222/99/555", xml)
