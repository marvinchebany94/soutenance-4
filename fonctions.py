"""
Ce fichier va contenir toutes les fonctions du projet
"""
import random
from tinydb import TinyDB, where, Query
from datetime import datetime
from modele import Matchs, Tournois, liste_des_tournois, Joueur, liste_joueurs, Tours
from verification import champ_vide, date_verification, test_choix_du_tournois, verification_controle_du_temps,\
    verification_tournois_already_exists, sexe_verification, classement_verification

def time_now():
    date = datetime.now()
    date = date.strftime("%d-%m-%y %H:%M")
    return date

def creation_tournois():
    #nom lieu date joueurs

    nom = input("Choisissez un nom pour le tournois : ")
    champ_vide(nom)
    verification_tournois_already_exists(nom)

    lieu = input("Choisissez le lieu du tournois : ")
    champ_vide(lieu)

    j = input("Entrez le jour du tournois (ex : 11) : ")
    champ_vide(j)
    j = int(j)

    m = input("Entrez le mois du tournois (ex : 6) : ")
    champ_vide(m)
    m = int(m)

    a = input("Entrez l'année du tournois (ex : 2021) : ")
    champ_vide(a)
    a = int(a)

    date = str(j) + "/" + str(m) + "/" + str(a)

    date_verification(j,m,a)

    controle_du_temps = input("Contrôle du temps (bullet, blitz ou coup rapide) : ")
    champ_vide(controle_du_temps)
    controle_du_temps = verification_controle_du_temps(controle_du_temps)

    description = input("Si vous voulez ajouter une description au tournois : ")

    date = time_now()
    date_de_creation = date

    tournois = Tournois(nom=nom, lieu=lieu, date=date, nombre_de_tours=4, tournees=None,
                        controle_du_temps=controle_du_temps, liste_des_joueurs=None, description=description,
                        date_de_creation=date_de_creation)

    db = TinyDB('db.json')
    tournois_table = db.table('Tournois')
    serialized_tournois = {
        'nom':tournois.nom,
        'lieu':tournois.lieu,
        'date':tournois.date,
        'nombre de tours':tournois.nombre_de_tours,
        'tournees':tournois.tournees,
        'contrôle du temps':tournois.controle_du_temps,
        'liste des joueurs':tournois.liste_des_joueurs,
        'description':tournois.description,
        'date de creation':tournois.date_de_creation
        }
    tournois_table.insert(serialized_tournois)
    tournois_table = tournois_table.search(where('nom') == tournois.nom)

    print(tournois_table)

    print("Le tournois a bien été créé et enregistré.")

def choix_du_tournois():
    liste_tournois = liste_des_tournois()


    print("""
            Veuillez selectionner un tournois dans la liste suivante :
            {}
        """.format(liste_tournois))

    choix_du_tournois = input("Choix du tournois : ")
    test_choix_du_tournois(choix_du_tournois)
    return choix_du_tournois


def creation_liste_joueur():
    i = 0

    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    players_table.truncate()

    while i < 8:
        i += 1

        nom = input("Nom de famille : ")
        nom = champ_vide(nom)

        prenom = input("Prénom : ")
        prenom = champ_vide(prenom)

        date_de_naissance = input("Date de naissance (jj/mm/aa) : ")
        date_de_naissance = champ_vide(date_de_naissance)

        sexe = input("sexe (m/f) : ")
        sexe = champ_vide(sexe)
        sexe_verification(sexe)

        classement = input("Classement : ")
        classement = champ_vide(classement)
        classement = classement_verification(classement)

        tournois = choix_du_tournois

        joueur = Joueur(nom, prenom, date_de_naissance, sexe, classement, tournois)

        #on enregistre le joueur ici
        try:

            print(players_table.all())
            serialized_player = {
                'nom':joueur.nom,
                'prenom':joueur.prenom,
                'date de naissance':joueur.date_de_naissance,
                'sexe':joueur.sexe,
                'classement':joueur.classement,
                'tournois':joueur.tournois
            }

            players_table.insert(serialized_player)

            print("""
                Le joueur {} {} a bien été enregistré dans la base de données.        
            """.format(joueur.nom, joueur.prenom))
        except:
            print("Le joueur n'a pas été enregistré dans la base de données.")

        print(players_table.all())
    return choix_du_tournois

