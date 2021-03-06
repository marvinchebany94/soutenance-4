# coding: utf-8
"""
Ce fichier va contenir toutes les fonctions du projet
"""
import sys
import os
from datetime import datetime
from tinydb import TinyDB, where, Query

current_path = sys.argv[0]
current_path = os.path.dirname(current_path)
current_path = os.path.dirname(current_path)
sys.path.append(current_path)
from modeles.modele import Matchs, Tournois, liste_des_tournois, Joueur, \
    liste_joueurs, Tours, id_auto_increment
from controle.verification import date_verification, test_choix_du_tournois, \
    verification_controle_du_temps, \
    verification_tournois_already_exists, sexe_verification, \
    classement_verification, nombre_de_jours_verification


def time_now():
    """
    La fonction sert à retourner la date et l'heure au moment de son
    utilisation
    :return: date et heure
    """
    date = datetime.now()
    date = date.strftime("%d-%m-%y %H:%M")
    return date


def creation_tournois():
    """
    La fonction va nous permettre de créer un tournois en entrant
    divers information.
    Chaque information est vérifiée via les fonctions de
    verification.py
    """
    i = 0
    dates = []
    while True:
        nom = input("Choisissez un nom pour le tournois : ")
        if nom == "":
            continue
        else:
            if verification_tournois_already_exists(nom):
                continue
            else:
                nom = nom.strip()
                break
    while True:
        lieu = input("Choisissez le lieu du tournois : ")
        if lieu == "":
            continue
        else:
            lieu = lieu.strip()
            break
    while True:
        nombre = input('Veuillez indiquer si le tournois sera sur \
un(1) ou plusieurs jours(2) : ')
        if not nombre_de_jours_verification(nombre):
            continue
        else:
            nombre = int(nombre)
            while i < nombre:
                i += 1
                print("Jour {} :".format(i))
                while True:
                    while True:
                        j = input("Entrez le jour du tournois (ex : 11) : ")
                        if j == "":
                            continue
                        else:
                            try:
                                j = int(j)
                                break
                            except ValueError:
                                print("valeur demandée invalide.")
                                continue
                    while True:
                        m = input("Entrez le mois du tournois (ex : 6) : ")
                        if m == "":
                            continue
                        else:
                            try:
                                m = int(m)
                                break
                            except ValueError:
                                print("Valeur demandée invalide.")
                                continue
                    while True:
                        a = input("Entrez l'année du tournois (ex : 2021) : ")
                        if a == "":
                            continue
                        else:
                            try:
                                a = int(a)
                                break
                            except ValueError:
                                print("Valide demandée invalide.")
                                continue
                    date = str(j) + "/" + str(m) + "/" + str(a)
                    if date_verification(j, m, a):
                        if date not in dates:
                            dates.append(date)
                            break
                        else:
                            print("la date que tu as créé existe déjà.")
                            continue
                    else:
                        continue
        break

    while True:
        controle_du_temps = input("Contrôle du temps (bullet, \
blitz ou coup rapide) : ")
        if controle_du_temps == "":
            continue
        else:
            controle_du_temps = verification_controle_du_temps(
                controle_du_temps)
            if not controle_du_temps:
                continue
            else:
                break
    while True:
        description = input("Si vous voulez ajouter une description \
au tournois : ")
        if description == "":
            continue
        else:
            break

    date_creation = time_now()
    date_de_creation = date_creation

    tournois = Tournois(nom=nom, lieu=lieu, date=dates, nombre_de_tours=4,
                        tournees=None,
                        controle_du_temps=controle_du_temps,
                        liste_des_joueurs=None, description=description,
                        date_de_creation=date_de_creation)

    db = TinyDB('db.json')
    tournois_table = db.table('Tournois')
    q = Query()
    serialized_tournois = {
        'nom': tournois.nom,
        'lieu': tournois.lieu,
        'date': tournois.date,
        'nombre de tours': tournois.nombre_de_tours,
        'tournees': tournois.tournees,
        'contrôle du temps': tournois.controle_du_temps,
        'liste des joueurs': tournois.liste_des_joueurs,
        'description': tournois.description,
        'date de creation': tournois.date_de_creation
    }
    tournois_table.insert(serialized_tournois)
    print("Le tournois a bien été créé et enregistré.")

    tournois_table = tournois_table.search(q.nom == tournois.nom)[0]

    print("""
Tournois : {}
Lieu : {}
Contrôle du temps : {}
Description : {}
    """.format(tournois_table['nom'], tournois_table['lieu'],
               tournois_table['contrôle du temps'],
               tournois_table['description']))

    if len(tournois_table['date']) == 1:
        print("Date : {}".format(tournois_table['date'][0]))
    else:
        debut = tournois_table['date'][0]
        fin = tournois_table['date'][1]
        print("""
Début : {}
Fin : {}
""".format(debut, fin))


