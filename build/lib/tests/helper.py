import os
from tempfile import NamedTemporaryFile

from xml_konwerter import konwertujdok


def _wez_test_plik(plik: str) -> str:
    p = os.path.join(os.path.dirname(__file__), "testdata", plik)
    return p


def konwertuj_dok(
    plik: str,
    d: dict,
    alist: dict = None,
    html_linia: str = None,
    k_lista: str = None,
    html_linia1: str = None,
    k_lista1: str = None,
) -> str:
    plik_path = _wez_test_plik(plik)
    htmlkeypairing = []
    if html_linia is not None:
        htmlkeypairing.append((html_linia, k_lista))
    if html_linia1 is not None:
        htmlkeypairing.append((html_linia1, k_lista1))
    with NamedTemporaryFile() as tfile:
        konwertujdok(sou=plik_path, dest=tfile.name, d=d,
                     alist=alist, htmlkeypairing=htmlkeypairing)
        xml = tfile.read()
        return xml.decode()
