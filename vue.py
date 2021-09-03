import sys
from fonctions import creation_tournois, creation_liste_joueur, add_players_to_tournament, creation_paires, matchs,\
    changer_classement_joueurs, creation_tour, creation_paires_tour_1, search_classement, search_player_by_classement, \
    liste_acteurs_odre_de_classement, liste_matchs_d_un_tournois
from modele import creation_joueurs, liste_acteurs_odre_alphabetique, liste_joueurs

def main():

    while True:
        commandes = input("(creer | choisir | modifier classement | creer bdd | test | q pour quitter) : ")
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
            #creation_joueurs()
            changer_classement_joueurs()

        if commandes == "q":
            print("Vous allez quitter le script.")
            sys.exit()

        if commandes == "creer bdd":
            creation_joueurs()

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
        else:
            print("Ta réponse ne figure pas dans la liste des choix.")
main()