def choix_du_tournois():
    """
    La fonction sera utilisée lorsque l'utilisateur voudra choisir un
    tournois afin d'y éffectuer
    des actions.
    :return: le tournois que l'utilisateur aura choisi
    """
    liste_tournois = liste_des_tournois(True)

    if liste_tournois == []:
        print("la liste des tournois est vide.")
    else:

        print("""
                Veuillez selectionner un tournois dans la liste suivante :
            """)

        for tournois in liste_tournois:
            print('- ', tournois)
        print('\n')

        while True:
            choix_du_tournois = input("Choix du tournois : ")
            if test_choix_du_tournois(choix_du_tournois):
                return choix_du_tournois
                break
            else:
                continue


def creation_liste_joueur(tournois):
    """
    La fonction servira à créer 8 joueurs pour un tournois choisi.
    La fonction repetera une boucle 8 fois afin d'y inscrire
    "les informations sur chaque joueur.
    Les informations seront testées par des fonctions de 'verification.py'
    """
    i = 0

    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()
    players_in_tournament = players_table.search(q.tournois == tournois)
    len_players = len(players_in_tournament)
    x = 8 - len_players
    print("Nombre de joueurs restants à créer : {}".format(x))
    while i < x:
        i += 1
        cmd = input('Entrez q pour quitter ou c pour continuer : ')
        if cmd == "q":
            break
        if cmd == "c":
            pass
        else:
            print("Mauvaise commande.")
        while True:
            nom = input("Nom de famille : ")
            if nom == "":
                continue
            else:
                nom = nom.strip()
                break
        while True:
            prenom = input("Prénom : ")
            if prenom == "":
                continue
            else:
                prenom = prenom.strip()
                break
        while True:
            date_de_naissance = input("Date de naissance (jj/mm/aa) : ")
            if date_de_naissance == "":
                continue
            else:
                try:
                    date_split = date_de_naissance.split('/')
                    if date_verification(int(date_split[0]),
                                         int(date_split[1]),
                                         int(date_split[2])):
                        break
                    else:
                        continue
                except ValueError:
                    print("Tu as mal rempli le champ.")
                    continue
        while True:
            sexe = input("sexe (m/f) : ")
            if sexe == "":
                continue
            else:
                if sexe_verification(sexe):
                    break
                else:
                    continue
        while True:
            classement = input("Classement : ")
            if classement == "":
                continue
            else:
                if not classement_verification(classement):
                    continue
                else:
                    classement = classement_verification(classement)
                    classement_unique(classement)
                    break

        points = 0
        joueurs_affrontes = []
        id = id_auto_increment()
        joueur = Joueur(nom, prenom, date_de_naissance, sexe, classement,
                        tournois, points, joueurs_affrontes, id)

        try:
            serialized_player = {
                'nom': joueur.nom,
                'prenom': joueur.prenom,
                'date de naissance': joueur.date_de_naissance,
                'sexe': joueur.sexe,
                'classement': joueur.classement,
                'tournois': joueur.tournois,
                'points': joueur.points,
                'liste joueurs affrontes': joueur.joueurs_affrontes,
                'id': joueur.id
            }

            players_table.insert(serialized_player)

            print("Le joueur {} {} a bien été enregistré dans la base de \
données."
                  .format(joueur.nom, joueur.prenom))
        except ValueError:
            print("Le joueur n'a pas été enregistré dans la base de données.")


