import sys, datetime
from modele import liste_des_tournois

def champ_vide(champ_a_tester):
    if len(champ_a_tester) == 0:
        print("Le champ {} est mal rempli.".format(champ_a_tester))
        sys.exit()
    else:
        pass

def date_verification(j, m, a):
    if type(j) != int or type(m) != int or type(a) != int:
        print("La date est invalide")
    else:
        try:
            date = datetime.datetime(a,m,j)
        except ValueError:
            print("La date n'est pas valide.")
            sys.exit()

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
        print("Tu n'as pas entré la bonne information. (f ou m)")
        sys.exit()

def classement_verification(classement):
    if int(classement) < 0:
        print("Tu en peux pas être classé en-dessous de 0.")
        sys.exit()
    else:
        return classement
