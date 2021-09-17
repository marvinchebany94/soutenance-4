import sys
import datetime
from modele import liste_des_tournois


def champ_vide(champ_a_tester):
    if len(champ_a_tester) == 0:
        print("Le champ est mal rempli.")
        sys.exit()
    else:
        return champ_a_tester


def date_verification(j, m, a):
    if type(j) != int or type(m) != int or type(a) != int:
        print("La date est invalide")
    else:
        try:
            datetime.datetime(a, m, j)
            return True
        except ValueError:
            print("La date n'est pas valide.")
            return False


def verification_tournois_already_exists(nom_du_tournois):
    liste_tournois = liste_des_tournois()
    if nom_du_tournois in liste_tournois:
        print("""
            Le tournois que vous voulez créer existe déjà dans la base de donnée.
             Veuillez trouver un autre nom pour celui-ci.       
            """)
        sys.exit()
    else:
        pass


def test_choix_du_tournois(reponse):
    liste_tournois = liste_des_tournois()
    if reponse not in liste_tournois:
        print("Tu n'as pas choisis un tournois figurant dans la liste.")
        sys.exit()
    else:
        pass


def verification_controle_du_temps(reponse):
    liste_manieres_de_jouer = ["bullet", "blitz", "coup rapide"]
    try:
        i = liste_manieres_de_jouer.index(reponse)
        return liste_manieres_de_jouer[i]
    except ValueError:
        print("Ton choix n'est pas dans la liste de choix indiqués.")
        sys.exit()


def sexe_verification(reponse):
    liste_reponses = ['m', 'f']
    try:
        i = liste_reponses.index(reponse)
        return liste_reponses[i]
    except ValueError:
        return "Tu n'as pas entré la bonne information."


def classement_verification(classement):
    try:
        int(classement)
    except ValueError:
        print("La valeur n'est pas correcte.")

        sys.exit()
    while int(classement) <= 0:
        print("Tu en peux pas être classé en-dessous de 0.")
        classement = input(": ")
        classement_verification(classement)
        break
    return int(classement)


def commandes_verifications(liste, commande):
    try:
        i = liste.index(commande)
        return liste[i]
    except ValueError:
        return "La commande ne figure pas dans la liste"
