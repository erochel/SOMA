// SOMA — table nutritionnelle simplifiée pour estimer les calories des recettes.
// Format : "mots-clés séparés par des virgules | kcal pour 100 g | poids d'une pièce (g) | poids d'une c.à.s (g)"
// Valeurs moyennes arrondies (ordre de grandeur type Ciqual) : c'est une estimation, pas une analyse.
window.SOMA_NUTRITION = `
huile,huile olive,huile sesame,huile vegetal,huile cuisine,huile cuisson,huile colza,huile pepin raisin|900||13
graisse canard,graisse boeuf,graisse bœuf|900||13
beurre,noisette beurre,beurre doux,beurre fondu|745|10|14
beurre cacahuete,beurre cacahouete|600||16
creme,creme fleurette,creme entiere,creme liquide,creme fraiche,creme aigre|300||15
lait|50||15
lait coco|180||15
lait soja|40||15
yaourt|60|125|15
yaourt grec|120||15
mascarpone|430||15
mozzarella|250|125|15
parmesan|400||6
fromage,fromage rape,fromage poudre|380||7
chantilly|300||8
mayonnaise|700||15
oeuf,œuf,oeufs entier,œuf entier,oeuf dur,œuf dur|145|55|
jaune,jaune oeuf,jaune œuf|330|18|
blanc oeuf,blanc œuf|48|35|
sucre,sucre poudre,sucre glace,sucre roux,sucre vanille|400|8|12
muscovado,sucre muscovado|380||12
miel|320||21
sirop erable|260||20
chocolat,chocolat noir|540||
chocolat blanc|560||
confiture,gelee,gele framboise|250||20
compote,compote pomme|70||15
puree pomme,puree figue|70||15
farine,farine ble,farine riz gluant|350||10
fecule,fecule pomme terre,fecule mais,maizena|350||10
chapelure,chapelure japonaise,panko|370||8
riz,riz rond,riz thai,riz risotto|350||15
portion riz,dose riz|350|60|
nouille,nouilles riz,somen,udon,nouilles ble|350|80|
pate feuilletee,pate feuillete,pate sucre|400|230|
pate riz gluant|230||
biscuit cuillere|390|300|
pain,pain grille|260|40|
pain brioche|330|60|
pain mie|270|25|
tortilla|300|40|
feuille riz|340|9|
kirimochi,mochi|230|50|
pois chiche|140||15
petit pois|80||15
noix ginkgo|180||
poudre amande|600||8
marron,marron concasse|170|15|
marron sucre,marron confit,marron glace|300|15|
olive,olive noire|150|4|
capre|20||
pate haricot rouge|250||18
concentre tomate|80||16
pulpe tomate,coulis tomate,tomate concassee,tomate pelee|25||15
boite tomate|25|400|
ketchup|110||17
moutarde|150||15
sauce soja,soja,sauce soja sucre,soja noir|60||16
mirin|240||16
sake,alcool cuisine,vin shaoxing|110||15
vin,vin blanc,vin rouge|70||15
verre vin|70|120|
bouteille vin|70|750|
cidre|40||15
rhum|230||15
jus,jus orange,jus pomme|45||15
jus citron|25||15
jus tomate|20||15
vinaigre,vinaigre riz,vinaigre cidre,vinaigre vin,vinaigre xeres,vinaigre blanc,vinaigre noir|20||15
vinaigre balsamique|110||15
miso,miso blanc|200||18
sauce huitre|100||18
nuoc-mam,nuoc mam,sauce nuoc-mam,sauce nuoc,nam pla,sauce thai nam pla|35||16
hoisin,sauce hoisin,tianmianjiang,sauce tianmianjiang|220||18
sriracha,sauce sriracha,sauce piment,pate piment,puree piment,sauce pimentee|90||16
ponzu,sauce ponzu|50||16
sauce worcestershire|80||16
tabasco|0||
dashi,bouillon,fond,fond veau,fond volaille,fond blanc,fond gibier,consomme gibier,bouillon dashi,bouillon algue|5||15
consomme poudre,bouillon poudre|250||8
cube bouillon|250|10|
gelatine,feuille gelatine,gelifiant,agar-agar|340|2|
eau,eau chaude,verre eau|0||15
sel,gros sel,sel fin|0||18
curry,curcuma,cumin,graine cumin,garam masala,garam massala,paprika,piment espelette,poudre chili,cannelle,coriandre,graine coriandre,poivre,poivre rouge,gingembre poudre,ail poudre,the vert,poudre the vert|300||7
vanille,arome vanille|280||5
gousse vanille|280|3|
poulet,blanc poulet,blanc poulet hache|120|150|
cuisse,cuisse poulet|170|180|
aile,aile poulet,pilon,pilon aile|220|50|
pointe,pointe aile|220|30|
canard,magret,magret canard|200|350|
boeuf,bœuf,viande boeuf,viande bœuf,rumsteck,bavette,paleron,entrecote,steak|150|150|
steak hache,boeuf hache,bœuf hache|210|125|
tranche boeuf,tranche bœuf|150|25|
veau,epaule veau|130||
porc,echine,echine porc,cote porc,filet porc|220|200|
poitrine,poitrine porc,poitrine fumee|300|20|
porc hache|220||
bacon,tranche bacon|300|15|
jambon,tranche jambon|110|40|
saucisse|280|35|
foie,foie volaille|130||
foie gras|460||
lievre,chevreuil,gibier,lapin|130||
os,os moelle|20||
saumon,tranche saumon,pave saumon,darne saumon|200|120|
saumon fume,tranche saumon fume|180|25|
thon,sashimi|130||
boite thon|120|140|
maquereau,filet maquereau|200|100|
maquereau conserve|220||
brochet,filet brochet|90|150|
cabillaud,filet cabillaud,poisson,filet poisson|85|150|
daurade|100|250|
anguille|280||
calamar,calmar,tentacule calmar|80|100|
crevette,crevette decortiquee|90|15|
palourde|70|4|
ecrevisse|80|20|
anchoi,anchois hache|200|4|
fruits mer|80||
tofu,tofu soyeux|60|300|
tofu frit,tranche tofu frit|270|30|
pomme terre|80|150|
patate douce|85|250|
carotte|35|100|
oignon|40|120|
echalote|70|30|
tomate,tomate fraiche|20|120|
tomate cerise|20|15|
poivron,poivron rouge,poivron vert,poivron jaune|30|150|
courgette|17|200|
courge,courge jaune|30|300|
aubergine|25|250|
concombre|13|300|
poireau,blanc poireau|30|150|
endive|17|120|
chou,chou blanc|25|1000|
feuille chou|25|30|
brocoli|35|400|
navet|25|150|
champignon,champignon paris,shitake,shiitake,shimeji,champignon noir|25|20|
salade,mesclun,roquette,laitue,cresson,feuille salade|15||
epinard|25||
asperge,asperge blanche|25|25|
potimarron|40||
betterave|45|150|
haricot vert|30||
gombo|33|10|
celeri,branche celeri|15|40|
radis,radis blanc|15|15|
bardane,racine bardane|70|200|
igname|110||
avocat|200|150|
orange|45|150|
citron,citron jaune,citron vert|30|100|
yuzu|30|80|
pomme|55|150|
poire|55|170|
fraise|32|15|
framboise|40||
mangue|65||
banane|90|120|
figue|75|50|
prune|45|30|
grenade|80||
gingembre,racine gingembre,morceau gingembre,gingembre rape,gingembre hache|80|30|8
ail,gousse ail,ail hache,ail rape,ail puree,ail emince|130|5|8
`;
