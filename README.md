# gefiproj-api
Ce dépôt contient le backend du projet GEFIPROJ.

## Installation et utilisation
**⚠️ Attention, le projet fonctionne uniquement sous Python v3.x**
 
Pour installer ce projet :
- Cloner le projet dans votre "workspace" local :

```shell
git clone https://github.com/cbn-alpin/gefiproj-api
```

- Se deplacer dans le dossier du projet cloné : 

```shell
cd gefiproj-api/
```

- Créer un environnement virtuel : 
```shell
python -m venv cbna_env
```

- Activer l'environnement virtuel : 
```shell
. ./cbna_env/bin/activate
```

- Installer les dépendances : 
```shell
pip install -r requirements.txt
```

- Configurer l'accès à la base de données : vous devez recuperer les configurations dans le drive google dans le dossier 
Configuration/config.yml. Vous devez enregistrer un fichier `config.yml` dans le fichier `config/` du projet.

- Lancer les tests avec 
```shell
python -m unittest discover -v -s tests/ -p '*_tests.py'
```

<b>Note importante</b> ⚠️ ️: Pour lancer les tests il faut avoir configuré l'entrée `test_database` et `test_token` dans le fichier de config 
avec les informations d'une base de donnée autre que celle de la production et un token valide.
 
## Lancement du framwork *Flask* 🚀
- Exporter des variables sur votre terminal : 
    ```shell
    export FLASK_APP=src/main.py
    ```

- Configurer : 
    ```shell
    set FLASK_APP=src/main.py
    ```

- Mode Debug : 
    ```shell
    export FLASK_DEBUG=true
    ```

- Lancer le projet : 
    ```shell
    flask run
    ```

Vérifier que le projet est lancé en allant sur  `/status` et voir que la reponse est `ok`
