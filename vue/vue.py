# coding: utf-8
import sys
import os
current_path = sys.argv[0]
current_path = os.path.dirname(current_path)
current_path = os.path.dirname(current_path)
sys.path.append(current_path)
from controle.verification import commandes_verifications
from controle.fonctions import creation_tournois, creation_liste_joueur, \
    add_players_to_tournament, creation_paires, matchs, \
    changer_classement_joueurs, creation_tour, \
    liste_acteurs_odre_de_classement, liste_matchs_d_un_tournois, \
    liste_tours_d_un_tournois, liste_triee, choix_du_tournois, \
    creating_paires, nombre_de_tours, time_now, \
    voir_les_points_des_joueurs
from modeles.modele import creation_joueurs, liste_acteurs_odre_alphabetique, \
    liste_joueurs, liste_des_tournois,\
    liste_id_for_each_players


LISTE_COMMANDES_GENERALES = [
    'créer un tournois(1)',
    'choisir un tournois(2)',
    "afficher la liste des acteurs : \
par ordre alphabétique(3) / par classement(4)",
    "afficher la liste de tous les tournois(5)", "q pour quitter"
]

LISTE_COMMANDES_POUR_LES_TOURNOIS = [
    "créer une liste de joueurs(1)",
    "créer un tour(2)",
    "modifier classement \
d'un joueur(3)",
    "afficher la liste des acteurs : \
par ordre alphabétique(4)/ par classement(5)",
    "afficher la liste de tous les tours(6)",
    "afficher la liste de tous les matchs(7)",
    "afficher les points des joueurs(8)",
    "q pour quitter"
]