def add_players_to_tournament(tournois):
    db = TinyDB('db.json')
    tournois_table = db.table('Tournois')
    q = Query()
    tournois_find = tournois_table.search(q.nom == tournois)[0]
    liste_des_joueurs = liste_joueurs()

    try:
        tournois_table.update({'liste des joueurs':liste_des_joueurs}, q.nom == tournois)
    except:
        print("Les joueurs n'ont pas été enregistré dans la base de données du tournois")

    print(tournois_table)

def creation_paires():
    """
    la fonction va créer 2 listes, les 4 meilleurs joueurs et les 4 moins bons.
    Dans un second temps elle va associer le 1er joueur de la 1ère liste avec le 1er de la deuxième et
    ainsi de suite.
    Au prochain tour, triez tous les joueurs en fonction de leur nombre total de points. Si plusieurs joueurs ont le
    même nombre de points, triez-les en fonction de leur rang.
    Associez le joueur 1 avec le joueur 2, le joueur 3 avec le joueur 4, et ainsi de suite. Si le joueur 1 a déjà joué
    contre le joueur 2, associez-le plutôt au joueur 3.
    :param liste_joueur:
    :return:
    """
    #on crée une liste contenant seulement le classement des joueurs
    liste_classement_joueur = []
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    for item in players_table:
        item = int(item['classement'])
        liste_classement_joueur.append(item)

    #on trie la liste en la mettant par ordre croissant
    liste_joueur_classement_croissant = sorted(liste_classement_joueur)
    print(liste_joueur_classement_croissant)

    #on reprend la liste classée par ordre croissant, puis on associe le rang des personnes à leur prénoms
    liste_classement_joueur_avec_nom = []

    for classement in liste_joueur_classement_croissant:

        #on va chercher la personne qui a le classement dans la base de donnée, player_infos va ressortir la
        #base de donnée qui correspond à celle-ci
        player_infos = players_table.search(where('classement') == classement)#str(classement))
        #on crée une boucle for pour prendre seulement le prénom et l'ajouter à la liste
        for infos in player_infos:
            print(infos['prenom'])
            prenom_nom = infos['prenom'] + " " + infos['nom']
            liste_classement_joueur_avec_nom.append(prenom_nom)

    #on crée les 2 groupes
    premier_groupe = liste_classement_joueur_avec_nom[0:4]
    print(premier_groupe)
    deuxieme_groupe = liste_classement_joueur_avec_nom[4:8]
    print(deuxieme_groupe)

    #on crée les 4 paires
    paire_1 = (premier_groupe[0], deuxieme_groupe[0])
    paire_2 = (premier_groupe[1], deuxieme_groupe[1])
    paire_3 = (premier_groupe[2], deuxieme_groupe[2])
    paire_4 = (premier_groupe[3], deuxieme_groupe[3])

    #on retourne la liste des 4 paires
    return [paire_1, paire_2, paire_3, paire_4]

