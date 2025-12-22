import xml.etree.ElementTree as et

from xml_konwerter import KONWXML


def konwertujdok(sou: str, dest: str, d: dict):
    tree = et.parse(sou)
    root = tree.getroot()
    K = KONWXML(root=root)
    K.replace_all(d=d)
    tree.write(dest)
