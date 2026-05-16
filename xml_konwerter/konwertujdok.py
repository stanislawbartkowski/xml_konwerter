from lxml import etree

from .konwxml import KONWXML


def konwertujdok(sou: str, dest: str, d: dict, alist: dict = None, htmlkeypairing: list[tuple[str, str]] = [], KO=KONWXML):  # noqa: E501
    alist = alist or d
    tree = etree.parse(sou)
    root = tree.getroot()
    K = KO()
    K.replace_all(root, d, alist, prefix="", htmlkeypairing=htmlkeypairing)
    tree.write(dest)