def add_players_to_tournament(tournois):
    """
    La fonction prend en paramètre le tournois auquel vous voulez ajouter
    des joueurs.
    Chaque tournois à une liste de joueurs au départ vide, la fonction
    utilisera la fonction
    liste_joueurs() qui retournera la liste des joueurs d'un tournois,
    puis fera un update de 'liste des joueurs'
    en y insérant la liste.
    """
    db = TinyDB('db.json')
    tournois_table = db.table('Tournois')
    q = Query()
    liste_des_joueurs = liste_joueurs(tournois)

    try:
        tournois_table.update({'liste des joueurs': liste_des_joueurs},
                              q.nom == tournois)
    except IndexError:
        print("Les joueurs n'ont pas été enregistré dans la base de\
données du tournois")


def search_player_by_id(id):
    """
    La fonction va retourner une variable avec le nom et prénom d'une
    personne en fonction de l'id en paramètre
    :param id: l'id dont on souhaite prendre des informations,
    l'id doit être un chiffre
    :return: la variable nom_prenom
    """
    db = TinyDB('db.json')
    players = db.table('Joueurs')
    q = Query()
    player = players.search(q.id == id)[0]
    nom_prenom = player['nom'] + " " + player['prenom']
    return nom_prenom


def creation_paires(id):
    """
    la fonction va créer 2 listes, les 4 meilleurs joueurs
    et les 4 moins bons.
    Dans un second temps elle va associer le 1er joueur de la
    1ère liste avec le 1er de la deuxième et
    ainsi de suite.
    Cette fonction sert seulement pour le premier tour et non les 3 autres.
    :return: une liste contenant 4 listes contenant les 4 paires avec
    le nom / prénom pour chaque joueur
    """

    liste_ordre_classement = liste_acteurs_odre_de_classement(id, False)
    premier_groupe = liste_ordre_classement[0:4]
    deuxieme_groupe = liste_ordre_classement[4:8]

    paire_1 = (premier_groupe[0], deuxieme_groupe[0])
    paire_2 = (premier_groupe[1], deuxieme_groupe[1])
    paire_3 = (premier_groupe[2], deuxieme_groupe[2])
    paire_4 = (premier_groupe[3], deuxieme_groupe[3])

    print("""
        Liste des matchs pour le tour 1 :
                {}
            {} vs {}
                {}
            {} vs {}
                {}
            {} vs {}
                {}
            {} vs {}
    """.format('\n',
               search_player_by_id(paire_1[0]),
               search_player_by_id(paire_1[1]),
               '\n',
               search_player_by_id(paire_2[0]),
               search_player_by_id(paire_2[1]),
               '\n',
               search_player_by_id(paire_3[0]),
               search_player_by_id(paire_3[1]),
               '\n',
               search_player_by_id(paire_4[0]),
               search_player_by_id(paire_4[1])))

    return [paire_1, paire_2, paire_3, paire_4]


