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
    print("Vous allez créer un tournois :")
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

def creation_liste_joueur():
    liste_tournois = liste_des_tournois()

    print("""
        Vous allez créer une liste de joueurs pour un tournois.
        Veuillez selectionner un tournois dans la liste suivante :
        {}
    """.format(liste_tournois))

    choix_du_tournois = input("choisissez le tournois auquel vous voulez ajouter des personnes : ")
    test_choix_du_tournois(choix_du_tournois)
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
    tournois_table = tournois_table.search(where('nom') == tournois)[0]
    liste_des_joueurs = liste_joueurs()
    liste_players_serialized = {
        'liste des joueurs':liste_des_joueurs
    }
    try:
        tournois_table.update({'liste des joueurs':liste_des_joueurs})
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
def matchs(paires):

    liste_matchs = []
    for paire in paires:
        score_1 = random.randint(0, 1)
        score_2 = random.randint(0, 1)
        while score_2 == score_1:
            score_2 = random.randint(0, 1)
        tuple = [paire[0], score_1], [paire[1], score_2] #ajout d'un id unique

        liste_matchs.append(tuple)

    db = TinyDB('db.json')
    matchs_table = db.table('Matchs')
    matchs_table.truncate()
    for m in liste_matchs:
        tuple_match = Matchs(paire=m, tournois='rocket league')

        match_serialized = {
            'paire':tuple_match.paire,
            'tournois':tuple_match.tournois
        }
        matchs_table.insert(match_serialized)

    #matchs_table = matchs_table.all()
    print(matchs_table.all())
    return liste_matchs

def creation_tour(tournois,liste_matchs):
    #on va voir si un tour existe déjà pour le tournois en question
    db = TinyDB('db.json')
    tours_table = db.table('Tours')

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
        tours_table = tours_table.search(where('tournois') == tournois)
        print("""
            Le {} a bien été enregistré :
            {}
        """.format(tour.nom, tours_table))

def changer_classement_joueurs():

    db = TinyDB('db.json')
    players_table = db.table("Joueurs")
    liste_des_joueurs = liste_joueurs()
    print("""
        Voici la liste des joueurs dans la base de données :
        {}
    """.format(liste_des_joueurs))
    nom_prenom = input("Choissisez la personne à qui vous voulez modifier le classement : ")
    nom_prenom = nom_prenom.split(" ")
    #print(nom_prenom[0])

    players_table = players_table.search(where('nom') == nom_prenom[0])
    for player in players_table:

        if nom_prenom[1] in str(player):
            player_founded = player
            print(player_founded)
            nouveau_classement = input("Entrez son nouveau classement : ")
            champ_vide(nouveau_classement)
            nouveau_classement = classement_verification(nouveau_classement)
            player_founded.update({'classement': nouveau_classement})
            print(player_founded)
        else:
            continue







