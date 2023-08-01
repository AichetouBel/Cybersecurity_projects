#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# Installation de MISP

## prérequis: 

Nous avons installé MISP à partir d'une image docker:
* Installer les packages complémentaires pour docker :``sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release``
* Mise à jour le système: ``sudo apt-get update``
* Configurer un répertoire stable

``` C
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

```

* Mettez à jour les paquets, et installez la dernière version de Docker.

    * ``sudo apt-get update``
    * ``sudo apt-get install docker-ce docker-ce-cli containerd.io``

## Instellation
* Clonez le projet MISP depuis le github.
    * ``cd ~``
    * ``git clone https://github.com/harvard-itsecurity/docker-misp.git``
* Accédez au répertoire de MISP
    * ``cd docker-misp``
* Modifiez le ficher build.sh
    * ``sudo nanoà build.sh ``
    * Changer les champs: MYSQL_MISP_PASSWORD et MISP_GPG_PASSWORD
* Construire l'image du docker
    * ``sudo ./build.sh``
* Créez un répertoire pour la base de données de MISP.
    * ``mkdir -p /docker/misp-db``
* Créez un certificat auto-signé pour MISP.
    * ``mkdir -p /docker/certs/ ``
    * ``sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /docker/certs/misp.key -out /docker/certs/misp.crt ``
* Démarrez le container:

        * ``cd /docker-misp``
        *  docker run -it -d \
        -p 443:443 \
        -p 80:80 \
        -p 3306:3306 \
        -v /docker/certs:/etc/ssl/private \
        -v /docker/misp-db:/var/lib/mysql \
        harvarditsecurity/misp

Accéder à l'interfrace graphique de MISP à partir d'un navigateur sur URL: ``http:0.0.0.0:80/`` Vous aurez un pop-up `` Warning Security Risk Ahead`` cliquer sur `` Advanced`` puis sur `` Accept the risk and continue``.

Utiliser les identifiants par défaut pour y accéder:

    * Login: admin@admin.test
    * Password: admin
Une fois connecter, vous allez être demandés à changer le mot de passe.


## Configuration de MISP


### Administration
* Aller à Administration > Server Settings & Maintenance > MISP Settings et changer les configurations ci-dessous:
    * MISP.live=TRUE
    * MISP.disable_emailing=TRUE
    * MISP.baseurl=IP do MISP
NB: Pour changer la valeur d'un champ, il suffit de double cliquer sur sa valeur.
* Aller à Administration > Scheduled Tasks et changer la valeur du fetch_feeds  24 et cliquer sur Update All.
* Par défaut MISP contient une variété des sources des événements, nous avons besoin de les activer. 
    * Aller sur ``Sync Actions`` > ``List Feeds``.
    * Cliquer sur ``Load default feed metadata``.
    * Cliquer sur le menu ``All feeds``.
    * Sélectionnez tous les champs et cliquer sur ``Enable Selected`` et puis sur ``Fetch and store all feed data``.
Vous pouvez voir la progression du téléchargement dans Administration > Jobs.

### Créer un utilisateur:

Allez sur Administration, Add User, entrer votre email, sélectionner un rôle et désélectionner tous les champs en bas.

Pour le PGP-key vous pouvez le générer à partir de votre machine ubuntu, si vous n'avez pas le générateur vous pouvez l'installer avec les commandes suivantes: 

    * ``sudo apt update`` 
    * ``sudo apt install gnupg``

1. Générez un GPG key avec la commande suivante: ``sudo gpg --gen-key`` vous aller être demandé à renseigner quelques champs(le nom, address email, passphrase) et vous pouvez être demandé à renseiger les suivants: 

* le type de clés que vous voulez, sélectionner 1 pour l'option par défaut.
* la taille de clé: 2048 ou tapez ENTRE
* la validité de la clé: tapez (0) pour une validité à vie.
entrée Y pour confirmer.
2. Vérifier la clé: ``sudo gpg --list-keys`
vous devez voir votre clé genérée avec ces informations contituer d'un bolc de 9 avec 4 letters par bloc.
Metter la clé dans son champ correspondant sur MISP interface graphique(soit lors de la création de l'utilisateur soit après en accédant à My profile > Edit)





## Troubelshooting
* Si vous aurez l'erreur suivante en démanrrant le container: 

        * docker: Error response from daemon: driver failed programming external connectivity on endpoint silly_jepsen (9b4a7157e0a2062e3adcb27e3456d8934005e15075544e5a2a307b22580a2d91): 
        Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use.

Solution:

    * Exécuter la commande à partir du répertoire de l'image docker de MISP `` cd /docker-misp 
    * désactiver apache2 avec la commande: sudo systemctl stop
* Si vous ne pouvez pas accéder à l'interface graphique: 
    * Vérifier si le port 80 est utilisé par une autre application: sudo netstat -lpn |grep :80
