"""
Ce fichier va contenir toutes les fonctions du projet
"""
import random
from tinydb import TinyDB, where, Query
from modele import db, players_table, liste_joueur, Matchs
def creation_paires(liste_joueur):
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
    for item in players_table:
        liste_classement_joueur.append(item['classement'])

    #on trie la liste en la mettant par ordre croissant
    liste_joueur_classement_croissant = sorted(liste_classement_joueur)

    #on reprend la liste classée par ordre croissant, puis on associe le rang des personnes à leur prénoms
    liste_classement_joueur_avec_nom = []

    for classement in liste_joueur_classement_croissant:

        #on va chercher la personne qui a le classement dans la base de donnée, player_infos va ressortir la
        #base de donnée qui correspond à celle-ci
        player_infos = players_table.search(where('classement') == classement)
        #on crée une boucle for pour prendre seulement le prénom et l'ajouter à la liste
        for infos in player_infos:
            print(infos['prenom'])
            prenom_nom = infos['prenom'] + " " + infos['nom']
            liste_classement_joueur_avec_nom.append(prenom_nom)

    #on crée les 2 groupes
    premier_groupe = liste_classement_joueur_avec_nom[0:4]
    deuxieme_groupe = liste_classement_joueur_avec_nom[4:8]

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
    id = 0
    liste_id_et_tuples = []
    for pair in paires:
        id += 1
        score_1 = random.randint(0, 1)
        score_2 = random.randint(0, 1)
        while score_2 == score_1:
            score_2 = random.randint(0, 1)
        tuple = ([pair[0], score_1], [pair[1], score_2])
        match = Matchs(id, tuple)

        liste_id_et_tuples.append([match.id, match.tuple])
        #liste_tuple.append(match.tuple)

    for id_tuple in liste_id_et_tuples:
        id = id_tuple[0]
        tuple = id_tuple[1]
        match = Matchs(id, tuple)
        try:
            db = TinyDB('db.json')
            matchs_table = db.table('matches')
            match_serialized = {
                'id':match.id,
                'tuple':match.tuple
            }
            matchs_table.insert(match_serialized)

        except:
            print("une erreur a été dectecté lors de la création de la bdd")
    matchs_table = matchs_table.all()
    print(matchs_table)





    #pour chaque paires


paires = creation_paires(liste_joueur)
print(paires)
matchs(paires)