#création de la fonction qui va créer des paires en fonctions de leur point ou classement
def creation_paires_tour_1():
    #on reprend la liste de tous les matchs afin d'avoir le score de chacun
    db = TinyDB('db.json')
    matchs_table = db.table('Matchs')
    players_table = db.table('Joueurs')
    liste_joueurs_1_point = []
    liste_joueurs_0_5_point = []
    liste_joueurs_0_point = []

    liste_croissante_joueur_1_point = []
    liste_finale_joueur_1_point = []
    liste_croissante_joueur_0_point = []
    liste_finale_joueur_0_point = []
    liste_finale = []

    for match in matchs_table:
        joueur_1 = match['paire'][0]
        joueur_2 = match['paire'][1]
        point_joueur_1 = match['paire'][0][1]
        point_joueur_2 = match['paire'][1][1]
        if point_joueur_1 == 1:
            liste_joueurs_1_point.append(joueur_1)
        else:
            liste_joueurs_0_point.append(joueur_1)
        if point_joueur_2 == 1:
            liste_joueurs_1_point.append(joueur_2)
        else:
            liste_joueurs_0_point.append(joueur_2)

    print("liste des joueurs à 1 points : {}".format(liste_joueurs_1_point))
    print("liste des joueurs à 0 point : {}".format(liste_joueurs_0_point))

    #on va chercher le classement des joueurs pour chaque groupe afin de les trier selon ça
    #groupe pour les joueurs à 1 point:
    for joueur in liste_joueurs_1_point:
        nom_prenom = joueur[0]
        nom = nom_prenom.split()[1]
        prenom = nom_prenom.split()[0]

        recherche_classement = players_table.search(where('nom') == nom)

        for resultat in recherche_classement:
            if resultat['prenom'] == prenom:
                classement = int(resultat['classement'])
                liste_croissante_joueur_1_point.append(classement)
            else:
                pass

    liste_croissante_joueur_1_point = sorted(liste_croissante_joueur_1_point)
    print(liste_croissante_joueur_1_point)

    for classement in liste_croissante_joueur_1_point:
        recherche_prenom_nom = players_table.search(where('classement') == classement)[0]
        nom_prenom = recherche_prenom_nom['nom'] + " " + recherche_prenom_nom['prenom']
        liste_finale_joueur_1_point.append(nom_prenom)

    print(liste_finale_joueur_1_point)


    #groupe pour les joueurs à 0 point :

    for joueur in liste_joueurs_0_point:
        nom_prenom = joueur[0]
        nom = nom_prenom.split()[1]
        prenom = nom_prenom.split()[0]

        recherche_classement = players_table.search(where('nom') == nom)

        for resultat in recherche_classement:
            if resultat['prenom'] == prenom:
                classement = int(resultat['classement'])
                liste_croissante_joueur_0_point.append(classement)
            else:
                pass

    liste_croissante_joueur_0_point = sorted(liste_croissante_joueur_0_point)
    print(liste_croissante_joueur_0_point)

    for classement in liste_croissante_joueur_0_point:
        recherche_prenom_nom = players_table.search(where('classement') == classement)[0]
        nom_prenom = recherche_prenom_nom['nom'] + " " + recherche_prenom_nom['prenom']
        liste_finale_joueur_0_point.append(nom_prenom)

    print(liste_finale_joueur_0_point)
    liste_finale = liste_finale_joueur_1_point + liste_finale_joueur_0_point
    print(liste_finale)

#on crée une fonction qui prendra en paramétre la paire, le score et qui va retourner un tuple contenant
#2 listes avec instance de joueur + le score
def matchs(tournois, paires):

    tournois= tournois
    liste_matchs = []

    db = TinyDB('db.json')
    matchs_table = db.table('Matchs')
    players_table = db.table('Joueurs')

    for paire in paires:
        score_1 = random.choice([0,0.5,1])
        if score_1 == 0:
            score_2 = 1
        if score_1 == 1:
            score_2 = 0
        if score_1 == 0.5:
            score_2 = 0.5

        joueur_1 = paire[0]
        joueur_2 = paire[1]

        score_j1 = update_points_joueurs(joueur_1, score_1)
        score_j2 = update_points_joueurs(joueur_2, score_2)

        j1 = joueur_1.split()
        j2 = joueur_2.split()
        nom_prenom_j1 = j1[1] + " " + j1[0]
        nom_prenom_j2 = j2[1] + " " + j2[0]


        update_joueurs_affrontes(tournois, nom_prenom_j1, nom_prenom_j2)
        update_joueurs_affrontes(tournois, nom_prenom_j2, nom_prenom_j1)

        print(joueur_1, " a : ",score_j1)
        print(joueur_2, " a : ", score_j2)

        tuple = ([joueur_1, score_1], [joueur_2, score_2]) #ajout d'un id unique
        liste_matchs.append(tuple)


    #matchs_table.truncate()
    for m in liste_matchs:
        tuple_match = Matchs(paire=m, tournois=tournois)

        match_serialized = {
            'paire':tuple_match.paire,
            'tournois':tuple_match.tournois
        }
        matchs_table.insert(match_serialized)

    for match in matchs_table.all()[-4:-1]:
        print("match : ",match)
    return liste_matchs

