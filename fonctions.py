"""
Ce fichier va contenir toutes les fonctions du projet
"""
import random
from tinydb import TinyDB, where, Query
from modele import Matchs, Tournois, liste_des_tournois, Joueur, liste_joueurs
from verification import champ_vide, date_verification, test_choix_du_tournois, verification_controle_du_temps,\
    verification_tournois_already_exists, sexe_verification, classement_verification

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

    tournois = Tournois(nom=nom, lieu=lieu, date=date, nombre_de_tours=4, tournees=None,
                        controle_du_temps=controle_du_temps, liste_des_joueurs=None, description=description)

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
        'description':tournois.description
        }
    tournois_table.insert(serialized_tournois)
    tournois_table = tournois_table.all()

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

        joueur = Joueur(nom, prenom, date_de_naissance, sexe, classement)

        #on enregistre le joueur ici
        try:

            print(players_table.all())
            serialized_player = {
                'nom':joueur.nom,
                'prenom':joueur.prenom,
                'date de naissance':joueur.date_de_naissance,
                'sexe':joueur.sexe,
                'classement':joueur.classement
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
        print(type(item), item)
        liste_classement_joueur.append(item)

    #on trie la liste en la mettant par ordre croissant
    liste_joueur_classement_croissant = sorted(liste_classement_joueur)
    print(liste_joueur_classement_croissant)

    #on reprend la liste classée par ordre croissant, puis on associe le rang des personnes à leur prénoms
    liste_classement_joueur_avec_nom = []

    for classement in liste_joueur_classement_croissant:

        #on va chercher la personne qui a le classement dans la base de donnée, player_infos va ressortir la
        #base de donnée qui correspond à celle-ci
        player_infos = players_table.search(where('classement') == str(classement))
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

#on crée une fonction qui prendra en paramétre la paire, le score et qui va retourner un tuple contenant
#2 listes avec instance de joueur + le score
def matchs(paires):
    #id du match

    liste_matchs = []
    for paire in paires:
        score_1 = random.randint(0, 1)
        score_2 = random.randint(0, 1)
        while score_2 == score_1:
            score_2 = random.randint(0, 1)
        match = ([paire[0], score_1], [paire[1], score_2])
        match = Matchs(match, 'rocket league')

        liste_matchs.append(match)

    db = TinyDB('db.json')
    matchs_table = db.table('Matchs')
    matchs_table.truncate()
    for m in liste_matchs:
        match = Matchs(m, tournois='rocket league')

        match_serialized = {
            'paire':match.paire,
            'tournois':match.tournois
        }
        matchs_table.insert(match_serialized)

        #except:
            #print("une erreur a été dectecté lors de la création de la bdd")
    matchs_table = matchs_table.all()
    print(matchs_table)

def changer_classement_joueurs():

    db = TinyDB('db.json')
    players_table = db.table("Joueurs")
    Joueurs = Query()
    liste_des_joueurs = liste_joueurs()
    print("""
        Voici la liste des joueurs dans la base de données :
        {}
    """.format(liste_des_joueurs))
    nom_prenom = input("Choissisez la personne à qui vous voulez modifier le classement : ")
    nom_prenom = nom_prenom.split(" ")
    print(nom_prenom[0])
    print(type(players_table))
    players_table = players_table.search(where('prenom') == nom_prenom[1])[0]

    #l = j.search(j['prenom'] == nom_prenom[1])
    print(players_table)



    nouveau_classement = input("Entrez son nouveau classement : ")
    champ_vide(nouveau_classement)
    nouveau_classement = classement_verification(nouveau_classement)

    players_table.update({'classement':nouveau_classement})
    print(players_table)



