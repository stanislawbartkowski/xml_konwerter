from copy import deepcopy
from xml.etree.ElementTree import Element


class KONWXML:
    TABLE_TAG = "table"

    @classmethod
    def replace_text(cls, root: Element, d: dict):
        for elem in root.iter():
            te = elem.text
            if te is None:
                continue
            spos = 0
            # znajdz zmienne w linii
            zmset = []
            while True:
                beg = te.find("{{", spos)
                end = te.find("}}", spos)
                if beg >= 0 and end > 0:
                    varia = te[beg + 2 : end]
                    if varia in d:
                        zmset.append(varia)
                else:
                    break
                spos = end + 2

            # teraz zamien
            for zm in zmset:
                subst = "{{" + zm + "}}"
                te = te.replace(subst, d[zm])

            elem.text = te

    @classmethod
    def replace_all(
        cls, root: Element, d: dict, alista: dict[str, list], prefix: str, htmlkeypairing: list[tuple[str, str]] = []
    ):
        cls.replace_text(root, d)
        prefix = prefix or ""
        for htmllista, keylista in htmlkeypairing:
            cls.replace_linie(root, d, alista, prefix + htmllista, keylista, htmlkeypairing)

    @classmethod
    def replace_linie(
        cls,
        root: Element,
        d: dict,
        alista: dict[str, list],
        htmllista: str,
        keylista: str,
        htmlkeypairing: list[tuple[str, str]],
    ):
        taglist = "{{LINIE" + htmllista + "}}"
        lte = None
        notable = 0
        # tutaj wyszukuj odpowiedniej tabeli oznaczone {{LINIE...}}
        # jest to koślawe, najpierw znajduje tag i zakłada,
        # że nastepny table jest tym szukanym
        for elem in root.iter():
            te = elem.text
            if elem.tag == cls.TABLE_TAG:
                notable += 1
            if te is None:
                continue
            if te == taglist:
                lte = elem
                break
        if lte is None:
            return
        # usuwa znacznik
        elem = root.find(f'.//p[.="{taglist}"]')
        parent = root.find(f'.//p[.="{taglist}"]/..')
        parent.remove(elem)

        # teraz szuka table o właściwym numerz
        tablepar = root.findall(".//table")[notable]
        # tutaj ./, tylko direct children
        trlist = tablepar.findall("./tr")
        # rozpoznanie, który element jest iterowalny
        tr = trlist[0] if len(trlist) == 1 else trlist[1]
        insert = -1 if len(trlist) <= 2 else 1
        # usun iterowalny element (i potem będzie powielny w pętli)
        lista = alista.get(keylista)
        if lista is None:
            for t in trlist:
                tablepar.remove(t)
            return
        tablepar.remove(tr)
        it = iter(lista) if insert == -1 else reversed(lista)
        for e in it:
            trc = deepcopy(tr)
            # _replace_text(trc, e)
            # tutaj rekurencyjnie podmnieniaj zawartość tabeli
            cls.replace_all(trc, d | e, e, htmllista, htmlkeypairing)
            if insert == -1:
                tablepar.append(trc)
            else:
                tablepar.insert(insert, trc)
