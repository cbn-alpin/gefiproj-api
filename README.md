# gefiproj-api
Ce dépôt contient le backend du projet GEFIPROJ. https://gefiproj.cbn-alpin.fr/

## Installation de l'API
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
## Création du fichier .flaskenv
- La configuration de l'application utilise des variables d'environnement présentes le fichier `.flaskenv`.
- Pour créer le fichier .flaskenv vous pouvez copier le fichier d'exemple : `cp sample.flaskenv .flaskenv`
- Vous pouvez dès à présent compléter les paramètres suivant :
  - `JWT_SECRET` : un chaîne de texte relativement longue qui sera utilisé comme "secret" lors de la génération d'un JWT. Vous pouvez par exemple utiliser un UUID et le générer avec la commande Linux : `uuidgen`
- Compléter au fur et à mesure de l'installation de Gefiproj décrite ci-dessous les paramètres manquant.

## Installation de la base de données
- La configuration des accès aux base de données se fait via des variables d'environnement `DATABASE_*` du fichier `.flaskenv`.
- Vous pouvez utiliser et configurer 3 types de bases de données correspondant chacune aux 3 types d'environnement de travail disponible : `dev`, `test` et `prod`.
- Ces bases peuvent être locales ou sur un serveur distant.
- Créer les bases de données correspondantes dans Postgresql.
- Pour chaque base, exécuter dans l'ordre les fichiers SQL présents dans le dossier `resources/database/` et nummérotés de 001 à 004.
  - Pour la base de `prod`, vous pouvez exécutez aussi les fichiers 005 et 006.
  - Pour les bases de `dev` et `test`, vous pouvez exécuter en plus les fichiers présents dans `resources/database/samples/`.


### Modifier les mots de passe utilisateurs
Dans la base de données, si vous souhaitez modifier les mots de passe des utilisateurs, il est possible 
de procéder ainsi pour générer la chaîne cryptée du mot de passe :

- Activer l'environnement virtuel : `source ./cbna_env/bin/activate`
- Lancer une console Python : `python`
- Charger la bibliothèque Passlib : `from passlib.hash import pbkdf2_sha256`
- Créer le mot de passe crypté : `print(pbkdf2_sha256.hash('<mon-mot-de-passe>'))`
- Copier/coller le hash qui s'affiche dans le code SQL de modification ou de création d'un utilisateur ou directement dans le champ `password_u` de la table `utilisateur`.

## Configuration de l'accès à Google Sheet
Pour pouvoir exporter des bilans vers Google Sheet, il faut créer un *compte de service* sur *Google Cloud Platform* en suivant ce lien https://console.cloud.google.com/ .
Il vous faudra créer un projet, un compte et une clé.

Vous pouvez récuperer le fichier `google-credentials.json` soit depuis l'interface de *Google Cloud Platform*, soit depuis le dossier *Google Drive*. Vous devez ensuite le placer dans le dossier `config/` du projet. Lien d'aide à la création du fichier `google-credentials.json` : https://cloud.google.com/docs/authentication/getting-started

Il faut aussi compléter tous les paramètres du fichier `.flaskenv` débutant par `GS_*` à l'aide des informations présentes sur *Google Cloud Platform* > *compte de service*

## Tests unitaires
Afin de pouvoir lancer les tests unitaires, il faut avoir configuré les paramètres `DATABASE_TEST_*` et `JWT_*` dans le fichier `.flaskenv`.
**ATTENTION** ⚠️ : assurez vous que les paramètres de la base de données de test sont bien différents de ceux de la production.

### Création d'un JWT Token
- Lancer l'API à l'aide de Flask comme indiqué ci-dessous.
- Se rendre sur l'interface de Swagger : http://127.0.0.1:5000/#/Authentification/login
- Sur le web service POST /api/auth/login, cliquer sur "Try it out"
- Dans le body, remplacer les valeurs des champs login et password par celle précédement sotcker dans votre base de données pour un utilisateur donné.
- Cliquer sur "Execute" et le résultat s'affichera dessous.
  - En cas d'erreur, regarder dans la Console les messages affichés par Flask.
  - En cas de succès, copier votre JWT Token dans le fichier `.flaskenv` au niveau de la valeur du paramètre `JWT_TEST_TOKEN`.

### Lancement des tests
- Lancer les tests avec :
```shell
source .flaskenv && GEFIPROJ_ENV="test" python -m unittest discover -v -s tests/ -p '*_tests.py'
```
La variable d'environnement `GEFIPROJ_ENV` permet de definir le type de base de données qui sera utilisé...

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
- Lancer le projet en utilisant les informations présente dans `.flaskenv` : 
    ```shell
    GEFIPROJ_ENV="dev" flask run
    ```
