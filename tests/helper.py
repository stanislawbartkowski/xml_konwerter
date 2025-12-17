import os
from tempfile import NamedTemporaryFile

import xml.etree.ElementTree as et

from konwdocs import KONWXML


def _wez_test_plik(plik: str) -> str:
    p = os.path.join(os.path.dirname(__file__), "testdata", plik)
    return p


def konwertuj_dok(plik: str, d: dict) -> str:
    plik_path = _wez_test_plik(plik)
    tree = et.parse(plik_path)
    root = tree.getroot()
    K = KONWXML(root=root)
    K.replace_all(d=d)
    tfile = NamedTemporaryFile()
    tree.write(tfile.name)
    xml = tfile.read()
    return xml.decode()
