# coding: utf-8
import sys
import os
import datetime
current_path = sys.argv[0]
current_path = os.path.dirname(current_path)
current_path = os.path.dirname(current_path)
sys.path.append(current_path)
from modeles.modele import liste_des_tournois


def date_verification(j, m, a):
    """
    La fonction va tester la validité d'une date, dans un premier temps
    elle vérifie que les 3 paramètres sont des chiffres, puis la date
    sera testée via datetime qui peut renvoyer un ValueError
    si la date est invalide.
    :param j: correspond au chiffre du jour
    :param m: correspond au chiffre du mois
    :param a: corespond au chiffre de l'année
    :return: True si la date est valide ou false si elle ne l'est pas
    """

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
    """
    La fonction va vérifier si le tournois que la personne veut créer
    existe déjà ou non dans la base de données.
    On va utiliser liste_des_tournois qui renvoit la liste des noms
    de tous les tournois
    :param nom_du_tournois: Le nom du tournois que l'on veut vérifier
    :return: True si le nom du tournois existe déjà, false si celui-ci
    n'est pas dans la base de données.
    """
    liste_tournois = liste_des_tournois(False)
    if nom_du_tournois in liste_tournois:
        print("""
    Le tournois que vous voulez créer existe déjà dans \
    la base de donnée.
    Veuillez trouver un autre nom pour celui-ci.
        """)
        return True
    else:
        return False


def test_choix_du_tournois(reponse):
    """
    La fonction va vérifier si l'utilisateur a bien choisi un nom de
    tournois figurant dans la base de données ou non.
    :param reponse: le paramétre demandé est le nom du tournois qui
    a été choisi par l'utilisateur.
    :return: False si la reponse n'est pos dans la liste, True si elle l'est.
    """
    liste_tournois = liste_des_tournois(False)
    if reponse not in liste_tournois:
        print("Tu n'as pas choisis un tournois figurant dans la liste.")
        return False
    else:
        return True


def verification_controle_du_temps(reponse):
    """
    La fonction va vérifier si la réponse est bien dans la liste ou non.
    :param reponse: La réponse qui va être testée.
    :return: False si la réponse n'est pas dans la liste, l'item
    correspondant si la réponse est bonne.
    """
    liste_manieres_de_jouer = ["bullet", "blitz", "coup rapide"]
    try:
        i = liste_manieres_de_jouer.index(reponse)
        return liste_manieres_de_jouer[i]
    except ValueError:
        print("Ton choix n'est pas dans la liste de choix indiqués.")
        return False


def sexe_verification(reponse):
    """
    La fonction va vérifier que la réponse soit bien m ou f
    :param reponse: la réponse a vérifier
    :return: True si la réponse est bonne, False si elle ne l'est pas
    """
    liste_reponses = ['m', 'f']
    try:
        liste_reponses.index(reponse)
        return True
    except ValueError:
        return False


def classement_verification(classement):
    """
    La fonction vérifie que la valeur du classement soit bonne.
    :param classement: la valeur à vérifier
    :return: False si la valeur est mauvaise, retourne la valeur
    si elle est valide
    """
    try:
        int(classement)
    except ValueError:
        print("La valeur n'est pas correcte.")
        return False

    if int(classement) <= 0:
        print("Tu en peux pas être classé en-dessous de 0.")
        return False
    else:
        return int(classement)


def commandes_verifications(liste, commande):
    """
    La fonction vérifie que la commande se trouve bien dans la
    liste des commandes
    :param liste: la liste des commandes en question
    :param commande: la commande que la fonction va vérifier
    :return: retourne une valeur de la liste si la commande
    existe, ou retourne un message d'erreur si elle n'existe pas
    """
    try:
        i = liste.index(commande)
        return liste[i]
    except ValueError:
        return "La commande ne figure pas dans la liste"

def nombre_de_jours_verification(nombre):
    """
    La fonction vérifie que le nombre de jours choisi par l'utilisateur
    se trouve bien entre 1 et 4
    :param nombre:
    :return:
    """
    liste_nombre = [1, 2, 3, 4]
    try:
        nombre = int(nombre)
    except ValueError:
        print("Veuillez entrer des chiffres seulement.")
        return False
    try:
        liste_nombre.index(nombre)
        return True
    except ValueError:
        print("Le chiffre indiqué ne se trouve pas entre 1 et 4.")
        return False