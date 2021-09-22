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


def liste_des_tournois(voir_la_liste):
    """
    La fonction retourne une liste contenant le nom de tous les tournois dans la base de données.
    La fonction est aussi capable d'écrire le nom, date et lieu pour chaque tournois en fonction de si True est passé en
    paramètre ou non
    :param voir_la_liste: Prend la valeur True ou False. True permet d'avoir le détail de chaque tournois grâce au print
    , False retourne seulement la liste contenant le nom de tous les tournois
    :return: une liste contenant le nom de tous les tournois
    """
    db = TinyDB('db.json')
    Tournois_table = db.table('Tournois')
    Tournois_table = Tournois_table.all()
    liste_tournois = []
    for tournois in Tournois_table:
        nom = tournois['nom']
        date = tournois['date']
        ville = tournois['lieu']
        controle_du_temps = tournois['contrôle du temps']
        if voir_la_liste:
            print("""
                tournois : {}
                date : {}
                lieu : {}
                contrôle du temps : {}
            """.format(nom, date, ville, controle_du_temps))
        else:
            pass
        liste_tournois.append(tournois['nom'])
    return liste_tournois


def liste_joueurs(tournois):
    """
    La fonction va chercher la liste de tous les joueurs présents dans un tournois.
    Si tournois == "", la fonction fera une recherche sur la totalité de la base de données, si un nom de tournois est
    renseigné, la fonction prendra le nom et prénom de tous les joueurs associés à celui*ci.
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
    La fonction retourne la liste des joueurs par ordre alphabétique selon un tournois ou pour tous les joueurs présents
    dans la base de données, et retourne un print avec le nom, prénom, classement et le tournois associé au joueur.
    :param liste_id: la liste des joueurs que l'on souhaite trier via leur id
    :param tournois: Le tournois pour lequel on va trier la liste des joueurs
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
                tournois = p['tournois']
                tuple = (nom_prenom, classement)
                if tuple not in joueur_deja_print:
                    joueur_deja_print.append(tuple)
                    print("""
                        Nom : {}
                        Prénom : {}
                        Classement : {}
                        Tournois : {}
                    """.format(nom, prenom, classement, tournois))
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
    """
    La fonction sert à incrémenter l'id de chaque joueurs. Chaque joueurs doit avoir un id unique, ainsi la fonction
    va chercher le dernier en id dans le base de données et lui ajouter 1.
    :return: retorune l'id qui sera donné au prochain joueur entré dans la base de données.
    """
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
    """
    La fonction sert à créer 8 joueurs qui auront les mêmes attributs mais un id et un classement différents.
    Elle est utilisée pour créer une liste de joueurs qui sera assigné automatiquement au tournois que vous avez choisi.
    :param tournois:
    :return: Un print disant que tous les joueurs ont bien été créé.
    """
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
    """
    La fonction sert à avoir la liste des id de tous les joueurs dans la base de données ou de ceux d'un tournois
    spécifique.
    :param tournois: si tournois == "" la fonction prendra l'id de tous les joueurs de la base de données, sinon la
    fonction cherchera les id de tous les joueurs d'un tournois.
    :return: retourne une liste qui contient tous les id
    """
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


def search_classement_by_id(id):
    """
    La fonction va rechercher le classement d'un joueur selon son id.
    :param id: la fonction prend un chiffre en paramètre
    :return: retourne un int correspondant au classement associé à l'id
    """

    db = TinyDB('db.json')
    players = db.table('Joueurs')
    q = Query()
    player = players.search(q.id == id)[0]
    classement = player['classement']
    return classement


