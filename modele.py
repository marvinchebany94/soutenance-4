from tinydb import TinyDB, Query
import random
from datetime import datetime
"""
Dans ce fichier on va créer toutes les classes pour le script
"""

class Joueur:
    def __init__(self, nom, prenom, date_de_naissance, sexe, classement, tournois, points,
                 joueurs_affrontes, id):
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
        self.id = id

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
    """
    La fonction retourne la liste de tous les tournois présents dans la base de données
    :return: liste_tournois qui est une liste contenant le nom de tous les tournois
    """

    db = TinyDB('db.json')
    Tournois_table = db.table('Tournois')
    Tournois_table = Tournois_table.all()
    liste_tournois = []
    for tournois in Tournois_table:
        liste_tournois.append(tournois['nom'])
    return liste_tournois

def liste_joueurs(tournois):
    """
    La fonction va chercher la liste de tous les joueurs présents dans un tournois.
    Si tournois == "", la fonction fera une recherche sur la totalité de la base de données.
    :param tournois: Le tournois dont la liste des joueurs sera cherchée
    :return: liste_joueurs, une liste contenant le nom et prénom de chaque joueurs du tournois
    """
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()
    liste_joueurs = []
    if tournois == "":
        for player in players_table.all():
            nom = player['nom']
            prenom = player['prenom']
            nom_prenom = nom + " " + prenom
            classement = player['classement']
            nom_prenom = nom + " " + prenom
            liste_joueurs.append(nom_prenom)
    else:
        joueurs = players_table.search(q.tournois == tournois)
        for joueur in joueurs:
            nom = joueur['nom']
            prenom = joueur['prenom']
            classement = joueur['classement']
            nom_prenom = nom + " " + prenom
            liste_joueurs.append(nom_prenom)
    return liste_joueurs

def liste_acteurs_odre_alphabetique(liste_id, tournois):
    """
    La fonction retourne la liste des joueurs par ordre alphabétique.
    :param liste_joueurs: la liste des joueurs que l'on souhaite trier via leur id
    :param tournois: Le tournois pour lequel on trira la liste des joueurs
    :return: un print qui retourne la liste "liste_joueur_ordre_alphabetique" qui contient la liste trièe avec le nom
    et prénom de chaque joueurs.
    """
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()
    liste_triee = []
    joueur_deja_print = []
    if tournois == "":
        for id in liste_id:
            player = players_table.search(q.id == id)[0]
            nom_prenom = player['nom'] + " " + player['prenom']
            liste_triee.append(nom_prenom)

        liste_joueur_ordre_alphabetique = sorted(liste_triee)
        for player in liste_joueur_ordre_alphabetique:
            player = player.split()
            p_found = players_table.search(q.nom == player[0] and q.prenom == player[1])

            for p in p_found:
                nom = p['nom']
                prenom = p ['prenom']
                nom_prenom = nom + " " + prenom
                classement = p['classement']
                tuple = (nom_prenom, classement)
                if tuple not in joueur_deja_print:
                    joueur_deja_print.append(tuple)
                    print("""
                        Nom : {}
                        Prénom : {}
                        Classement : {}
                    """.format(nom, prenom, classement))
                else:
                    continue

    else:
        for id in liste_id:
            player = players_table.search(q.id == id)[0]
            nom_prenom = player['nom'] + " " + player['prenom']
            liste_triee.append(nom_prenom)

        liste_joueur_odre_alphabetique = sorted(liste_triee)
        for player in liste_joueur_odre_alphabetique:
            player = player.split()
            p = players_table.search((q.nom == player[0]) & (q.prenom == player[1]) & (q.tournois == tournois))[0]
            nom = p['nom']
            prenom = p['prenom']
            nom_prenom = nom + " " + prenom
            classement = p['classement']
            tournois = p['tournois']
            print("""
                Nom : {}
                Prénom : {}
                Classement : {}
                Tournois : {}
            """.format(nom, prenom, classement, tournois))


def id_auto_increment():
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    players_table = players_table.all()
    if not players_table:
        id = 1
    else:
        last_player = players_table[-1]
        id = last_player['id']
        id += 1
    return id

def creation_joueurs(tournois):

    marvin = Joueur("decocq", "marvin", "20/07/98", "m", 1, tournois, 0, [], "")
    marvin2 = Joueur("chebany", "rocket", "20/07/98", "m", 3, tournois, 0, [], "")
    marvin3 = Joueur("dunoyer", "kahyss", "16/03/2019", "m", 10, tournois, 0, [], "")
    loan = Joueur("dunoyer", "loan", "01/11/00", "f", 100, tournois, 0, [], "")
    papa = Joueur("decocq", "martial", "13/10/71", "m", 41, tournois, 0, [], "")
    maman = Joueur("chebany", "angela", "16/03/2019", "f", 2, tournois, 0, [], "")
    mamie = Joueur("chebany", "henriette", "09/06/50", "f", 34, tournois, 0, [], "")
    papy = Joueur("chebany", "cheban", "12/04/44", "m", 68, tournois, 0, [], "")
    liste_des_joueurs = [marvin, marvin2, marvin3, loan, papa, maman, mamie, papy]
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    #players_table.truncate()
    for player in liste_des_joueurs:
        id = id_auto_increment()
        classement_aleatoire = random.randint(1,1000)
        serialized_player = {
            'nom':player.nom,
            'prenom':player.prenom,
            'date de naissance':player.date_de_naissance,
            'sexe':player.sexe,
            'classement':classement_aleatoire,
            'tournois':player.tournois,
            'points':player.points,
            'liste joueurs affrontes':player.joueurs_affrontes,
            'id':id
        }
        players_table.insert(serialized_player)
    print('\n')
    print('la liste des joueurs a bien été créé.')

def liste_id_for_each_players(tournois):
    db = TinyDB('db.json')
    players = db.table('Joueurs')
    q = Query()
    liste_id = []
    if tournois == "":
        for player in players.all():
            id = player['id']
            liste_id.append(id)
    else:
        players_of_tournament = players.search(q.tournois == tournois)
        for player in players_of_tournament:
            id = player['id']
            liste_id.append(id)
    return liste_id

print(liste_id_for_each_players("rocket league"))
def search_classement_by_id(id):

    db = TinyDB('db.json')
    players = db.table('Joueurs')
    q = Query()
    player = players.search(q.id == id)[0]
    classement = player['classement']
    return classement