def creation_tour(tournois,liste_matchs):
    #on va voir si un tour existe déjà pour le tournois en question
    db = TinyDB('db.json')
    tours_table = db.table('Tours')
    q = Query()

    #on recherche si un round existe et est associé au tournois ou non :
    resultat = tours_table.search(where('tournois') == tournois)

    #si le résultat est vide on crée le round 1 :
    if not resultat:
        fin = time_now()
        tour = Tours(nom='Round 1', debut=None, fin=fin, match=liste_matchs, tournois=tournois)
        tour_serialized = {
            'nom':tour.nom,
            'debut':tour.debut,
            'fin':tour.fin,
            'match':tour.match,
            'tournois':tour.tournois

        }
        tours_table.insert(tour_serialized)
        tours_table = tours_table.search(where('tournois') == tournois)[-1]
        print("""
            Le {} a bien été enregistré :
            {}
        """.format(tour.nom, tours_table))
    else:
        find_last_round = tours_table.search(q.tournois == tournois)[-1]
        round_number = int(find_last_round['nom'][-1])
        round_number += 1
        nom = "Round " + str(round_number)
        fin = time_now()
        tour = Tours(nom=nom, debut=None, fin=fin, match=liste_matchs, tournois=tournois)
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
                    Le {} a bien été enregistré :
                    {}
                """.format(tour.nom, tours_table))

def changer_classement_joueurs():

    db = TinyDB('db.json')
    players_table = db.table("Joueurs")
    q = Query()

    liste_des_joueurs = liste_joueurs()
    print("""
        Voici la liste des joueurs dans la base de données :
        {}
    """.format(liste_des_joueurs))
    nom_prenom = input("Choissisez la personne à qui vous voulez modifier le classement : ")
    nom_prenom = nom_prenom.split(" ")

    try:
        player = players_table.search((q.prenom == nom_prenom[1]) & (q.nom == nom_prenom[0]))
        print(player)
        nouveau_classement = input('Entre le nouveau classement : ')
        champ_vide(nouveau_classement)
        nouveau_classement = classement_verification(nouveau_classement)
        players_table.update({'classement': nouveau_classement}, (q.prenom == nom_prenom[1] and q.nom == nom_prenom[0]))
        player = players_table.search((q.prenom == nom_prenom[1]) & (q.nom == nom_prenom[0]))
        print(player)
    except:
        print("La personne n'existe pas dans la base de données.")

def update_points_joueurs(joueur, point_a_ajouter):
    joueur = joueur.split()
    nom = joueur[1]
    prenom = joueur[0]
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()
    query_player = players_table.search((q.nom == nom and q.prenom == prenom))[0]
    points_actuels = query_player['points']
    points_finaux = points_actuels + point_a_ajouter
    player_updating = players_table.update({'points':points_finaux}, (q.nom == nom and q.prenom == prenom))
    query_player = players_table.search((q.nom == nom) and (q.prenom == prenom))[0]
    print(query_player['points'])
    return query_player['points']


def search_classement(nom_prenom):
    nom_prenom_split = nom_prenom.split()
    nom = nom_prenom_split[0]
    prenom = nom_prenom_split[1]
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()

    player = players_table.search((q.nom == nom) and (q.prenom == prenom))[0]
    classement = player['classement']
    return [nom_prenom, classement]

def search_player_by_classement(classement):
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()

    player = players_table.search(q.classement == classement)[0]
    player_identite = player['nom'] + " " + player['prenom']

    return player_identite

def liste_acteurs_odre_de_classement(liste_joueurs):
    liste_classement_joueur = []
    for player in liste_joueurs:
        classement = search_classement(player)
        liste_classement_joueur.append(classement[1])

    liste_joueur_ordre_croissant = sorted(liste_classement_joueur)
    liste_acteurs_odre_de_classement = []
    for classement in liste_joueur_ordre_croissant:
        joueur = search_player_by_classement(classement)
        liste_acteurs_odre_de_classement.append(joueur)

    return liste_acteurs_odre_de_classement

def liste_matchs_d_un_tournois(tournois):
    db = TinyDB('db.json')
    matchs_table = db.table('Matchs')
    q = Query()
    all_matchs = matchs_table.search(q.tournois == tournois)
    liste_matchs = []
    for match in all_matchs:
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
            match :
                {} vs {}
            Vainqueur :
                {}
        """.format(joueur_1, joueur_2, vainqueur))
    return liste_matchs

