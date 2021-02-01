# gefiproj-api
Ce dépôt contient le backend du projet GEFIPROJ. https://gefiproj.cbn-alpin.fr/

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

# Own Paas serveur with CapRover  🚀
There are many easy CI/CD platforms that offer generous free minutes for your builds, for example GitHub and GitLab both offer free minutes for private repositories and unlimited free minutes for public repositories.
## Prerequisites
    
#### Configure Firewall

```bash
sudo ufw allow 80,443,3000,996,7946,4789,2377/tcp; sudo ufw allow 7946,4789,2377/udp;
```

#### Step 1: CapRover Installation
```
docker run -p 80:80 -p 443:443 -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock -v /captain:/captain caprover/caprover
```

#### Step 2: Connect Root Domain

Let's say you own mydomain.com. You can set *.something.mydomain.com as an A-record in your DNS settings to point to the IP address of the server where you installed CapRover. Note that it can take several hours for this change to take into effect. It will show up like this in your DNS configs:

- TYPE: A record
- HOST: *.something
- POINTS TO: (IP Address of your server)
- TTL: (doesn't really matter)


#### Step 3: 

```
docker exec -it [DOCKER CONTAINER ID] bash
npm install -g caprover
caprover serversetup
```

Now we can connect to : [https://captain.cbna.khadir.net](https://captain.cbna.khadir.net/)

[More details here](https://caprover.com/docs/get-started.html#step-3-install-caprover-cli)