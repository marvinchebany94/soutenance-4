import sys
from fonctions import creation_tournois, creation_liste_joueur, add_players_to_tournament, creation_paires

def main():
    while True:
        creer_ou_choisir_un_tournois = input("Voulez vous créer ou choisir un tournois déjà créé ? "
                                             "(creer / choisir / q pour quitter) : ")
        if creer_ou_choisir_un_tournois == "creer":
            creation_tournois()
            tournois = creation_liste_joueur()
            add_players_to_tournament(tournois)
            paires = creation_paires()
            print(paires)
        if creer_ou_choisir_un_tournois == "choisir":
            tournois = creation_liste_joueur()
            add_players_to_tournament(tournois)
            paires = creation_paires()
            print(paires)
        if creer_ou_choisir_un_tournois == "q":
            print("Vous allez quitter le script.")
            sys.exit()
        else:
            print("Ta réponse ne figure pas dans la liste des choix.")
main()