import os
from tempfile import NamedTemporaryFile

import xml.etree.ElementTree as et

from konwdocs import konwertujdok


def _wez_test_plik(plik: str) -> str:
    p = os.path.join(os.path.dirname(__file__), "testdata", plik)
    return p


def konwertuj_dok(plik: str, d: dict) -> str:
    plik_path = _wez_test_plik(plik)
    with NamedTemporaryFile() as tfile:
        konwertujdok(sou=plik_path, dest=tfile.name, d=d)
        xml = tfile.read()
        return xml.decode()
