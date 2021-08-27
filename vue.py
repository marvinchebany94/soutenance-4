from fonctions import creation_tournois, creation_liste_joueur

def main():
    while True:
        creer_ou_choisir_un_tournois = input("Voulez vous créer ou choisir un tournois déjà créé ? "
                                             "(creer / choisir / q pour quitter) : ")
        if creer_ou_choisir_un_tournois == "creer":
            creation_tournois()
        if creer_ou_choisir_un_tournois == "choisir":
            creation_liste_joueur()
        if creer_ou_choisir_un_tournois == "q":
            print("Vous allez quitter le script.")
            sys.exit()
        else:
            print("Ta réponse ne figure pas dans la liste des choix.")
main()