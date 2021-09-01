import sys, datetime
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
            date = datetime.datetime(a,m,j)
            return True
        except ValueError:
            print("La date n'est pas valide.")
            return False

def verification_tournois_already_exists(nom_du_tournois):
    liste_tournois = liste_des_tournois()
    if nom_du_tournois in liste_tournois: #chercher une fonction pour chercher plus rapidement
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
    if reponse not in liste_manieres_de_jouer:
        print("{} n'est pas dans la liste de choix indiqués.".format(reponse))
        sys.exit()
    else:
        for maniere in liste_manieres_de_jouer:
            if reponse == maniere:
                return maniere
            else:
                pass

def sexe_verification(reponse):
    if reponse == "f":
        return reponse
    if reponse == "m":
        return reponse
    else:
        while reponse != "f" or reponse != "m":
            print("Tu n'as pas entré la bonne information. (f ou m)")
            reponse = input(": ")
            sexe = sexe_verification(reponse)
            return sexe
            break


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
    return classement