def liste_tours_d_un_tournois(tournois):
    db = TinyDB('db.json')
    tours_table = db.table('Tours')
    q = Query()
    all_tours = tours_table.search(q.tournois == tournois)
    for tour in all_tours:
        print(tour)
        print('\n')

def liste_triee(liste_joueurs):
    groupe_4_pts = []
    groupe_3_5_pts = []
    groupe_3_pts = []
    groupe_2_5_pts = []
    groupe_2_pts = []
    groupe_1_5_pts = []
    groupe_1_pts = []
    groupe_0_5_pts = []
    groupe_0_pts = []
    listes = [groupe_4_pts, groupe_3_5_pts, groupe_3_pts, groupe_2_5_pts, groupe_2_pts, groupe_1_5_pts, groupe_1_pts,
              groupe_0_5_pts, groupe_0_pts]

    for player in liste_joueurs:
        player = player.split()
        nom = player[0]
        prenom = player[1]
        nom_prenom = nom + " " + prenom

        db = TinyDB('db.json')
        players_table = db.table('Joueurs')
        q = Query()
        player_query = players_table.search((q.nom == nom) and (q.prenom == prenom))[0]

        player_points = player_query['points']
        if player_points == 0:
            groupe_0_pts.append(nom_prenom)
        if player_points == 0.5:
            groupe_0_5_pts.append(nom_prenom)
        if player_points == 1:
            groupe_1_pts.append(nom_prenom)
        if player_points == 1.5:
            groupe_1_5_pts.append(nom_prenom)
        if player_points == 2:
            groupe_2_pts.append(nom_prenom)
        if player_points == 2.5:
            groupe_1_pts.append(nom_prenom)
        if player_points == 3:
            groupe_3_pts.append(nom_prenom)
        if player_points == 3.5:
            groupe_3_5_pts.append(nom_prenom)
        if player_points == 4:
            groupe_4_pts.append(nom_prenom)
    liste_triee = []
    for liste in listes:

        if len(liste) == 1:
            liste_triee += liste
        elif len(liste) == 0:
            pass
        else:
            liste_ordre_croissant = liste_acteurs_odre_de_classement(liste)
            liste_triee += liste_ordre_croissant

    return liste_triee

def update_joueurs_affrontes(tournois, joueur, joueur_a_ajouter):
    joueur = joueur.split()
    nom = joueur[0]
    prenom = joueur[1]
    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()
    player = players_table.search((q.nom == nom) & (q.prenom == prenom) & (q.tournois == tournois))[0]
    print(player)

    liste_joueur_to_add = []
    if player['liste joueurs affrontes'] == []:
        print('liste vide')
    else:
        for p in player['liste joueurs affrontes']:
            liste_joueur_to_add.append(p)

    liste_joueur_to_add.append(joueur_a_ajouter)
    player_update = players_table.update({'liste joueurs affrontes':liste_joueur_to_add},
                                         (q.nom == nom) & (q.prenom == prenom) & (q.tournois == tournois))
    print(player)



def liste_joueurs_affrontes(joueur, tournois):
    joueur = joueur.split()
    nom = joueur[0]
    prenom = joueur[1]

    db = TinyDB('db.json')
    players_table = db.table('Joueurs')
    q = Query()

    player = players_table.search((q.nom == nom) & (q.prenom == prenom) & (q.tournois == tournois))[0]
    liste_joueurs_affrontes = player['liste joueurs affrontes']

    return liste_joueurs_affrontes

