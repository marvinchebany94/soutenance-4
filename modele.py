from tinydb import TinyDB
"""
Dans ce fichier on va créer toutes les classes pour le script
"""

class Joueur:
    def __init__(self, nom, prenom, date_de_naissance, sexe, classement):
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe
        self.classement = classement

class Tournois:
    def __init__(self, nom, lieu, date, nombre_de_tours, tournees, liste_des_joueurs, description):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nombre_de_tours = nombre_de_tours
        nombre_de_tours = 4
        self.tournees = tournees
        self.liste_des_joueurs = liste_des_joueurs
        Liste_des_joueurs = []
        self.description = description

class Matchs:
    def __init__(self, id, tuple):
        self.id = id
        self.tuple = tuple


def liste_des_tournois():

    db = TinyDB('db.json')
    Tournois_table = db.table('Tournois')
    Tournois_table = Tournois_table.all()
    liste_tournois = []
    for tournois in Tournois_table:
        liste_tournois.append(tournois['nom'])
    return liste_tournois


marvin = Joueur("de cocq", "marvin", "20/07/98", "masculin", 1)
marvin2 = Joueur("chebany", "rocket", "20/07/98", "masculin", 3)
marvin3 = Joueur("dunoyer", "kahyss", "16/03/2019", "masculin", 10)
loan = Joueur("dunoyer", "loan", "01/11/00", "féminin", 100)
papa = Joueur("de cocq", "martial", "13/10/71", "masculin", 41)
maman = Joueur("chebany", "angela", "16/03/2019", "féminin", 2)
mamie = Joueur("chebany", "henriette", "09/06/50", "féminin", 34)
papy = Joueur("chebany", "cheban", "12/04/44", "masculin", 68)



liste_joueur = [marvin, marvin2, marvin3, loan, papa, maman, mamie, papy]
tournois = Tournois('rocket league', 'val-de-marne', "28/08/21","4","none", liste_joueur, "Beau tournois")
db = TinyDB('db.json')
players_table = db.table('joueurs')
tournois_table = db.table('tournois')
players_table.truncate()	# clear the table first

for player in liste_joueur:
    serialized_player = {
        'nom': player.nom,
        'prenom': player.prenom,
        'date de naissance': player.date_de_naissance,
        'sexe': player.sexe,
        'classement': player.classement

    }
    players_table.insert(serialized_player)
serialized_player = players_table.all()


liste_joueur = []
for item in players_table:
    liste_joueur.append(item)




"""
serialized_tournois = {
    'nom': tournois.nom,
    'lieu':tournois.lieu,
    'date':tournois.date,
    'nombre de tour':tournois.nombre_de_tours,
    'tournees':tournois.tournees,
    'liste de joueurs':liste_joueur,
    'description':tournois.description
}

tournois_table.insert(serialized_tournois)
serialized_tournois = tournois_table.all()

print(serialized_tournois)

"""

