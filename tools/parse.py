"""Parse La Gutxunomie (markdown export of the PDF) into structured recipes for SOMA."""
import json, re, sys, unicodedata

src = open(sys.argv[1], encoding="utf-8").read()
out = sys.argv[2]

pages = re.split(r"^## Seite (\d+)\s*$", src, flags=re.M)
# pages = ['', '1', text, '2', text, ...]
page_map = {int(pages[i]): pages[i + 1] for i in range(1, len(pages), 2)}

def cat_for(p):
    if p < 19: return "Légumes"
    if p < 37: return "Poissons"
    if p < 73: return "Viandes"
    if p < 84: return "Desserts"
    return "Créations"

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

VERBS = set("""
epluchez eplucher coupez couper coupe faire faites faite melanger melangez placez placer mettez mettre
versez verser ajoutez ajouter rajoutez rajouter preparez preparer realiser realisez hacher hachez laver lavez
laisser laissez cuire cuisez porter portez decouper decoupez saler salez saupoudrer saupoudrez mixer mixez chauffez chauffer retirer retirez envelopper enveloppez prenez prendre
plonger plongez blanchir blanchissez desosser aplatir aplatissez parer piquer etendre etaler etalez reprenez
quadriller quadrillez decongeler cassez casser montez monter fouettez fouetter battre servez servir dressez
dresser filtrez incorporez incorporer deglacer remplir mouillez assaisonnez
enrouler presser pressez tremper trempez nettoyer nettoyez emincez emincer seche secher badigeonner
faire
""".split())

QTY = r"(\d+(?:[.,]\d+)?(?:\s*/\s*\d+)?|½|¼|¾|⅓|⅔)"
UNITS = [
    (r"c\.?\s?a\.?\s?s\.?|c\. à soupe|cuill[eè]res? à soupe|cs", "c.à.s"),
    (r"c\.?\s?a\.?\s?c\.?|c\. à café|cuill[eè]res? à café|cc", "c.à.c"),
    (r"kg", "kg"), (r"g", "g"), (r"cl|cL", "cl"), (r"ml", "ml"), (r"l|L|litres?", "l"),
    (r"pincées?", "pincée"), (r"gousses?", "gousse"),
]
FRAC = {"½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 1 / 3, "⅔": 2 / 3}

def parse_ingredient(text):
    t = text.strip().rstrip(".")
    m = re.match(QTY + r"\s*(.*)$", t)
    if not m:
        return {"raw": t, "qty": None, "unit": None, "name": t}
    q, rest = m.group(1), m.group(2)
    if q in FRAC: qty = FRAC[q]
    elif "/" in q:
        a, b = [x.strip() for x in q.split("/")]; qty = float(a) / float(b)
    else: qty = float(q.replace(",", "."))
    unit = None
    for pat, u in UNITS:
        um = re.match(r"(?:" + pat + r")(?=[\s’'.]|$)\s*", rest, flags=re.I)
        if um:
            unit, rest = u, rest[um.end():]
            break
    name = re.sub(r"^(de |d’|d'|des )", "", rest.strip(), flags=re.I).strip()
    if not name:
        return {"raw": t, "qty": None, "unit": None, "name": t}
    return {"raw": t, "qty": round(qty, 3), "unit": unit, "name": name}

def is_step(text):
    t = strip_accents(text.strip()).lower()
    first = re.split(r"[\s,’'.:]", t, maxsplit=1)[0]
    if re.match(r"^\d+\.\s", text.strip()): return True
    if len(text) > 130: return True
    if len(text) > 75 and first in VERBS: return True
    return first in VERBS and len(text.split()) > 3

def slugify(s):
    s = strip_accents(s).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

recipes = []
for p in sorted(page_map):
    if p < 7: continue
    lines = [l.rstrip() for l in page_map[p].strip().split("\n")]
    # drop header "La Gutxunomie by ER" and page number
    lines = [l for l in lines if l.strip() and l.strip() != "La Gutxunomie by ER" and l.strip() != str(p)]
    if not lines: continue
    if any(re.match(r"^\d\. (LES|CRÉATIONS)", l) for l in lines[:2]):
        continue  # section divider
    title = lines[0].strip()
    serv = 4
    body = [l for l in lines[1:] if not re.fullmatch(r"\s*-\s*1\s?c\.a\.[sc]\s*", l)]
    if body and body[0].lower().startswith("ingrédients pour"):
        m = re.search(r"pour (\d+)", body[0]); serv = int(m.group(1)) if m else 4
        body = body[1:]
    menu = None
    mm = re.match(r"Menu N°(\d+)\s*:\s*(.*)", title)
    if mm: menu, title = int(mm.group(1)), mm.group(2).strip()

    # merge continuation lines into bullets
    items = []  # (kind, text) kind: bullet|header|plain
    prev_len = 0
    for l in body:
        wrapped = prev_len >= 70
        prev_len = len(l.strip())
        s = l.strip()
        bm = re.match(r"^(?:[-•o]|\d+\.)\s*(.*)$", s)
        if s.startswith("#"):
            items.append(("note", s.lstrip("# ").strip())); continue
        if bm and (s[0] in "-•" or re.match(r"^\d+\.\s", s) or s.startswith("o ")):
            txt = bm.group(1).strip()
            if re.match(r"^\d+\.\s", s): txt = s
            if not txt: continue
            items.append(("bullet", txt))
        elif s.endswith(":") and len(s) < 45:
            items.append(("header", s.rstrip(" :")))
        elif items and wrapped and items[-1][0] in ("bullet", "plain"):
            k, t = items[-1]; items[-1] = (k, t + " " + s)
        else:
            items.append(("plain", s))

    groups = [{"name": None, "items": []}]
    steps, notes = [], []
    in_steps = False
    for k, t in items:
        if k == "note": notes.append(t); continue
        if not in_steps and k == "bullet" and is_step(t):
            in_steps = True
        if in_steps:
            if k == "header": steps.append(t + " :")
            else:
                steps.append(re.sub(r"^\d+\.\s*", "", t))
            continue
        if k == "header" or (k == "bullet" and t.endswith(":") and len(t) < 45):
            groups.append({"name": t.rstrip(" :"), "items": []}); continue
        if k == "plain":
            if len(t) < 45: groups.append({"name": t, "items": []})
            else: notes.append(t)
            continue
        # bullet ingredient; skip placeholders
        if re.fullmatch(r"1\s?c\.a\.[sc]", t): continue
        groups[-1]["items"].append(parse_ingredient(t))
    groups = [g for g in groups if g["items"]]
    n_ing = sum(len(g["items"]) for g in groups)
    if n_ing == 0 and not steps:
        status = "a_completer" if not notes else "brouillon"
    elif not steps or n_ing == 0:
        status = "brouillon"
    else:
        status = "complete"
    # a recipe whose last step is empty/truncated
    if title in ("Nouilles Sautées à la Vo", "Ramen", "Pâtes aux Écrevisses façon Gutxu", "Risotto aux Pommes", "Pho Parmentier", "Gâteau Roulé au Sucre Muscovado", "Soufflé Léger de Grâce"):
        status = "brouillon" if (steps or n_ing) else "a_completer"
    recipes.append({
        "id": slugify(title), "title": title, "category": cat_for(p), "menu": menu,
        "page": p, "servings": serv, "status": status,
        "ingredients": groups, "steps": steps, "notes": notes,
    })

json.dump(recipes, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(recipes), Counter(r["status"] for r in recipes), Counter(r["category"] for r in recipes))
