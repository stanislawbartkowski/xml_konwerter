import os
from tempfile import NamedTemporaryFile

from xml_konwerter import KONWXML, konwertujdok


def _wez_test_plik(plik: str) -> str:
    p = os.path.join(os.path.dirname(__file__), "testdata", plik)
    return p


def _zamien_tagi_faktura(plik: str) -> str:
    src = _wez_test_plik(plik)
    with open(src) as f:
        content = f.read()
    content = content.replace("table", "fakturalinie").replace("tr", "wiersze")
    tmp = NamedTemporaryFile(mode="w", suffix=".xml", delete=False)
    tmp.write(content)
    tmp.close()
    return tmp.name


def konwertuj_dok(
    plik: str,
    d: dict,
    alist: dict = None,
    html_linia: str = None,
    k_lista: str = None,
    html_linia1: str = None,
    k_lista1: str = None,
    KO=KONWXML,
    zamien: bool = False
) -> str:
    plik_path = _zamien_tagi_faktura(plik) if zamien else _wez_test_plik(plik)
    htmlkeypairing = []
    if html_linia is not None:
        htmlkeypairing.append((html_linia, k_lista))
    if html_linia1 is not None:
        htmlkeypairing.append((html_linia1, k_lista1))
    with NamedTemporaryFile() as tfile:
        konwertujdok(sou=plik_path, dest=tfile.name, d=d,
                     alist=alist, htmlkeypairing=htmlkeypairing, KO=KO)
        xml = tfile.read()
        return xml.decode()


class FAKTURA(KONWXML):
    TABLE_TAG = "fakturalinie"
    TR_TAG = "wiersze"


class FAKTURABEZ(FAKTURA):
    REMNOVE_TABLE_TAG = True
