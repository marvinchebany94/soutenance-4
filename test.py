
from datetime import datetime
import time
import random

"""
class Joueurs:
    def __init__(self, prenom, nom, age):
        self.prenom = prenom
        self.nom = nom
        self.age = age

prenom = input("choisir le prénom de votre joueur :")
age = input("choisir l'âge de votre joueur")

db = TinyDB('test.py')
joueurs_table = db.table('Joueurs')
serialized_joueur = {
    'prenom':prenom,
    'nom':'',
    'age':age
}
joueurs_table.insert(serialized_joueur)
print(joueurs_table.all())
joueurs_table.truncate()

print(joueurs_table.all())
"""
date = datetime.now()

print(date.strftime('%d-%m-%y %H:%M'))

i = 5

print(random.choice([0,0.5,1]))

from modele import Joueur
from tinydb import TinyDB, where,Query
from fonctions import update_points_joueurs
def joueur():
    db = TinyDB('Joueurs.json')
    q = Query()
    db.truncate()
    marvin = Joueur("decocq", "marvin", "20/07/98", "m", 1, None, 0)
    marvin2 = Joueur("chebany", "rocket", "20/07/98", "m", 3, None, 0)
    marvin3 = Joueur("dunoyer", "kahyss", "16/03/2019", "m", 10, None, 0)
    loan = Joueur("dunoyer", "loan", "01/11/00", "f", 100, None, 0)
    papa = Joueur("decocq", "martial", "13/10/71", "m", 41, None, 0)
    maman = Joueur("chebany", "angela", "16/03/2019", "f", 2, None, 0)
    mamie = Joueur("chebany", "henriette", "09/06/50", "f", 34, None, 0)
    papy = Joueur("chebany", "cheban", "12/04/44", "m", 68, None, 0)
    liste_des_joueurs = [marvin, marvin2, marvin3, loan, papa, maman, mamie, papy]
    for player in liste_des_joueurs:
        db.insert({
            'nom': player.nom,
            'prenom': player.prenom,
            'date de naissance': player.date_de_naissance,
            'sexe': player.sexe,
            'classement': player.classement,
            'tournois': player.tournois,
            'points': player.points
        })
    marvin = db.search(q.prenom == 'marvin')
    print(marvin)
    db.update({'classement':15}, q.prenom == 'marvin')
    marvin = db.search(q.prenom == 'marvin')
    print(marvin)
def marvin():
    db = TinyDB('Joueurs.json')
    q = Query()
    marvin = db.search(q.prenom == 'marvin')
    print(marvin)

joueur = update_points_joueurs('decocq marvin', 4.5)
print(joueur)
