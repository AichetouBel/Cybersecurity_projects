#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# Surveillez un serveur Lunix avec nagios

 Par la suite nous allons surveiller un serveur lunix avec nagios. Pour faire ceci nous avons utilisé une machine ubuntu installer sur une machine virtuelle comme notre serveur lunix et la machine sur laquelle nous avons installé nagios comme serveur nagios.

## Configuration du serveur lunix 

1. Identifier le nom de l'hôte et son address ip avec les commandes suivantes:

`` Hostname ``

`` ifconfig ``

Pour notre cas hostname: linuxServer et address ip: 192.168.239.132


 1. Installer le NRPE

 Pour surveiller un serveur lunix nous avons besoin d'installer NRPE sur le serveur avec la commande suivante:

```sudo apt install nagios-nrpe-server nagios-plugins -y ``

2. Modifier le fichier de configuration de nrpe avec nano ou n'importe quel editeur que vous voulez.

``sudo nano /etc/nagios/nrpe.cfg``

* Ajouter l'adresse de votre machine dans le fichier de configuration ``/etc/nagios/nrpe.cfg`` en changeant l'adresse ip dans la ligne suivante par le votre ``server_address=127.0.0.1`` 

``server_address=192.168.239.132``

NB:assurer vous que ce ligne de code n'est pas commanté.

* Ajouter l'adresse ip du serveur nagios au ``allowed_host`` pour notre cas c'est le 192.168.239.136 .

``allowed_host: 127.0.0.1, 192.168.239.136``

3. Rédemarrer nrpe:

* ``sudo systemctl restart nagios-nrpe-server``
* ``sudo systemctl enable nagios-nrpe-server``

Aprés chaque modification dans le fichier de configuration de nrpe il faut rédemarer nrpe et le permetterr..


4. Configurer le firewall 

Par défaut nagios nrpe agent écoute sur le port 5666, donc il faut le permettre sur le firewall.

`` sudo ufw status ``

`` sudo ufw enable ``

`` sudo ufw allow 5666/tcp ``

 5. permetter ssh pour avoir l'accès à distance à notre serveur lunix.

 ``sudo ufw allow ssh``

 6. vérifier le status de firewall

`` sudo ufw status ``


### ``Configuration de Nagios sever``

Maintenant accéder à la machine sur laquelle vous avez installé nagios.

1. Créer un dossier ``servers`` s'il n'existe pas dans ``/usr/etc/local/nagios/etc``

* ``cd /usr/local/nagios/etc``
* ``mkdir servers``

2. Changer la permission du dossier ``servers``

* ``sudo chmod 775 servers``
* ``sudo chown nagios:nagios servers``

3. pour que la configuration dans le dossier ``servers`` soit chargée par nagios lors de son démarrage, on doit indiquer le chemin vers le dossier dans le fichier nagios.cfg en décommantant ou ajoutant le ligne de code suivant ou en l'ajoutant s'il n'existe pas `` cfg_dir=/usr/local/nagios/etc/servers``

4. créer un fichier cfg

Dans le dossier ``servers`` créer un fichier cfg (ce sont les fichier de configuration de nagios)

* ``cd servers``
* ``sudo touch lunixServer.cfg``

</br>


### ``Configuration de l'hôte ``

* ``sudo nano lunixServer.cfg``

pour configurer  l'hôte entrer le bout du code suivant en changeant le nom de l'hôte, l'alias, et l'addresse ip par le vôtre.
NB: L'addresse ip, l'alis et l'hôte sont ceux du serveur linux.

define host{
use                     linux-server
host_name               linuxServer
alias                   linuxServer
address                 192.168.239.132
}

NB: l'option ``use`` indique le template qui va être utilisé par nagios 
5. changer la permission du fichier linuxServer.cfg

``sudo chown nagios:nagios linuxServer.cfg``
``sudo chmod 664 linuxServer.cfg``

6. Vérifier le ficher de configuration de nagios pour toute erreur sur le serveur nagios avec la commande suivante:

`` sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg``

si vous voyez ``Total warnings=0`` et ``Total Errors=0`` ceci implique que la configuration est bonne. Si non, vous avez un problème dans votre configuration .

7. Permettre le port 5666

``sudo ufw allow 5666/tcp``
``sudo ufw status``

8. Rédemarrer nagios

``sudo systemctl restart nagios.service``


9. Vérification de l'hôte 

Vérifier que l'hôte a bien été ajouté. Accéder à l'interface graphique de nagios et vous devez voir votre serveur linux dans la liste des hôtes.

#### `` Configuration du service``


``Pré-requis``

1. Installer nagios nrpe plugins sur la machine , serveur linux:

`` sudo apt install nagios-nrpe-plugin``

2.  Verifier la commande check_nrpe

* ``cd /usr/lib/nagios/plugins``
* ``ls``

Vous devez voir la commande check_nrpe

3. déplacer la commande dans le dossier libexec de nagios

`` cp /usr/lib/nagios/plugins/check_nrpe /usr/local/nagios/libexec ``

4. Définir la commande check_nrpe dans le fichier commands.cfg de nagios

* ``cd /usr/local/nagios/etc/objects``
* ``sudo nano commands.cfg``
* Ajouter le bout du code suivant: 

define command {

    command_name    check_nrpe
    command_line    $USER1$/check_nrpe -H $HOSTADDRESS$ -c $ARG1$
}


``L'ajout des services``

1. sudo nano linuxServer.cfg

2. Ajouter le bout du code suivant à votre code:

define service{
use                             generic-service
host_name                       linuxServer
service_description             Current Load
check_command                   check_nrpe!check_load
}


ce service permet de voir la charge actuelle sur notre serveur linux.

3. Rédemarer nagios ``sudo systemctl restart nagios.service`` 

4. Accéder à l'interface graphique de nagios, aller dans les services et vous devez voir le service que vous venez d'ajouter.

NB: vous pouvez voir pending sur le status du service c'est normale, ça va prendre quelque temps avant d'être activé.
NB: par défaut nagios vérifie les services chaque 5 min, vous pouvez changer l'intervalle de vérification dans le fichier ``nagios.cfg``, mais faite attention de configurer un intervalle trop petit car vous risquez que la machine client vous considère comme spam.

# Troublshooting 

1. Vérifier la connexion ssh entre les deux hosts en essayant de se connecter en ssh à partir du nagios server vers linux server avec la commande ``ssh linuxServer@192.168.239.132`. Si la connexion se passe pas:
     * vérifier que vous avez bien installé ssh sur la machine: ``sudo service ssh status``
         * Si ssh n'est pas reconnu installer le: ``sudo apt install ssh`` 
         * Si ssh est désactivé, il faut l'activer: ``sudo service ssh start ``
     * vérifier que vous avez ajouté une clé ssh. Si ce n'est pas le cas:
         * Généré une clé ssh: ``ssh-keygen -t rsa``. choisisser l'emplacement par défaut en cliquant sur entrer, la même chose pour le passphrase et un fichier id_rsa doit être généré.
         * Accéder à l'emplacement par défaut du fichier id_rsa et exécuter la commande suivante pour ajouter votre clé publique aux clé authoris"es par votre machine: ``cp id_rsa.pub authorized_keys``.
2. vérifier le fichier nrpe.cfg (sur l achine linux server) pour détecter toute possible erreur dans la configuration en exécutant la commande suivante:``sudo systemctl status nagios-nrpe-server``.
3. vérifier que le paramétre ``don't blame nrpe`` dans le fichier nrpe.cfg est égal à 1
4. vérifier que tout service que vous avez ajouté dans le fichier linuxServer.cfg sur la machine serveur nagios est bien défini:
     * Dans fichier nrpe.cfg sur la machine linux server.
     * Se trouve Parmis les commandes dans /usr/lib/nagios/plugins sur la machine nagios server.
     * Dans le fichier /usr/local/nagios/etc/objects/command.cfg sur la machine nagios server.
5. vérifier que les fichiers de configuration sur la machine nagios server ne contiennent pas des erreur ```sudo systemctl status nagios.service``  et ``sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg``