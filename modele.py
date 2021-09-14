from tinydb import TinyDB, Query

from datetime import datetime
"""
Dans ce fichier on va créer toutes les classes pour le script
"""

class Joueur:
    def __init__(self, nom, prenom, date_de_naissance, sexe, classement, tournois, points,
                 joueurs_affrontes):
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe
        self.classement = classement
        self.tournois = tournois
        self.points = points
        points = 0
        self.joueurs_affrontes = joueurs_affrontes
        joueurs_affrontes = []

class Tournois:
    def __init__(self, nom, lieu, date, nombre_de_tours, tournees, liste_des_joueurs, controle_du_temps, description,
                 date_de_creation):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nombre_de_tours = nombre_de_tours
        nombre_de_tours = 4
        self.tournees = tournees
        self.liste_des_joueurs = liste_des_joueurs
        Liste_des_joueurs = []
        self.controle_du_temps = controle_du_temps
        self.description = description
        self.date_de_creation = date_de_creation


class Tours:
    def __init__(self, nom, debut, fin, match, tournois):
        self.nom = nom
        self.debut = debut
        self.fin = fin
        self.match = match
        match = ()
        self.tournois = tournois

class Matchs:
    def __init__(self, paire, tournois):
        self.paire = paire
        paire = ()
        self.tournois = tournois


def liste_des_tournois():

    db = TinyDB('db.json')
    Tournois_table = db.table('Tournois')
    Tournois_table = Tournois_table.all()
    liste_tournois = []
    for tournois in Tournois_table:
        liste_tournois.append(tournois['nom'])
    return liste_tournois

def liste_joueurs():
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    liste_joueurs = []
    for player in players_table.all():
        nom = player['nom']
        prenom = player['prenom']
        nom_prenom = nom + " " + prenom
        liste_joueurs.append(nom_prenom)
    return liste_joueurs

def liste_acteurs_odre_alphabetique(liste_joueurs, tournois):
    if tournois == "":
        liste_joueur_ordre_alphabetique = sorted(liste_joueurs)
        print(liste_joueur_ordre_alphabetique)
    else:
        liste_joueurs = []
        db = TinyDB('db.json')
        players_table = db.table('Joueurs')
        q = Query()
        players = players_table.search(q.tournois == tournois)

        for player in players:
            nom_prenom = player['nom'] + " " + player['prenom']
            liste_joueurs.append(nom_prenom)
        liste_joueur_odre_alphabetique = sorted(liste_joueurs)
        print(liste_joueur_odre_alphabetique)

def creation_joueurs(tournois):

    marvin = Joueur("decocq", "marvin", "20/07/98", "m", 1, tournois, 0, [])
    marvin2 = Joueur("chebany", "rocket", "20/07/98", "m", 3, tournois, 0, [])
    marvin3 = Joueur("dunoyer", "kahyss", "16/03/2019", "m", 10, tournois, 0, [])
    loan = Joueur("dunoyer", "loan", "01/11/00", "f", 100, tournois, 0, [])
    papa = Joueur("decocq", "martial", "13/10/71", "m", 41, tournois, 0, [])
    maman = Joueur("chebany", "angela", "16/03/2019", "f", 2, tournois, 0, [])
    mamie = Joueur("chebany", "henriette", "09/06/50", "f", 34, tournois, 0, [])
    papy = Joueur("chebany", "cheban", "12/04/44", "m", 68, tournois, 0, [])
    liste_des_joueurs = [marvin, marvin2, marvin3, loan, papa, maman, mamie, papy]
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    players_table.truncate()
    for player in liste_des_joueurs:
        serialized_player = {
            'nom':player.nom,
            'prenom':player.prenom,
            'date de naissance':player.date_de_naissance,
            'sexe':player.sexe,
            'classement':player.classement,
            'tournois':player.tournois,
            'points':player.points,
            'liste joueurs affrontes':player.joueurs_affrontes
        }
        players_table.insert(serialized_player)
    print('\n')
    print('la liste des joueurs a bien été créé.')