def matchs(tournois, paires):
    """
    Pour chaque paire la fonction va demander un score seulement pour le
     joueur qui se trouve à gauche, puis selon ce score là,
     elle s'adaptera et créra le résultat du deuxième adversaire.
    elle va ensuite utiliser la fonction update_points_joueur()
    qui servira à mettre à jour le nombre de points d'un joueur
    puis utiliser update_joueurs_affrontes() afin d'ajouter le
    joueur affronté dans la liste des joueurs affrontès pour
    chaque joueurs.
    Chaque tuple sera ensuite inseré dans la table des
    matchs dans la base de données.
    :param tournois: tournois pour lequel nous allons
    créer des matchs
    :param paires: liste des 4 paires retournées par creation_paires()
     ou creating_paires() selon le tour
    :return: la liste de tous les matchs qui ont été enregistré
    """
    tournois = tournois
    liste_matchs = []

    db = TinyDB('db.json')
    matchs_table = db.table('Matchs')
    players_table = db.table('Joueurs')
    q = Query()
    for paire in paires:

        joueur_1 = players_table.search(q.id == paire[0])[0]
        joueur_1 = joueur_1['nom'] + " " + joueur_1['prenom']
        joueur_2 = players_table.search(q.id == paire[1])[0]
        joueur_2 = joueur_2['nom'] + " " + joueur_2['prenom']

        print("""
            Match :
                {} vs {}
            """.format(joueur_1, joueur_2))

        while True:
            scores = [0, 0.5, 1]
            score_1 = input("Veuillez entrer le score du joueur à gauche :")
            if score_1 == "":
                continue
            else:
                if score_1 == "1" or score_1 == "0":
                    score_1 = int(score_1)
                else:
                    score_1 = float(score_1)
                if score_1 not in scores:
                    print("Le score indiqué n'est pas bon.")
                    continue
                else:
                    if score_1 == 0:
                        score_2 = 1
                        score_2 = int(score_2)
                        break
                    if score_1 == 1:
                        score_2 = 0
                        score_2 = int(score_2)
                        break
                    if score_1 == 0.5:
                        score_2 = 0.5
                        score_2 = float(score_2)
                        break

        update_points_joueurs(joueur_1, tournois, score_1)
        update_points_joueurs(joueur_2, tournois, score_2)

        update_joueurs_affrontes(paire[0], paire[1])
        update_joueurs_affrontes(paire[1], paire[0])

        tuple = ([joueur_1, score_1], [joueur_2, score_2])
        liste_matchs.append(tuple)

    for m in liste_matchs[0:4]:
        tuple_match = Matchs(paire=m, tournois=tournois)

        match_serialized = {
            'paire': tuple_match.paire,
            'tournois': tuple_match.tournois
        }
        matchs_table.insert(match_serialized)

    i = 0
    for match in matchs_table.all()[-4:len(matchs_table)]:
        i += 1
        liste_matchs.append(match)
        joueur_1 = match['paire'][0][0]
        joueur_2 = match['paire'][1][0]
        score_1 = match['paire'][0][1]
        if score_1 == 1:
            vainqueur = joueur_1
        elif score_1 == 0.5:
            vainqueur = 'match nul'
        else:
            vainqueur = joueur_2
        print("""
            match {} :
                {} vs {}
            Vainqueur :
                {}
        """.format(i, joueur_1, joueur_2, vainqueur))

    return liste_matchs[0:4]


def creation_tour(tournois, liste_matchs, debut):
    """
    La fonction vérifie l'existence d'un tour pour un tournois donné.
    Si aucun tour n'est renvoyé la fonction va créer le premier tour.
    Si un tour existe déjà, la fonction va prendre le chiffre du dernier
     tour, et lui ajouter 1 afin de créer le tour suivant.
    :param tournois: Tounrois pour lequel le tour doit être créé
    :param liste_matchs: la liste des matchs qui doivent être
    insérés dans la table des tours.
    :return: Un message disant que le tour X a bien été enregistré +
    un aperçu de la colonne qui correspond au tour dans
    la base de données.
    """

    db = TinyDB('db.json')
    tours_table = db.table('Tours')
    q = Query()

    resultat = tours_table.search(where('tournois') == tournois)

    if not resultat:
        fin = time_now()
        tour = Tours(nom='Round 1', debut=debut, fin=fin,
                     match=liste_matchs, tournois=tournois)
        tour_serialized = {
            'nom': tour.nom,
            'debut': tour.debut,
            'fin': tour.fin,
            'match': tour.match,
            'tournois': tour.tournois

        }
        tours_table.insert(tour_serialized)
        tours_table = tours_table.search(where('tournois') == tournois)[-1]
        print("Le {} a bien été enregistré.".format(tour.nom))

    else:
        find_last_round = tours_table.search(q.tournois == tournois)[-1]
        round_number = int(find_last_round['nom'][-1])
        round_number += 1
        nom = "Round " + str(round_number)
        fin = time_now()
        tour = Tours(nom=nom, debut=debut, fin=fin, match=liste_matchs,
                     tournois=tournois)
        tour_serialized = {
            'nom': tour.nom,
            'debut': tour.debut,
            'fin': tour.fin,
            'match': tour.match,
            'tournois': tour.tournois

        }
        tours_table.insert(tour_serialized)
        tours_table = tours_table.search(where('tournois') == tournois)[-1]
        print("""
            Le {} a bien été enregistré.
        """.format(tour.nom))


