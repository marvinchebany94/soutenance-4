import sys
from tinydb import TinyDB
from fonctions import creation_tournois, creation_liste_joueur, add_players_to_tournament, creation_paires, matchs,\
    changer_classement_joueurs, creation_tour, creation_paires_tour_1, search_classement, search_player_by_classement, \
    liste_acteurs_odre_de_classement, liste_matchs_d_un_tournois, liste_tours_d_un_tournois, liste_triee, \
    choix_du_tournois, etape_3_4_systeme_suisse, creating_paires, nombre_de_tours
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

    liste_commandes_generales = ["1", "2", "3", "4", "5", "q"]
    liste_commandes_pour_les_tournois = ["1", "2", "3", "4", "5", "6", "7", "q"]

    while True:

        print("""
        ----- Menu principal -----
        """)

        print(LISTE_COMMANDES_GENERALES)
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
            tournois = choix_du_tournois()

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

            while True:
                print("""
                      -----------TOURNOIS ' {} '-----------
                """.format(tournois))

                print(LISTE_COMMANDES_POUR_LES_TOURNOIS)

                cmd = input('Entrez votre commande : ')
                commande = commandes_verifications(liste_commandes_pour_les_tournois, cmd)

                if commande == "q":
                    break

                if commande == "1":
                    creation_joueurs(tournois)
                    liste_des_joueurs = liste_joueurs()
                    add_players_to_tournament(tournois)

                if commande == "2":
                    numero_tour = nombre_de_tours(tournois)
                    print("""
                        VOUS ALLEZ CREER LE TOUR NUMERO {}
                    """.format(numero_tour))

                    if numero_tour == 1:
                        paires = creation_paires()
                        liste_des_matchs = matchs(tournois, paires)
                        print(liste_des_matchs)
                        creation_tour(tournois, liste_des_matchs)

                    else:
                        print("""
                            TOUR {} :
                        """.format(numero_tour))

                        liste_des_joueurs = liste_joueurs()
                        l_triee = liste_triee(liste_des_joueurs)
                        all_paires = creating_paires(tournois, l_triee)
                        liste_des_matchs = matchs(tournois, all_paires)
                        creation_tour(tournois, liste_des_matchs)


                if commande == "3":
                    changer_classement_joueurs()

                if commande == "4":
                    print("""
                        ~VOUS ALLEZ VOIR LA LISTE DE TOUS LES ACTEURS PAR ODRE ALPHABETIQUE : ~            
                    """)
                    liste_des_joueurs = liste_joueurs()
                    liste_acteurs_odre_alphabetique(liste_des_joueurs, tournois)

                if commande == "5":
                    print("""
                        ~VOUS ALLEZ VOIR LA LISTE DE TOUS LES ACTEURS PAR ODRE DE CLASSEMENT : ~            
                    """)
                    liste_des_joueurs = liste_joueurs()
                    print(liste_acteurs_odre_de_classement(liste_des_joueurs))

                if commande == "6":
                    print("""
                    
                        VOUS ALLEZ VOIR LA LISTE DE TOURS LES TOURS DU TOURNOIS :
                        
                    """)
                    liste_tours_d_un_tournois(tournois)

                if commande == "7":
                    print("""

                        VOUS ALLEZ VOIR LA LISTE DE TOUS LES MATCHS DU TOURNOIS :

                    """)
                    liste_matchs_d_un_tournois(tournois)
main()