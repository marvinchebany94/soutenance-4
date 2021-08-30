from tinydb import TinyDB, where
from datetime import datetime
import time
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
print(date[0:1])
