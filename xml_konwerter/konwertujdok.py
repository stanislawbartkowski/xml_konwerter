import xml.etree.ElementTree as et

from xml_konwerter import KONWXML


def konwertujdok(sou: str, dest: str, d: dict, htmllinia: str = None, kluczlista: str = None):
    tree = et.parse(sou)
    root = tree.getroot()
    K = KONWXML()
    K.replace_all(root, prefix="", d=d, alista=None)
    if htmllinia is not None:
        K.replace_linie(root, d, d, htmllinia, kluczlista)
    tree.write(dest)
