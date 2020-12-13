# gefiproj-api
Ce dépôt contient le backend du projet GEFIPROJ.

## Installation et utilisation

Pour installer ce projet :
- Cloner le projet dans votre "workspace" local : `git clone https://github.com/cbn-alpin/gefiproj-api`
- Se deplacer dans le dossier du projet cloné : `cd gefiproj-api/`
- Créer un environnement virtuel : `python3 -m venv venv`
- Activer l'environnement virtuel : `. ./venv/bin/activate`
- Installer les dépendances : `pip install -r requirements.txt`
- Configurer l'accès à la base de données : vous devez recuperer les configurations dans le drive google dans le dossier 
Configuration/config.yml. Vous devez enregistrer un fichier `config.yml` dans le fichier `config/` du projet.
- Lancer les tests avec `python -m unittest discover -v -s tests/ -p '*_tests.py'`  
<b>Note importante</b> ⚠️ ️: Pour lancer les tests il faut avoir configuré l'entrée `test_database` et `test_token` dans le fichier de config 
avec les informations d'une base de donnée autre que celle de la production et un token valide.
- Lancer soit
    - avec Flask :
        - Exporter des variables sur votre terminal : `export FLASK_APP=src/main.py`
        - Configurer : `set FLASK_APP=src/main.py`
        - Mode Debug : `export FLASK_DEBUG=true`
        - Lancer le projet : `flask run`
    - ou avec pipenv : 
        - Lancer le projet : `pipenv run python src/main.py`

Vérifier que le projet est lancé en allant sur  `/status` et voir que la reponse est `ok`
