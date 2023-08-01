#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# ``Nagios Installation & Configuration``


## Nagios: 


C'est une application de surveillance réseaux et système. Elle permet la surveillance de tous les composants critiques de l’infrastructure(les hôtes, les applications, les services, les systèmes d’exploitation, les serveurs, les protocoles réseau, les bases de données... ). Elle permet également la création des alertes pour notifier les administrateurs sur les dysfonctionnements dans le système ou les équipements réseaux.


Par la suite nous allons voir la procédure d'installation de Nagios core 4.4.6 sur ubuntu 18.04
 
## Prè-requis:

1. Méttre à jour le système

``sudo apt-get update``

2. Installer apache et php:

``sudo apt-get install -y autoconf gcc libc6 make wget unzip apache2 php7.2 libapache2-mod-php7.2 libgd-dev``
NB: si vous avez php déjà installé sur votre machine, vous devez installer la version du package  `` libapache2-mod-php7.2`` qui correspond à la version de php dont vous disposez.
vous pouvez vérifier votre version de php avec la commande ``php -v ``

## Installation de Nagios

``NB:`` à la fin de cette documentation vous trouvez une section ``Troubleshooting``, si vous rencontrez un problème, vérifiez s'il a été traité dans cette section. 
 

1. télécharger nagios:

``cd /tmp``

`` wget -O nagioscore.tar.gz https://github.com/NagiosEnterprises/nagioscore/archive/nagios-4.4.6.tar.gz``

``tar xzf nagioscore.tar.gz``

2. Compillation

``cd /tmp/nagioscore-nagios-4.4.6``

``sudo ./configure --with-httpd-conf=/etc/apache2/sites-enabled``

``sudo make all``

3. Créer  un group et un utilisateur nagios 

``sudo make install-groups-users``

``sudo usermod -a -G nagios www-data``

4. installer les fichiers binaires

``sudo make install``

5. installer service/ Daemon 

``sudo make install-daemoninit``

6. Installer commande mode:

``sudo make install-commandmode``

7. Installer les fichiers de configuration 

``sudo make install-config``

8. Installer apache web server
``sudo apt-get install apache2 libapache2-mod-wsgi``

* si vous aurez l'erreur: ``Package 'libapache2-mod-wsgi' has no installation candidate`` lancer la commande suivante ``sudo apt-get install libapache2-mod-wsgi-py3`` 

``sudo make install-webconf``

``sudo a2enmod rewrite``

``sudo a2enmod cgi``

9. Configurer le firewall 
Nous avons besoin de permettre le trafic sur le port 80(utilisé par défaut par apache) pour pouvoir accéder à l'interface graphique de nagios.

``sudo ufw allow Apache``

``sudo ufw reload``

10. Créer l'utilisateur admin de nagios

C'est l'identifiant de l'utilisateur avec laquelle on va accéder à l'interface graphique de nagios. Dans notre cas c'est nagiosadmin.

Vous allez être demandés à choisir un mot de passe également.

``sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin``

11. Ajouter apache full au firewall `` sudo ufw allow 'Apache Full' ``
12. Rédemarrer le serveur nagios ``sudo systemctl restart apache2.service``

* Si vous aurez l'erreur ``Failed to start The Apache HTTP Server`` exécuter la commande suivante ``journalctl -xeu apache2.service`` vous  aurez une description détaillée de l'erreur. 
    * Vérifier que vous n'avez pas deux versions de php installé qui crée un conflis avec la commande suivante  ``sudo find / -name '*libapache2-mod-php*'``  supprimer l'une des deux versions avec la commande ``sudo apt-get purge libapache2-mod-php7.2 php7.2`` en remplaçant 7.2 avec le numéro de votre version.
    * Si  vous avez l'erreur suivante: ``apache /usr/sbin/apachectl: 174: /usr/sbin/apache2: not found`` exécuter la commande suivante: ``sudo apt install --reinstall apache2-bin`` et rédemarrer apache2.

13. Démarrer le service / Deamon 

``sudo systemctl start nagios.service``

Nagios est maintenant installé. Pour vérifier cela, il faut accéder à l'interface graphique de nagios.

*  ouvrir un navigateur web
*  tapez localhost/nagios

vous allez être demandés à se connecter, entrer l'identifiant et le mot de passe que vous avez choisis par avant et vous devez être capable d'accéder à la page d'accueil de nagios.

Pour que nagios peut surveiller les équipements il a besoin de certains plugins que nous allons installer par la suite.

## Instalation des plugines de nagios

`` Pré-réquis``

Assurez-vous que le package suivant est bien installer, entrez la commande ci-dessous:


1. Télécharger les plugins de nagios

``cd /tmp``

``wget --no-check-certificate -O nagios-plugins.tar.gz https://github.com/nagios-plugins/nagios-plugins/archive/release-2.3.3.tar.gz  ``

``tar zxf nagios-plugins.tar.gz``

2. compiler le fichier et l'installer


``cd /tmp/nagios-plugins-release-2.3.3/``

``sudo ./tools/setup``

``sudo ./configure``

``sudo make``

``sudo make install``

3. Rédemarrer nagios

``sudo systemctl restart nagios.service``

Nagios est bien installé et configuré.

Après l'installation, il faut attendre quelques minutes normalement toutes les services de la machine host vont être accessibles.
Si le service SSH est en rouge ceci peut indiquer que votre machine ne possède pas du serveur Openssh qu'il faut installer.

* Installation du ssh``

    * ``sudo apt install ssh``
    * ``sudo service ssh start`` or ``sudo systemctl start ssh``

Les Commandes de service Deaomon pour  Nagios:
* ``sudo systemctl start nagios.service``
* ``sudo systemctl stop nagios.service``
* ``sudo systemctl restart nagios.service``
* ``sudo systemctl status nagios.service``


# Troubleshooting
1. vérifier que les fichiers de configuration de nagios serveur ne contiennent pas des erreurs ```sudo systemctl status nagios.service``  et ``sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg``

2. Si vous aurez l'erreur suivante: ``It appears as though you do not have permission to view information for any of the hosts you requested...``

Il faut changer le nom de l'admin dans le fichier cgi.cfg. Cette erreur est due au faite que dans le fichier de configuration de nagios le nom de l'admin par défaut c'est: ``nagiosadmin``, de ce fait, si lors de l'installation vous choisissez un nom différent de ceci, vous n'êtes plus reconnu comme l'admin par défaut, donc il faut le changer manuellement.

* Rccéder au fichier de configuration de nagios: ``sudo nano /usr/local/nagios/etc/cgi.cfg`` .
* Changer toutes  les permissions avec le nom de l'admine vers le nom de l'admine  que vous avez choisi. 
* Redemarrer nagios.

3. Si vous aurez l'erreur: ``nagios The requested URL was not found on this server.`` exécuter les commandes suivantes:

    * sudo cp /etc/apache2/nagios.conf /etc/apache2/sites-available/nagios.conf

    * sudo ln -s /etc/apache2/sites-available/nagios.conf /etc/apache2/sites-enabled/

    * sudo systemctl restart apache2






