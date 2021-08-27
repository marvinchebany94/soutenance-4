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

def test_choix_du_tournois(reponse):
    liste_tournois = liste_des_tournois()
    if reponse not in liste_tournois:
        print("Tu n'as pas choisis un tournois figurant dans la liste.")
        sys.exit()
    else:
        pass