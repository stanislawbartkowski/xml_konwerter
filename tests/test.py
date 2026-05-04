import unittest

from helper import konwertuj_dok


class TestKonwerter(unittest.TestCase):
    PRZYKLAD = "test_faktura.xml"
    PRZYKLAD_LINIE = "test_linie.xml"
    PRZYKLAD_LINIE_NAGL = "test_linie_nagl.xml"
    PRZYKLAD_LINIE_NAGL_PODL = "test_linie_nagl_podl.xml"
    PRZYKLAD_LINIE2 = "test_linie2_nagl.xml"
    PRZYKLAD_LINIE_NESTED = "test_linie2_nested.xml"

    HTML_LINIE = ""
    HTML_LINIE1 = "1"
    KLUCZ_LINIA = "linia"
    KLUCZ_LINIA1 = "linia1"

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

    def _test_zamien_linie_naglowek(self, xml_name, add_text=None):
        d = {
            "ID": "Space Corporation",
        }
        xml = konwertuj_dok(
            xml_name,
            d,
            html_linia=self.HTML_LINIE,
            k_lista=self.KLUCZ_LINIA,
            html_linia1=self.HTML_LINIE1,
            k_lista1=self.KLUCZ_LINIA1,
        )
        print(xml)
        self.assertIn("Space Corporation", xml)
        # powienie usunąć
        self.assertNotIn("LINIE", xml)
        self.assertNotIn("SUPER NA", xml)
        self.assertIn("table", xml)
        if add_text:
            self.assertNotIn(add_text, xml)

        # teraz naglowek
        # dwie linie
        linie = {self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}]}
        d.update(linie)
        xml = konwertuj_dok(
            xml_name,
            d,
            html_linia=self.HTML_LINIE,
            k_lista=self.KLUCZ_LINIA,
            html_linia1=self.HTML_LINIE1,
            k_lista1=self.KLUCZ_LINIA1,
        )
        print(xml)
        self.assertIn("SUPER NA", xml)
        self.assertIn("XXXXX", xml)
        self.assertIn("YYYYY", xml)
        self.assertIn("table", xml)
        if add_text:
            self.assertIn(add_text, xml)

    def test_zamien_linie_naglowek(self):
        self._test_zamien_linie_naglowek(self.PRZYKLAD_LINIE_NAGL)

    def test_zamien_linie_naglowek_podglowek(self):
        self._test_zamien_linie_naglowek(self.PRZYKLAD_LINIE_NAGL_PODL, "SUPER POD")

    def test_zamien_linie2(self):
        self._test_zamien_linie_naglowek(self.PRZYKLAD_LINIE2)

    def test_zamien_linie2_linie2(self):
        xml_name = self.PRZYKLAD_LINIE2
        d = {
            "ID": "Space Corporation",
            self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}],
            self.KLUCZ_LINIA1: [{"CUSTOMER": "SPACE", "NUMER": "22"}],
        }
        xml = konwertuj_dok(
            xml_name,
            d,
            html_linia=self.HTML_LINIE,
            k_lista=self.KLUCZ_LINIA,
            html_linia1=self.HTML_LINIE1,
            k_lista1=self.KLUCZ_LINIA1,
        )
        print(xml)
        self.assertIn("XXXX", xml)
        self.assertIn("SPACE 22", xml)

    def test_zamien_linie_nested(self):
        xml_name = self.PRZYKLAD_LINIE_NESTED
        linia1 = [{"OPISSUMA": f"OPISSUMA{no}", "DRUGASUMA": f"1{no}"} for no in range(100)]
        d = {
            "ID": "Space Corporation",
            self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}],
            self.KLUCZ_LINIA1: [{"linia": [{"OPIS1": "OPISAAAA", "SUMA1": "2222"}]}, {"linia1": linia1}],
        }
        xml = konwertuj_dok(
            xml_name,
            d,
            html_linia=self.HTML_LINIE,
            k_lista=self.KLUCZ_LINIA,
            html_linia1=self.HTML_LINIE1,
            k_lista1=self.KLUCZ_LINIA1,
        )
        print(xml)
        self.assertIn("SUPER NA", xml)
        self.assertIn("XXXXX", xml)
        self.assertIn("YYYYY", xml)
        self.assertIn("OPISAAAA 2222", xml)
        self.assertIn("OPISSUMA0 10", xml)
        self.assertIn("OPISSUMA99 199", xml)
