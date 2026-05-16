import pytest

from helper import FAKTURA, FAKTURABEZ, konwertuj_dok
from xml_konwerter import KONWXML

PARAMS = pytest.mark.parametrize(
    "zamien,KO,table,tr,expect_table",
    [
        (False, KONWXML, "table", "tr", True),
        (True, FAKTURA, "fakturalinie", "wiersze", True),
        (True, FAKTURABEZ, "fakturalinie", "wiersze", False),
    ],
)


class TestKonwerter:
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
        assert "NIP_SPRZEDAWCA_123" in xml
        assert "NABYWCA_999" in xml
        assert "2022-99-99" in xml
        assert "NUMER-222/99/555" in xml

    @PARAMS
    def test_zamien_linie(self, zamien, KO, table, tr, expect_table):
        przyklad = self.PRZYKLAD_LINIE
        d = {
            "ID": "Space Corporation",
        }
        xml = konwertuj_dok(przyklad, d,
                            html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA, KO=KO, zamien=zamien)
        print(xml)
        assert "Space Corporation" in xml
        assert "LINIE" not in xml
        assert (table in xml) == expect_table
        assert tr not in xml

        # jedna linia
        linie = {self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}]}
        d.update(linie)
        xml = konwertuj_dok(przyklad, d,
                            html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA, KO=KO, zamien=zamien)
        print(xml)
        assert "XXXXX" in xml
        assert (table in xml) == expect_table

        # dwie linie
        linie = {self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}]}
        d.update(linie)
        xml = konwertuj_dok(przyklad, d,
                            html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA, KO=KO, zamien=zamien)
        print(xml)
        assert "XXXXX" in xml
        assert "YYYYY" in xml
        assert (table in xml) == expect_table
        assert tr in xml

        # teraz setka
        linie = {self.KLUCZ_LINIA: [
            {"NUMER": f"XXX{no}YYY"} for no in range(100)]}
        d.update(linie)
        xml = konwertuj_dok(przyklad, d,
                            html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA, KO=KO, zamien=zamien)
        print(xml)
        assert "XXX1YYY" in xml
        assert "XXX99YYY" in xml
        assert (table in xml) == expect_table
        assert tr in xml

    def _test_zamien_linie_naglowek(self, xml_name, zamien, KO, table, tr, expect_table, add_text=None):
        d = {
            "ID": "Space Corporation",
        }
        xml = konwertuj_dok(
            xml_name, d,
            html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA,
            html_linia1=self.HTML_LINIE1, k_lista1=self.KLUCZ_LINIA1,
            KO=KO, zamien=zamien,
        )
        print(xml)
        assert "Space Corporation" in xml
        assert "LINIE" not in xml
        assert "SUPER NA" not in xml
        assert (table in xml) == expect_table
        assert tr not in xml
        if add_text:
            assert add_text not in xml

        # teraz naglowek
        linie = {self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}]}
        d.update(linie)
        xml = konwertuj_dok(
            xml_name, d,
            html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA,
            html_linia1=self.HTML_LINIE1, k_lista1=self.KLUCZ_LINIA1,
            KO=KO, zamien=zamien,
        )
        print(xml)
        assert "SUPER NA" in xml
        assert "XXXXX" in xml
        assert "YYYYY" in xml
        assert (table in xml) == expect_table
        assert tr in xml
        if add_text:
            assert add_text in xml

    @PARAMS
    def test_zamien_linie_naglowek(self, zamien, KO, table, tr, expect_table):
        self._test_zamien_linie_naglowek(self.PRZYKLAD_LINIE_NAGL, zamien, KO, table, tr, expect_table)

    @PARAMS
    def test_zamien_linie_naglowek_podglowek(self, zamien, KO, table, tr, expect_table):
        self._test_zamien_linie_naglowek(self.PRZYKLAD_LINIE_NAGL_PODL, zamien, KO, table, tr, expect_table, "SUPER POD")

    @PARAMS
    def test_zamien_linie2(self, zamien, KO, table, tr, expect_table):
        self._test_zamien_linie_naglowek(self.PRZYKLAD_LINIE2, zamien, KO, table, tr, expect_table)

    @PARAMS
    def test_zamien_linie2_linie2(self, zamien, KO, table, tr, expect_table):
        xml_name = self.PRZYKLAD_LINIE2
        d = {
            "ID": "Space Corporation",
            self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}],
            self.KLUCZ_LINIA1: [{"CUSTOMER": "SPACE", "NUMER": "22"}],
        }
        xml = konwertuj_dok(
            xml_name, d,
            html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA,
            html_linia1=self.HTML_LINIE1, k_lista1=self.KLUCZ_LINIA1,
            KO=KO, zamien=zamien,
        )
        print(xml)
        assert "XXXX" in xml
        assert "SPACE 22" in xml
        assert (table in xml) == expect_table
        assert tr in xml

    @PARAMS
    def test_zamien_linie_nested(self, zamien, KO, table, tr, expect_table):
        xml_name = self.PRZYKLAD_LINIE_NESTED
        linia1 = [{"OPISSUMA": f"OPISSUMA{no}", "DRUGASUMA": f"1{no}"}
                  for no in range(100)]
        d = {
            "ID": "Space Corporation",
            self.KLUCZ_LINIA: [{"NUMER": "XXXXX"}, {"NUMER": "YYYYYY "}],
            self.KLUCZ_LINIA1: [{"linia": [{"OPIS1": "OPISAAAA", "SUMA1": "2222"}]}, {"linia1": linia1}],
        }
        xml = konwertuj_dok(
            xml_name, d,
            html_linia=self.HTML_LINIE, k_lista=self.KLUCZ_LINIA,
            html_linia1=self.HTML_LINIE1, k_lista1=self.KLUCZ_LINIA1,
            KO=KO, zamien=zamien,
        )
        print(xml)
        assert "SUPER NA" in xml
        assert "XXXXX" in xml
        assert "YYYYY" in xml
        assert "OPISAAAA 2222" in xml
        assert "OPISSUMA0 10" in xml
        assert "OPISSUMA99 199" in xml
        assert (table in xml) == expect_table
        assert tr in xml
