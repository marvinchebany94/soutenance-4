import sys
from tinydb import TinyDB
from fonctions import creation_tournois, creation_liste_joueur, add_players_to_tournament, creation_paires, matchs,\
    changer_classement_joueurs, creation_tour, creation_paires_tour_1, search_classement, search_player_by_classement, \
    liste_acteurs_odre_de_classement, liste_matchs_d_un_tournois, liste_tours_d_un_tournois, liste_triee, \
    choix_du_tournois
from modele import creation_joueurs, liste_acteurs_odre_alphabetique, liste_joueurs, liste_des_tournois
from verification import commandes_verifications

def main():

    #PAIRES = creation_paires()
    LISTE_COMMANDES_GENERALES = ['créer un tournois(1)', 'choisir un tournois(2)', "afficher la liste des acteurs :\
 par ordre alphabétique(3) / par classement(4)", "afficher la liste de tous les tournois(5)", "q pour quitter"]

    LISTE_COMMANDES_POUR_LES_TOURNOIS = ["créer une liste de joueurs(1)", "créer un tour(2)", "modifier classement\
 d'un joueur(3)", "afficher la liste des acteurs : par ordre alphabétique(4) / par classement(5)", "afficher la\
 liste de tous les tours(6)", "affichier la liste de tous les matchs(7)", "q pour quitter"]

    LISTE_COMMANDES_GENERALES = " | ".join(LISTE_COMMANDES_GENERALES)
    LISTE_COMMANDES_POUR_LES_TOURNOIS = " | ".join(LISTE_COMMANDES_POUR_LES_TOURNOIS)

    print("""
                ----------Chess Tournament Creator----------
            """)
    print(LISTE_COMMANDES_GENERALES)

    liste_commandes_generales = ["1", "2", "3", "4", "5", "6", "7", "q"]

    while True:

        commandes = input('Entrez votre commande : ')
        cmd = commandes_verifications(liste_commandes_generales, commandes)

        if cmd == "q":
            print("""
                ~VOUS ALLEZ QUITTER L APPLICATION~
            """)
            sys.exit()

        if cmd == "1":
            print("""
            ~VOUS ALLEZ CREER UN TOURNOIS : ~            
            """)
            creation_tournois()

        if cmd == "2":
            print("""
            ~VOUS ALLEZ CHOISIR UN TOURNOIS : ~            
            """)
            choix_du_tournois()

        if cmd == "3":
            print("""
            ~VOUS ALLEZ VOIR LA LISTE DE TOUS LES ACTEURS PAR ODRE ALPHABETIQUE : ~            
            """)
            liste_des_joueurs = liste_joueurs()
            liste_acteurs_odre_alphabetique(liste_des_joueurs, "")

        if cmd == "4":
            print("""
            ~VOUS ALLEZ VOIR LA LISTE DE TOUS LES ACTEURS PAR ODRE DE CLASSEMENT : ~            
            """)
            liste_des_joueurs = liste_joueurs()
            print(liste_acteurs_odre_de_classement(liste_des_joueurs))

        if cmd == "5":
            print("""
            ~VOUS ALLEZ VOIR LA LISTE DE TOUS LES TOURNOIS : ~            
            """)
            print(liste_des_tournois())

        while cmd == "2":
            print(LISTE_COMMANDES_POUR_LES_TOURNOIS)
            break

        commandes = input("(creer | choisir | modifier classement | creer bdd | test | q pour quitter) : ")
        if commandes == "creer":
            creation_tournois()
            #tournois = creation_liste_joueur()
            #add_players_to_tournament(tournois)
            #paires = creation_paires()
            #print(paires)
        if commandes == "choisir":
            tournois = creation_liste_joueur()

        if commandes == "modifier classement":
            #creation_joueurs()
            changer_classement_joueurs()

        if commandes == "q":
            print("Vous allez quitter le script.")
            sys.exit()

        if commandes == "creer bdd":
            creation_joueurs('gta')

        if commandes == "test":

            paires = creation_paires()
            liste_matchs = matchs(paires)
            print(liste_matchs)
        if commandes == 'liste ordre alphabetique':
            liste_des_joueurs = liste_joueurs()
            liste_acteurs_odre_alphabetique(liste_des_joueurs)
        if commandes == "classement":
            liste_des_joueurs = liste_joueurs()
            print(liste_acteurs_odre_de_classement(liste_des_joueurs))
        if commandes == 'matchs':
            liste_matchs_d_un_tournois('rocket league')
        if commandes == 'tours':
            matchs_liste = matchs(PAIRES)
            creation_tour('rocket league', matchs_liste)
            liste_tours_d_un_tournois('rocket league')
        if commandes == "add":
            add_players_to_tournament('new tournois')
            joueurs = liste_joueurs()
            liste_acteurs_odre_alphabetique(joueurs, 'new tournois')
        if commandes == 'tour 2':
            joueurs = liste_joueurs()
            print(liste_triee(joueurs))
        if commandes == "suppr":
            suppr_all_db()
        else:
            print("Ta réponse ne figure pas dans la liste des choix.")
main()