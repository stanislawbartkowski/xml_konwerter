from lxml import etree

from xml_konwerter import KONWXML


def konwertujdok(sou: str, dest: str, d: dict, alist: dict = None, htmlkeypairing: list[tuple[str, str]] = []):
    alist = alist or d
    tree = etree.parse(sou)
    root = tree.getroot()
    K = KONWXML()
    K.replace_all(root, d, alist, prefix="", htmlkeypairing=htmlkeypairing)
    tree.write(dest)
