# gefiproj-api
Ce dépôt contient le backend du projet GEFIPROJ.

## Installation et utilisation

Pour installer ce projet :
- Cloner le projet dans votre "workspace" local : `git clone https://github.com/yakuzhanh/gefiproj-api.git`
- Exporter des variables sur votre terminal : export FLASK_APP=src/main.py 
- Configurer : set FLASK_APP=src/main.py 
- Lancer le projet : flask run


### Configuration

Vous devez recuperer les configurations dans le drive google dans le dossier Configuration/config.yml
Vous devez enregistrer un fichier config.yml dans le fichier config du projet.


## Prérequis
### Dépendances

Ce projet utilise les bibliothèques Python et outils suivant :
- [Python 3.9](https://www.python.org/downloads/3.9) : pour installer python
- [Pyenv](https://github.com/pyenv/pyenv) : pour installer dans l'espace de l'utilisateur courant une version spécifique de Python (créer un fichier `config/settings.ini` pour surcoucher la version spécifique de Python 3 définie par défaut dans le fichier `config/settings.default.ini`).
- [Pipenv](https://pipenv.pypa.io/en/latest/) : pour installer l'environnement virtuel et gérer les dépendances Python.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) : pour réaliser les web services.
- [SqlAlchemy](https://www.sqlalchemy.org/) : ORM permettant d'intéroger la base de données.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) : permet de gérer l'installation de la base de donnée et ses migrations futures.
- Installer votre dependance avec la commande suivante : pip install -r requirements


## Tester les webservices

Le dossier `resources/postman/` contient une collection [Postman](https://www.postman.com/downloads/) permettant de tester les web services.

Ce projet contient aussi le code utilisant une authentification à base de [JWT](https://jwt.io/) qui s'appuie sur [le service Auth0](https://auth0.com/fr/).
Toutefois, il n'est pas actif par défaut car cela demande de créer un compte et de le configurer.
Les décorateurs assurant l'authentification des web services POST, PUT et DELETE sont donc commentés.
