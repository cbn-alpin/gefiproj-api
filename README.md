# gefiproj-api
Ce dépôt contient le backend du projet GEFIPROJ.

## Installation et utilisation

Pour installer ce projet :
- Cloner le projet dans votre "workspace" local : `git clone https://github.com/cbn-alpin/gefiproj-api`
- Installer les dépendances : `pip install -r requirements.txt`
- Lancer avec Flask :
    - Exporter des variables sur votre terminal : `export FLASK_APP=src/main.py`
    - Configurer : `set FLASK_APP=src/main.py`
    - Lancer le projet : `flask run`
- Lancer avec pipenv : 
    - Lancer le projet : `pipenv run python src/main.py`


### Configuration

Vous devez recuperer les configurations dans le drive google dans le dossier Configuration/config.yml
Vous devez enregistrer un fichier config.yml dans le fichier config du projet.


## Prérequis
### Dépendances

Ce projet utilise les bibliothèques Python et outils suivant :
- [Python 3.9](https://www.python.org/downloads/3.9) : pour installer python
- [Pyenv](https://github.com/pyenv/pyenv) : pour installer dans l'espace de l'utilisateur courant une version spécifique de Python (créer un fichier `config/settings.ini` pour surcoucher la version spécifique de Python 3 définie par défaut dans le fichier `config/settings.default.ini`).
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) : pour réaliser les web services.
- [SqlAlchemy](https://www.sqlalchemy.org/) : ORM permettant d'intéroger la base de données.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) : permet de gérer l'installation de la base de donnée et ses migrations futures.
- [Pipenv](https://pipenv.pypa.io/en/latest/) : 
Pour installer l'environnement virtuel et gérer les dépendances Python :
```bash
pip3 install pipenv
```
Executez la commande suivant dans votre dossier project pour installer des dépendances:
```bash
pipenv install --dev
```
