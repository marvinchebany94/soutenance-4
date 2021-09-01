import sys
from fonctions import creation_tournois, creation_liste_joueur, add_players_to_tournament, creation_paires, matchs,\
    changer_classement_joueurs, creation_tour, creation_paires_tour_1
from modele import creation_joueurs

def main():

    while True:
        commandes = input("(creer | choisir | modifier classement | q pour quitter) : ")
        if commandes == "creer":
            creation_tournois()
            tournois = creation_liste_joueur()
            add_players_to_tournament(tournois)
            paires = creation_paires()
            print(paires)
        if commandes == "choisir":
            tournois = creation_liste_joueur()
            add_players_to_tournament(tournois)
            paires = creation_paires()
            print(paires)
            matchs(paires)

        if commandes == "modifier classement":
            creation_joueurs()
            changer_classement_joueurs()

        if commandes == "q":
            print("Vous allez quitter le script.")
            sys.exit()

        if commandes == "test":
            creation_joueurs()
            paires = creation_paires()
            liste_matchs = matchs(paires)
            creation_tour('rocket league', liste_matchs)
            creation_paires_tour_1()

        else:
            print("Ta réponse ne figure pas dans la liste des choix.")
main()