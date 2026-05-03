import unittest

from helper import konwertuj_dok


class TestKonwerter(unittest.TestCase):
    PRZYKLAD = "test_faktura.xml"
    PRZYKLAD_LINIE = "test_linie.xml"
    PRZYKLAD_LINIE_NAGL = "test_linie_nagl.xml"

    HTML_LINIE = ""
    KLUCZ_LINIA = "linia1"

    def test_zamien(self):
        d = {
            "NIP": "NIP_SPRZEDAWCA_123",
            "NIP_NABYWCA": "NABYWCA_999",
            "DATA_WYSTAWIENIA": "2022-99-99",
            "NUMER_FAKTURY": "NUMER-222/99/555",
        }
        xml = konwertuj_dok(self.PRZYKLAD, d)
        print(xml)
        self.assertIn("NIP_SPRZEDAWCA_123", xml)
        self.assertIn("NABYWCA_999", xml)
        self.assertIn("2022-99-99", xml)
        self.assertIn("NUMER-222/99/555", xml)

    def test_zamien_linie(self):
        d = {
            "ID": "Space Corporation",
        }
        xml = konwertuj_dok(self.PRZYKLAD_LINIE, d, html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA)
        print(xml)
        self.assertIn("Space Corporation", xml)
        # powienie usunąć
        self.assertNotIn("LINIE", xml)
        self.assertIn("table", xml)

        # jedna linia
        linie = {self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}]}
        d.update(linie)
        xml = konwertuj_dok(self.PRZYKLAD_LINIE, d, html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA)
        print(xml)
        self.assertIn("XXXXX", xml)
        self.assertIn("table", xml)

        # dwie linie
        linie = {self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}]}
        d.update(linie)
        xml = konwertuj_dok(self.PRZYKLAD_LINIE, d, html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA)
        print(xml)
        self.assertIn("XXXXX", xml)
        self.assertIn("YYYYY", xml)
        self.assertIn("table", xml)

        # teraz setka
        linie = {self.KLUCZ_LINIA: [{"NUMER": f"XXX{no}YYY"} for no in range(100)]}
        d.update(linie)
        xml = konwertuj_dok(self.PRZYKLAD_LINIE, d, html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA)
        print(xml)
        self.assertIn("XXX1YYY", xml)
        self.assertIn("XXX99YYY", xml)
        self.assertIn("table", xml)

    def test_zamien_linie_naglowek(self):
        d = {
            "ID": "Space Corporation",
        }
        xml = konwertuj_dok(self.PRZYKLAD_LINIE_NAGL, d, html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA)
        print(xml)
        self.assertIn("Space Corporation", xml)
        # powienie usunąć
        self.assertNotIn("LINIE", xml)
        self.assertNotIn("SUPER NA", xml)
        self.assertIn("table", xml)

        # teraz naglowek
        # dwie linie
        linie = {self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}]}
        d.update(linie)
        xml = konwertuj_dok(self.PRZYKLAD_LINIE_NAGL, d, html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA)
        print(xml)
        self.assertIn("SUPER NA", xml)
        self.assertIn("XXXXX", xml)
        self.assertIn("YYYYY", xml)
        self.assertIn("table", xml)
