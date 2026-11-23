"""Manual corrections on top of the automatic parse, then export recipes.js for SOMA."""
import json, re, sys
_code = open("tools/parse.py", encoding="utf-8").read()
_ns = {"re": re, "unicodedata": __import__("unicodedata")}
exec(_code[_code.index("def strip_accents"):_code.index("def is_step")], _ns)
parse_ingredient = _ns["parse_ingredient"]

R = json.load(open(sys.argv[1], encoding="utf-8"))
by = {r["title"]: r for r in R}

def ing(raw):
    return parse_ingredient(raw)

# Porc aigre-doux : "Pour le dressage" is a group header
r = by["Porc Aigre-Doux au Thé Vert"]
sauce = r["ingredients"][1]["items"]
i = next(k for k, x in enumerate(sauce) if x["raw"] == "Pour le dressage")
r["ingredients"][1]["items"] = sauce[:i]
r["ingredients"].append({"name": "Dressage", "items": sauce[i + 1:]})

# Saumon confit : split the marinade line
r = by["Saumon Confit Flamme"]
items = r["ingredients"][0]["items"]
mar = next(x for x in items if x["raw"].startswith("Marinade"))
items.remove(mar)
parts = [p.strip() for p in mar["raw"].split(":", 1)[1].split(";")]
r["ingredients"].append({"name": "Marinade", "items": [ing(p[0].upper() + p[1:]) for p in parts]})

# Ramen africaine : harissa group
r = by["Ramen Africaine"]
items = r["ingredients"][0]["items"]
i = next(k for k, x in enumerate(items) if x["raw"] == "Harissa maison")
r["ingredients"] = [{"name": None, "items": items[:i]}, {"name": "Harissa maison", "items": items[i + 1:]}]

# Gâteau roulé : clean
r = by["Gâteau Roulé au Sucre Muscovado"]
r["ingredients"][1]["name"] = "Motif coloré"
for grp in r["ingredients"]:
    for x in grp["items"]:
        if x["raw"].startswith("optionnel"):
            x.update(ing("1cc de sauce soja (optionnel)"))
r["notes"] = ["Motif fleuri : technique de Yuni Sweets (vidéo « How to make floral design Roll cake »)."]

# Soufflé léger : fold the stray group into Déco
r = by["Soufflé Léger de Grâce"]
extra = r["ingredients"].pop()
deco = r["ingredients"][-1]["items"]
deco[-1].update(ing("Fleurs rincées et égouttées (comestibles, c’est encore mieux)"))
deco.extend(extra["items"])

# Risotto aux pommes : rebuild from the messy source
r = by["Risotto aux Pommes"]
r["servings"] = 2
r["ingredients"] = [{"name": None, "items": [ing(x) for x in [
    "½ oignon", "40g de beurre", "200g de riz pour risotto (arborio ou carnaroli)",
    "600ml de bouillon de poulet", "200ml de jus de pomme (pas trop sucré)", "¼ de pomme",
    "4 c.a.s de jus de citron", "40g de parmesan", "4 tranches de bacon (ou bœuf)", "Persil frais", "Sel, poivre"]]}]
r["steps"] = []
r["notes"] = ["Idée dessert associée : banana cake cuit dans une peau de banane (coller avec du blanc d’œuf)."]

# Lièvre à la Royale : merge the plating sub-items into one step
r = by["Lièvre à la Royale"]
k = r["steps"].index("Dans l’assiette, déposer :")
r["steps"] = r["steps"][:k] + ["Dans l’assiette, déposer : " + ", ".join(s.lower() for s in r["steps"][k + 1:]) + "."]

# Chou farci : "12-14 feuilles de chou"
for x in by["Chou Farci"]["ingredients"][0]["items"]:
    if x["name"].startswith("-14"):
        x.update({"raw": "12 à 14 feuilles de chou", "qty": 13, "unit": None, "name": "feuilles de chou"})

# Cleanup
for r in R:
    for g in r["ingredients"]:
        for x in g["items"]:
            x["name"] = re.sub(r"^\.\s*(de |d’|d')?", "", x["name"]).strip()
    r["notes"] = [n for n in r["notes"] if n]

open(sys.argv[2], "w", encoding="utf-8").write(
    "// Généré depuis « La Gutxunomie » par Enzo Rochel — ne pas éditer à la main, voir tools/\n"
    "window.SOMA_RECIPES = " + json.dumps(R, ensure_ascii=False, indent=0) + ";\n")
from collections import Counter
print(Counter(r["status"] for r in R))
print([r["title"] for r in R if r["status"] != "complete"])
