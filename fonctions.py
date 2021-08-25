"""
Ce fichier va contenir toutes les fonctions du projet
"""
import random
def system_suisse(liste_joueur):
    """
    la fonction va créer 2 listes, les 4 meilleurs joueurs et les 4 moins bons.
    Dans un second temps elle va associer le 1er joueur de la 1ère liste avec le 1er de la deuxième et
    ainsi de suite.
    Au prochain tour, triez tous les joueurs en fonction de leur nombre total de points. Si plusieurs joueurs ont le
    même nombre de points, triez-les en fonction de leur rang.
    Associez le joueur 1 avec le joueur 2, le joueur 3 avec le joueur 4, et ainsi de suite. Si le joueur 1 a déjà joué
    contre le joueur 2, associez-le plutôt au joueur 3.
    :param liste_joueur:
    :return:
    """

    """
    On va 
    on va créer les variables des 2 listes
    """
    liste_meilleurs_joueurs = liste_joueur

    """
    pour trier la liste des joueurs on va utiliser sorted(liste)
    """


    print(sorted(liste_joueur))
liste = [10,5,6,1,3,7]
system_suisse(liste)