def main():
    print("""
    ----------Chess Tournament Creator----------
    """)
    liste_commandes_generales = ["1", "2", "3", "4", "5", "q"]
    liste_commandes_pour_les_tournois = ["1", "2", "3", "4", "5", "6", "7",
                                         "8", "q"]

    while True:

        print("""
        ----- Menu principal -----
        """)

        for item in LISTE_COMMANDES_GENERALES:
            print(item)
        print('\n')
        commandes = input('Entrez votre commande : ')
        cmd = commandes_verifications(liste_commandes_generales, commandes)

        if cmd == "q":
            print("~VOUS ALLEZ QUITTER L APPLICATION~")
            sys.exit()

        if cmd == "1":
            print("~VOUS ALLEZ CREER UN TOURNOIS : ~")
            creation_tournois()

        if cmd == "2":
            print("~VOUS ALLEZ CHOISIR UN TOURNOIS : ~")
            tournois = choix_du_tournois()

        if cmd == "3":
            print("~VOUS ALLEZ VOIR LA LISTE DE TOUS LES ACTEURS PAR \
ODRE ALPHABETIQUE : ~")
            liste_des_id = liste_id_for_each_players("")
            liste_acteurs_odre_alphabetique(liste_des_id, "")

        if cmd == "4":
            print("~VOUS ALLEZ VOIR LA LISTE DE TOUS LES ACTEURS \
PAR ODRE DE CLASSEMENT : ~")
            liste_des_joueurs = liste_id_for_each_players("")
            liste_acteurs_odre_de_classement(liste_des_joueurs, True)

        if cmd == "5":
            print("~VOUS ALLEZ VOIR LA LISTE DE TOUS LES TOURNOIS : ~")
            liste_des_tournois(True)

        while cmd == "2":
            if tournois is None:
                break
            numero_tour = nombre_de_tours(tournois)
            if numero_tour == 5:
                print("Tour 5")
                LISTE_COMMANDES_POUR_LES_TOURNOIS[1] = "Le tournois est \
fini, vous pouvez modifier les classements ici(2)"
            else:
                LISTE_COMMANDES_POUR_LES_TOURNOIS[1] = "Créer un tour(2)"

            while True:
                print("""
                      -----------TOURNOIS ' {} '-----------
                """.format(tournois))
                for item in LISTE_COMMANDES_POUR_LES_TOURNOIS:
                    print(item)
                print('\n')
                cmd = input('Entrez votre commande : ')
                commande = commandes_verifications(
                    liste_commandes_pour_les_tournois,
                    cmd
                )
                if commande == "q":
                    break
                if commande == "1":
                    while True:
                        print('\n')
                        if len(liste_id_for_each_players(tournois)) == 8:
                            print("8 joueurs ont déjà été inscris à \
                                  ce tournois.".upper())
                            print('\n')
                            break
                        if 0 < len(liste_id_for_each_players(tournois)) < 8:
                            print("""
                                VOUS ALLEZ CONTINUER A CREER DES JOUEURS \
MANUELLEMENT
                            """)
                            creation_liste_joueur(tournois)
                            add_players_to_tournament(tournois)
                        else:
                            print("Créer une liste de joueurs \
automatiquement(1)")
                            print("Créer une liste de joueurs manuellement(2)")
                            print("q pour quitter")
                            cmd = input("Veuillez entrer votre commande : ")
                            if cmd == "1":
                                creation_joueurs(tournois)
                                liste_des_joueurs = liste_joueurs(tournois)
                                add_players_to_tournament(tournois)
                                break
                            if cmd == "2":
                                print("""
                                    VOUS ALLEZ CREER UNE LISTE DE JOUEURS \
                                    MANUELLEMENT
                                """)
                                creation_liste_joueur(tournois)
                                add_players_to_tournament(tournois)
                                break
                            if cmd == "q":
                                break
                if commande == "2":
                    numero_tour = nombre_de_tours(tournois)
                    if len(liste_id_for_each_players(tournois)) != 8:
                        print("Vous ne pouvez pas créer un tour, \
le tournois n'est pas encore plein.")
                        break
                    if numero_tour == 5:
                        print("""
                        VOUS NE POUVEZ PLUS CREER DE TOURS, LE TOURNOIS EST \
TERMINE.
                        VEUILLEZ INDIQUER UN NOUVEAU CLASSEMENT POUR \
CHAQUE JOUEURS.
                        """)
                        while True:
                            cmd = input('q pour quitter | c pour continuer : ')
                            if cmd == "q":
                                break
                            if cmd == "c":
                                changer_classement_joueurs(tournois)
                                continue
                            else:
                                print("Commande invalide")
                        break

                    if numero_tour == 1:
                        print("""
                            VOUS ALLEZ CREER LE TOUR NUMERO {}
                        """.format(numero_tour))
                        debut = time_now()
                        id = liste_id_for_each_players(tournois)
                        paires = creation_paires(id)
                        liste_des_matchs = matchs(tournois, paires)
                        creation_tour(tournois, liste_des_matchs, debut)

                    else:
                        print("""
                            VOUS ALLEZ CREER LE TOUR NUMERO {}
                        """.format(numero_tour))
                        debut = time_now()
                        print("""
                            TOUR {} :
                        """.format(numero_tour))

                        liste_des_joueurs = liste_joueurs(tournois)
                        l_triee = liste_triee(liste_des_joueurs, tournois)
                        all_paires = creating_paires(tournois, l_triee)
                        liste_des_matchs = matchs(tournois, all_paires)
                        creation_tour(tournois, liste_des_matchs, debut)
                if commande == "3":
                    changer_classement_joueurs(tournois)
                if commande == "4":
                    print("~VOUS ALLEZ VOIR LA LISTE DE TOUS LES ACTEURS PAR \
ODRE ALPHABETIQUE : ~")
                    liste_des_id = liste_id_for_each_players(tournois)
                    liste_acteurs_odre_alphabetique(liste_des_id, tournois)
                if commande == "5":
                    print("~VOUS ALLEZ VOIR LA LISTE DE TOUS LES ACTEURS PAR \
ODRE DE CLASSEMENT : ~")

                    liste_des_id = liste_id_for_each_players(tournois)
                    liste_acteurs_odre_de_classement(liste_des_id, True)
                if commande == "6":
                    print("VOUS ALLEZ VOIR LA LISTE DE TOURS LES \
TOURS DU TOURNOIS :")
                    liste_tours_d_un_tournois(tournois)
                if commande == "7":
                    print("""
                        VOUS ALLEZ VOIR LA LISTE DE TOUS LES \
MATCHS DU TOURNOIS :
                    """)
                    liste_matchs_d_un_tournois(tournois)
                if commande == "8":
                    print("""
                        VOUS ALLER VOIR LA LISTE DE TOUS LES \
JOUEURS AVEC LEURS POINTS :
                    """)
                    liste_id = liste_id_for_each_players(tournois)
                    if not liste_id:
                        print("Il faut créer une liste de joueurs.")
                    else:
                        voir_les_points_des_joueurs(liste_id)


main()