def classement_unique(classement):
    """
    La fonction va voir si un classement est déjà associé à un joueur,
    dans ce cas là la fonction va ajouter +1 au
    classement de la personne en quesrion afin de ne pas avoir des joueurs
     avec le même classement dans la base de données.
    :param classement: le classement à tester
    """
    classement = int(classement)
    db = TinyDB('db.json')
    players = db.table('Joueurs')
    q = Query()
    while True:
        try:
            player = players.search(q.classement == classement)[0]
        except IndexError:
            break
        nouveau_classement = player['classement'] + 1
        classement_unique(nouveau_classement)
        players.update({'classement': nouveau_classement},
                       (q.classement == classement))


def changer_classement_joueurs(tournois):
    """
    La fonction va montrer la liste de tous les joueurs présents dans la
    base de données, puis demander à l'utilisateur d'en choisir un.
    La fonction va lui montrer les données de la personne, puis lui demander
     de changer son classement.
    Le classement choisi par l'utilisateur sera vérifié via la fonction
    classement_verification()
    Si tout est ok, la fonction va mettre à jour le classement de la personne.
    :return: Retourne la colonne dans la base de données correspondant
    au joueur choisi.
    """
    db = TinyDB('db.json')
    players_table = db.table("Joueurs")
    q = Query()

    print("Voici la liste des joueurs dans le tournois ' {} '  :"
          .format(tournois))
    for joueur in liste_joueurs(tournois):
        print('- ', joueur)
    print('\n')
    while True:
        nom_prenom = input("Choisissez la personne à qui vous voulez \
modifier le classement : ")
        if nom_prenom not in liste_joueurs(tournois):
            continue
        else:
            nom_prenom = nom_prenom.split(" ")
            break
    try:
        player = players_table.search((q.nom == nom_prenom[0])
                                      & (q.prenom == nom_prenom[1])
                                      & (q.tournois == tournois))[0]
        print("""
            Nom : {}
            Prénom : {}
            classement : {}
        """.format(player['nom'], player['prenom'], player['classement']))

        while True:
            nouveau_classement = input('Entre le nouveau classement : ')
            if nouveau_classement == "":
                continue
            else:
                nouveau_classement = classement_verification(
                    nouveau_classement)
                if not nouveau_classement:
                    continue
                else:
                    classement_unique(nouveau_classement)
                    break

        players_table.update({'classement': nouveau_classement},
                             ((q.nom == nom_prenom[0])
                              & (q.prenom == nom_prenom[1])
                              & (q.tournois == tournois)))
        player = players_table.search((q.nom == nom_prenom[0])
                                      & (q.prenom == nom_prenom[1])
                                      & (q.tournois == tournois))[0]
        print("""
Le classement a été mis à jour :
    Nom : {}
    Prénom : {}
    Nouveau classement : {}
""".format(player['nom'], player['prenom'], player['classement']))

    except IndexError:
        print("La personne n'existe pas dans la base de données.")


def update_points_joueurs(joueur, tournois, point_a_ajouter):
    """
    la fonction va chercher la colonne d'un joueur dans la
    table des Joueurs.
    Elle va additioner les points actuels avec les points à ajouter.
    Puis faire une mise à jours des points du joueurs, et
    l'enregistrer dans la base de données.
    :param joueur: Joueur auquel on va ajouter des points
    :param point_a_ajouter: Nombre de points à lui ajouter
    :return: le nombre de points que le joueur a après la
    mise à jours de la base de données.
    """
    joueur = joueur.split()
    nom = joueur[0]
    prenom = joueur[1]
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()
    query_player = players_table.search((q.nom == nom)
                                        & (q.prenom == prenom)
                                        & (q.tournois == tournois))[0]
    points_actuels = query_player['points']
    points_finaux = points_actuels + point_a_ajouter
    players_table.update({'points': points_finaux},
                         ((q.nom == nom)
                          & (q.prenom == prenom)
                          & (q.tournois == tournois)))
    query_player = players_table.search((q.nom == nom)
                                        & (q.prenom == prenom)
                                        & (q.tournois == tournois))[0]

    return query_player['points']