- La variable d'environnement `GEFIPROJ_ENV` permet de controller l'envrionnement de la base de données dans lequel Flask est lancé. Les valeurs possibles sont : `dev`, `test` et `prod`. Les informations de connexion à la base de données seront chargées en conséquence (voir fichier `.flaskenv`).

Vérifier que le projet est lancé en allant sur `http://127.0.0.1:5000/#/Authentification/login` et tester les web services.

## TODO

- [ ] Utiliser requirements.txt ou Pipfile (faire un choix)
- [ ] Faire le point sur l'utilisation de Docker et Travis
- [ ] Trouver une solution alternative à Caprover à base de container et de fichier Docker-Compose
- [ ] Indiquer dans le wiki de gefiproj-webapp les termes anglais correspondant aux termes français
- [ ] Traduire la base de données en anglais
- [ ] Simplifier la génération du fichier de config à partir des variables d'environnement


#  Test Server with Dockerfile
```
cmd=docker build -t cbna_backend:v1 .
docker run -d -p 5000:5000 cbna_backend:v1
```
If you need to parse .env in build you can use this script helping :

```bash
#!/bin/bash
awk '{ sub ("\\\\$", " "); printf " --build-arg %s", $0  } END { print ""  }' $@

docker build $(./buildargs.sh .env) -t cbna_backend:v1 .
````


```bash
#!/bin/bash

#docker build "${opts[@]}" -t cbna_backend:v1 .
function create_build_arg {
        awk '{ sub ("\\\\$", " "); printf " --build-arg %s", $0  } END { print ""  }' $@ < .env
}

OUTPUT=$(create_build_arg)
cmd+='docker build'
cmd+=$OUTPUT
cmd+=' -t cbna_backend:v1 .'

eval $cmd
```

Copy file from pgAdmin Docker contenair to host

```bash
docker cp 0659194cca59:/var/lib/pgadmin/storage/contact_cbn-alpin.fr/test1 /home/ubuntu
```


# Own Paas serveur with CapRover  🚀
There are many easy CI/CD platforms that offer generous free minutes for your builds, for example GitHub and GitLab both offer free minutes for private repositories and unlimited free minutes for public repositories.
## Prerequisites
    
### Configure Firewall

```bash
sudo ufw allow 80,443,3000,996,7946,4789,2377,5000,5432/tcp; sudo ufw allow 7946,4789,2377/udp;
```

### Step 1: CapRover Installation
```
docker run -p 80:80 -p 443:443 -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock -v /captain:/captain caprover/caprover
```

### Step 2: Connect Root Domain

Let's say you own mydomain.com. You can set *.something.mydomain.com as an A-record in your DNS settings to point to the IP address of the server where you installed CapRover. Note that it can take several hours for this change to take into effect. It will show up like this in your DNS configs:

```
*.gefiproj.cbn-alpin.fr
```

- TYPE: A record
- HOST: *.gefiproj.cbn-alpin.fr
- POINTS TO: 149.202.162.89

### Step 3: Install CapRover CLI

```
docker exec -it [DOCKER CONTAINER ID] bash
npm install -g caprover
caprover serversetup
```

![Linux terminal](resources/img/1.png)

Now we can connect to : [https://captain.gefiproj.cbn-alpin.fr/](https://captain.gefiproj.cbn-alpin.fr/)


### Step 4: Install Apps

####  Create and Deploy API Serveur

![Linux terminal](resources/img/3.png)

- When you set the name of app, it's Automatically set as sub-domaine name (`i.e. api.cbna.*`). You change the sub-domaine name in text form and click `Connect New Domain`.
- Don't forgot to click to `Enable HTTPS`

Before start deployment, we have to set the environment variables. Ask your **administrator** for more details.

![Linux terminal](resources/img/5.png)

In `Deployment` tabs we set all GitHub parameters

![Linux terminal](resources/img/4.png)

For this first deployment, we will force build by clicking in `Force Build`. After we will configure the URL generate by CapRover in GitHub /settings/hooks :

`https://captain.cbna.*/api/v2/user/apps/webhooks/triggerbuild?namespace=captain&token=eyJhbGci...`

####  Create and Deploy Frontend - Angular SPA

More easy then the API Server, juste have to deploy with GitHub like before and configure the webhook for the next push in the branch you define.

### Backup

We can backup CapRover configs in order to be able to spin up a clone of this server. Note that your application data (volumes, and images) are not part of this backup.

[More details here](https://caprover.com/docs/get-started.html#step-3-install-caprover-cli)