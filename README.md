# soutenance-4

Bienvenue sur le README de chess tournament creator, je vais vous expliquer comment utiliser mon script.

Pour commencer il faudra avoir python installé sur votre ordinateur. Si ce n'est pas le cas, voici un lien menant à la dérnière version de celui-ci :
https://www.python.org/downloads/release/python-397/

Une fois installé, vous allez télécharger le dossier zip sur le github.
Il faudra ensuite déziper le dossier.

Le dossier contient plusieurs répertoire :

-modéle (modele.py)

-vue (vue.py)

-contrôle (fonctions.py et verification.py)

Vous allez ouvrir l'invite de commandes, puis à l'aide des commandes :
-dir qui vous montrera tous les fichiers et répertoires de l'endroit ou vous vous trouvez
-cd qui servira à vous rendre dans le dossier souhaiter
vous ferez cd + nom du dossier dézipé.

Vous allez créer un environnement virtuel via la commande : python -m venv env 

Une fois l'environnement créé, il faudra l'activer.
Vous utiliserez la commande env/Scripts/activate ou activate.bat 

Si entre parenthèses vous voyez (env) c'est que l'environnement a bien été activé.

Il est maintenant temps d'installer les modules nécéssaires au bon fonctionnement du programme.

python -m pip install -r requirements.txt

Vous pouvez maintenant lancer le script sans avoir de problèmes au niveau des modules.

Lancez dans l'invite de commandes : chemin_du_fichier/vue.py

Une fois lancée vous arriverez sur le menu principal qui contient une liste d'actions possibles d'effectuer.
Chaque action est numérotée. Pour le menu principal on aura 6 commandes :
créer un tournois, choisir un tournois, afficher la liste des acteurs par ordre alphabétique ou par classement, afficher la liste de tous les tournois, puis quitter l'application.

Si vous entrez 1 :
Vous allez créer un tournois, le programme vous demandera plusieurs informations comme le nom du tournois, le lieu, la date, le contrôle du temps et une description.

Si vous entrez 2 :
Le programme affichera la liste de tous les tournois avec des infos comme le nom, le lieu, la date et le contrôle du temps.
Pour choisir le tournois avec lequel vous voudrez intéragir il suffira d'entrer son nom.

Si vous entrez 3:
Le programme affichera la liste de tous les acteurs par ordre alphabétique en mettant leur nom, prénom et classement.

Si vous entrez 4 :
Le programme affichera la liste de tous les acteurs par ordre de classement en mettant le nom, prénom et classement.

Si vous entrez 5 :
le programme affichera la liste de tous les tournois avec leur nom, date, lieu et contrôle du temps.

Si vous entrez q :
Le programme s'arrête.