def search_classement_by_id(id):
    """
    La fonction va cherche le classement d'une personne selon son id.
    :param id: L'id sur lequel la fonction fera la recherche.
    :return:Le classement qui a été trouvé après la recherche.
    """
    db = TinyDB('db.json')
    players = db.table('Joueurs')
    q = Query()
    player = players.search(q.id == id)[0]
    classement = player['classement']

    return classement


def search_player_by_classement(classement):
    """
    la fonction va chercher le nom et prénom d'une personne en fonction
     du classement passé en paramétre
    :param classement: Le classement de la personne dont on recherche
    le nom et prénom
    :return: nom et prénom de la personne trouvée
    """
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()

    player = players_table.search(q.classement == classement)[0]
    player_identite = player['nom'] + " " + player['prenom']

    return player_identite


def liste_acteurs_odre_de_classement(id, show_liste):
    """
    La fonction retourne la liste des acteurs par ordre de classement.
    :param id: liste des id des joueurs que l'on veut trier
    :return: la liste triée par ordre de classement contrnant
    l'id des joueurs
    """
    liste_classement_joueur = []
    for i in id:
        classement = search_classement_by_id(i)
        liste_classement_joueur.append(classement)

    liste_joueur_ordre_croissant = sorted(liste_classement_joueur)
    liste_acteurs_odre_de_classement = []
    for classement in liste_joueur_ordre_croissant:
        db = TinyDB('db.json')
        players = db.table('Joueurs')
        q = Query()
        player = players.search(q.classement == classement)[0]
        id = player['id']
        if show_liste:
            nom = player['nom']
            prenom = player['prenom']
            classement = player['classement']
            tournois = player['tournois']
            print("""
                Nom : {}
                Prénom : {}
                Classement : {}
                Tournois : {}
            """.format(nom, prenom, classement, tournois))
        else:
            pass
        liste_acteurs_odre_de_classement.append(id)

    return liste_acteurs_odre_de_classement


def liste_matchs_d_un_tournois(tournois):
    """
    La fonction va rerchercher tous les matchs concernant un
    tournois précis.
    Elle va renvoyer pour chacun des matchs un print avec les
    2 joueurs, et le vainqueur.
    :param tournois: tournois pour lequel nous cherchons la
    liste des matchs
    :return: la liste de tous les matchs du tournois
    """
    db = TinyDB('db.json')
    matchs_table = db.table('Matchs')
    q = Query()
    all_matchs = matchs_table.search(q.tournois == tournois)
    liste_matchs = []
    i = 0
    for match in all_matchs:
        i += 1
        liste_matchs.append(match)
        joueur_1 = match['paire'][0][0]
        joueur_2 = match['paire'][1][0]
        score_1 = match['paire'][0][1]
        if score_1 == 1:
            vainqueur = joueur_1
        elif score_1 == 0.5:
            print("""
            match {} :
                {} vs {}
                Match Nul
                    """.format(i, joueur_1, joueur_2))
        else:
            vainqueur = joueur_2
        print("""
            match {} :
                {} vs {}
            Vainqueur :
                {}
        """.format(i, joueur_1, joueur_2, vainqueur))
    return liste_matchs


def liste_tours_d_un_tournois(tournois):
    """
    La fonction renvoit la liste de tous les tours d'un tournois
    spécifique.
    :param tournois: Tournois pour lequel le script va chercher
    les tours.
    :return: Le script renvoit la colonne correspondant à chaque
    tours.
    """
    db = TinyDB('db.json')
    tours_table = db.table('Tours')
    q = Query()
    all_tours = tours_table.search(q.tournois == tournois)
    i = 0
    for tour in all_tours:
        print("""
            {} :
            Début : {}
            Fin : {}
        """.format(tour['nom'], tour['debut'], tour['fin']))

        for match in tour['match']:
            i += 1
            joueur_1 = match[0][0]
            joueur_2 = match[1][0]
            score_1 = match[0][1]
            if score_1 == 1:
                vainqueur = joueur_1
            elif score_1 == 0.5:
                vainqueur = 'match nul'
            else:
                vainqueur = joueur_2
            print("""
                    match {} :
                        {} vs {}
                    Vainqueur :
                        {}
                    """.format(i, joueur_1, joueur_2, vainqueur))
        print('\n')


def liste_triee(liste_joueurs, tournois):
    """
    la fonction va placer les joueurs selon leurs points dans plusieurs
    listes, puis va trier ces listes dans l'ordre
    croissant, puis former une liste finale correspondantà une liste
    trièe par ordre croissant.
    :param liste_joueurs: la liste comportant le nom et prénom de chaque
    jours que vous voulez trier.
    :return: la liste liste_triee qui contient les id des joueurs
    """
    groupe_4_pts = []
    groupe_3_5_pts = []
    groupe_3_pts = []
    groupe_2_5_pts = []
    groupe_2_pts = []
    groupe_1_5_pts = []
    groupe_1_pts = []
    groupe_0_5_pts = []
    groupe_0_pts = []
    listes = [groupe_4_pts, groupe_3_5_pts, groupe_3_pts, groupe_2_5_pts,
              groupe_2_pts, groupe_1_5_pts, groupe_1_pts, groupe_0_5_pts,
              groupe_0_pts]

    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()

    for player in liste_joueurs:
        p = player.split()
        nom = p[0]
        prenom = p[1]
        player_query = players_table.search((q.nom == nom)
                                            & (q.prenom == prenom)
                                            & (q.tournois == tournois))[0]
        player_points = player_query['points']
        id = player_query['id']
        if player_points == 0:
            groupe_0_pts.append(id)
        if player_points == 0.5:
            groupe_0_5_pts.append(id)
        if player_points == 1:
            groupe_1_pts.append(id)
        if player_points == 1.5:
            groupe_1_5_pts.append(id)
        if player_points == 2:
            groupe_2_pts.append(id)
        if player_points == 2.5:
            groupe_1_pts.append(id)
        if player_points == 3:
            groupe_3_pts.append(id)
        if player_points == 3.5:
            groupe_3_5_pts.append(id)
        if player_points == 4:
            groupe_4_pts.append(id)
    liste_triee = []
    for liste in listes:

        if len(liste) == 1:
            liste_triee += liste
        elif len(liste) == 0:
            pass
        else:
            liste_ordre_croissant = liste_acteurs_odre_de_classement(
                liste, False)
            liste_triee += liste_ordre_croissant

    return liste_triee


def update_joueurs_affrontes(joueur, joueur_a_ajouter):
    """
    La fonction va mettre à jours la liste des joueurs affrontés
    par un joueur.
    :param joueur: l'id du joueur auquel on va ajouter un joueur
    :param joueur_a_ajouter: id du joueur que l'on va ajouter dans
    la liste des joueurs affrontes du joueur en question
    """
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()
    player = players_table.search(q.id == joueur)[0]
    joueur_a_ajouter = players_table.search(q.id == joueur_a_ajouter)[0]
    joueur_a_ajouter = joueur_a_ajouter['prenom'] + " " +\
                                                    joueur_a_ajouter['nom']

    liste_joueur_to_add = []
    if player['liste joueurs affrontes'] == []:
        pass
    else:
        for p in player['liste joueurs affrontes']:
            liste_joueur_to_add.append(p)

    liste_joueur_to_add.append(joueur_a_ajouter)
    players_table.update(
        {'liste joueurs affrontes': liste_joueur_to_add},
        (q.id == joueur))


def liste_joueurs_affrontes(joueur):
    """
    La fonction va chercher la liste des joueurs affrontès par un joueur,
     puis nous la retourner.
    :param joueur: id du joueur pour lequel la fonction va retourner la
    liste des joueurs affrontes
    :return: une liste contenant le nom et prénom de tous les joueurs
    affrontès par le joueur
    """
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()

    player = players_table.search(q.id == joueur)[0]
    liste_joueurs_affrontes = player['liste joueurs affrontes']

    return liste_joueurs_affrontes


def etape_3_4_systeme_suisse(liste_joueurs, tournois):
    """
    la fonction correspond à l'étape 3 et 4 du système suisse.
    Pour créer une paire on va faire joueur 1 vs joueur 2, si le joueur 2 a
    déjà été affronté par le joueur 1,
    alors le joueur 1 affronte le 3, et ainsi de suite.
    lorsqu'une paire est créée, les 2 joueurs sont supprimés de la liste,
    et l'algorithme fait la même chose pour les
    joueurs 1 et 2 de la nouvelle liste.
    :param liste_joueurs: liste des joueurs triès par la fonction liste_triee()
    :param tournois: tournois en question
    :return: la liste des joueurs après la suppression des 2 items, et
    la paire créée contenant nom et prénom des 2
    joueurs
    """
    liste = liste_joueurs
    liste_joueurs_affrontes_par_j1 = liste_joueurs_affrontes(liste[0])
    i = 1

    while True:
        db = TinyDB('db.json')
        joueurs = db.table('Joueurs')
        q = Query()
        joueur = joueurs.search(q.id == liste[i])[0]
        prenom_nom = joueur['prenom'] + " " + joueur['nom']
        if prenom_nom not in liste_joueurs_affrontes_par_j1:
            paire = [liste[0], liste[i]]
            liste.remove(liste[0])
            liste.remove(liste[i - 1])
            break
        else:
            i += 1
            continue
    return liste, paire


def nombre_de_tours(tournois):
    """
    La fonction va chercher le nombre de tour d'un tournois.
    :param tournois: tournois pour lequel on va faire la recherche
    :return: le chiffre qui corrspondra au tour suivant
    """
    db = TinyDB('db.json')
    table = db.table('Tours')
    q = Query()
    table_recherche = table.search(q.tournois == tournois)
    resultat = len(table_recherche) + 1
    return resultat


def creating_paires(tournois, liste_joueurs):
    """
    Pour chaque paire on utilise la fonction etape_3_4_systeme_suisse()
    qui nous renvoit une paire + une nouvelle liste.
    On fait ça 4 fois afin d'avoir nos 4 paires
    :param tournois: tournois en question
    :param liste_joueurs: liste des joueurs contenant pour chaque
    joueur un nom et prénom
    :return: les 4 paires contenant le nom et prénom des 2 adversaires.
    Ces paires seront utilisées dans la fonction
    matchs()
    """

    paire_1 = etape_3_4_systeme_suisse(liste_joueurs, tournois)
    nouvelle_liste = paire_1[0]

    paire_2 = etape_3_4_systeme_suisse(nouvelle_liste, tournois)
    nouvelle_liste = paire_2[0]

    paire_3 = etape_3_4_systeme_suisse(nouvelle_liste, tournois)
    nouvelle_liste = paire_3[0]

    paire_4 = [nouvelle_liste[0], nouvelle_liste[1]]

    tour = nombre_de_tours(tournois)

    print("""
        Liste des matchs pour le tour {} :

            {} vs {}

            {} vs {}

            {} vs {}

            {} vs {}
    """.format(tour, search_player_by_id(paire_1[1][0]),
               search_player_by_id(paire_1[1][1]),
               search_player_by_id(paire_2[1][0]),
               search_player_by_id(paire_2[1][1]),
               search_player_by_id(paire_3[1][0]),
               search_player_by_id(paire_3[1][1]),
               search_player_by_id(paire_4[0]),
               search_player_by_id(paire_4[1])))

    return paire_1[1], paire_2[1], paire_3[1], paire_4


def voir_les_points_des_joueurs(liste_id):
    """
    La fonction va écrire le nom et prénom de la personne
    suivi par son nombre de points.
    """
    db = TinyDB('db.json')
    joueurs = db.table('Joueurs')
    q = Query()
    for id in liste_id:
        joueur = joueurs.search(q.id == id)[0]
        nom_prenom = joueur['nom'] + " " + joueur['prenom']
        points = joueur['points']
        print("{} : {}".format(nom_prenom, points))