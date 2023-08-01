#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

## Splunk and Nagios Integration


Dans cette documentation nous allons voir comment envoyer les données de Nagios core à Splunk pour la centralisation des données dans notre SOC.
Il y'a deux méthodes pour le faire soit en surveillant le fichier de journaux de Nagios avec Splunk ou soit en installant un plugin appelé ``Splunk add-on for Nagios core``

## Surveiller le fichier de journaux de Nagios avec Splunk

* Accéder à l'interface graphique de splunk 
* Cilquer sur l'option ``Add Data``
* Cliquer sur l'option ``Monitor``
* Cliquer sur ``file&directories``
* Naviguer vers l'emplacement du fichier log de nagios(nagios.log). Par défaut, il est dans la répertoire ``/usr/local/nagios/var``et cliqué sur ``Next``.
* Cliquer sur ``save as``. choisissez le nom que vous voulez et le type d'application qui est ``Search&Reporting`` et cliqué sur Next.
* Balayer en bas pour choisir un index. Cliquer sur créer un index:
   * Choisissez un nom pour votre index.
   * index Data type: event.
   * Les autres options, laissaient les par défaut.
   * Cliquer sur save
* Choisissez votre index parmi la liste des indexe
* Cliquer sur ``Review``
* Cliquer sur ``submit``
* Cliquer sur ``start searching`` pour voir les données
* Sur la barre de recherche fitrer par le nom de votre index (index= "nomDeVotreIndex") ou le sourcetype. Plusieurs filters pertinents peuvent être crées grace ou SQL(Langage de recherche dans la base de données de Splunk).

Vous devez être capable de voir les journaux de Nagios. Grâce à cette fonctionnalité de surveillance continue de splunk vous pouvez voir les futurs journaux également, lorsqu'ils vont être générés.


## Splunk add-on for Nagios core installation
Dans cette méthode, nous allons voir les étapes d'intégration de splunk 8.2.5 avec nagios core 4.4.6 .
L'intégration se fait à travers un add-on en splunk appellé ``Splunk add-on for Nagios core``

1. Connectez vous sur l'interface graphique de splunk.  
2. Allez dans Apps --> find more apps et chercher "Splunk add-on for Nagios core" et installer le plugin.

Vous devez être capable de voir le add-on que vous venez d'ajouter avec vos applications, à gauche de la page d'acceuil. Si ce n'est pas le cas acceder à app manager: 
* checrher "Splunk add-on for Nagios core et cliquer sur "Edit proporties"
* changer la visibilité de l'application 
  
  <br/>
###  Configurer l'instance Nagios core pour "Splunk Add-on for Nagios Core"
<br/>

Pour utiliser le module complémentaire Splunk pour Nagios Core, vous devez préparer votre instance Nagios Core en activant les journaux et les éléments de journal et en mettant à jour les configurations.

``NB``:Dans toutes les instructions de configuration et les exemples suivants, remplacez $NAGIOS_HOME par votre dossier Nagios. Par exemple, /usr/local/nagios.

1.  activer les journaux et les éléments de journal

* Acceder au fichier nagios.cfg en mode écriture par defaut il est dans le dossier  ``$NAGIOS_HOME/etc``
* vérifier que les paramettres ci-dessus sont configurer comme suit:
  
``log_file=$NAGIOS_HOME/var/nagios.log``

``log_notifications=1``

``log_service_retries=1``

``log_host_retries=1``

``log_event_handlers=1``

``log_initial_states=1``

``log_current_states=1``

``log_external_commands=1``

``log_passive_checks=1``

2. mettre à jour les configuration dans nagios.cfg 

vérifier que les paramettres ci-dessus sont configurer comme suit, s'il n'exite pas, faut les ajouter à la fin du fichier:
   
``process_performance_data=1``

``host_perfdata_file_mode=a``

``service_perfdata_file_mode=a``

``host_perfdata_file_processing_interval=86400``

``service_perfdata_file_processing_interval=86400``

``service_perfdata_file=$NAGIOS_HOME/var/service-perfdata``

``host_perfdata_file=$NAGIOS_HOME/var/host-perfdata``

<br/>

``NB:`` il faut pas configurer les paramettres suivants:

``#service_perfdata_command=...``

``#host_perfdata_command=...``

``#service_perfdata_file_template=...``

``#host_perfdata_file_template=...``

Si elles sont commentées, gardez-les commentées. Si elles sont définies, supprimez ou commentez les options.

Si ces lignes sont définies, l'extractions des champs dans l'add-on peuvent échouer.

3. mettre à jour les configurations dans templates.cfg 

Mêttre à jour les configurations dans /usr/local/nagios/etc/objects/templates.cfg pour l'hôte et service templates.
* sudo nano templates.cfg
* changer les paramétres suivants: ``process_perf_data 1`` ; ``Process performance data``
  
4. Validez les configurations
   * /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
  
  Cette commande permet de verifier s'il y'a des erreurs de configuration dans nagios

5. Rédemarrer Nagios
   * sudo systemctl restart nqgios.service

### Configuration Des entrées de journaux(log inputs)

Configurez vos entrées tout en prenant en considération les données que  vous souhaitez collecter et à votre version de Splunk DB Connect.
``Prérequis``
* Installer Splunk DB connect: c'est 
  Configuration des entrées de logs pour l'extension Splunk pour Nagios Core

1. Accéder au fichier ``$SPLUNK_HOME/etc/apps/Splunk_TA_nagio-core/local/inputs.conf`` en mode ecriture.

NB: si vous n'avez toujours pas l'accée même en utilisant sudo, vérifier les permissions sur le repertoire avec la commande ``ls -ll``.

Pour donnée l'accés en écriture et en exécution, lancer la commande suivante: ``sudo chmod 777 local``

Si le fichier ``inputs.conf`` n'existe pas il faut le créer.

1. Ajouter les commandes ci-dessus dans le fichier inputs.conf
   

[monitor://$NAGIOS_HOME/var/nagios.log]
  
sourcetype = nagios:core
 
[monitor://$NAGIOS_HOME/var/host-perfdata]

sourcetype = nagios:core:hostperf
 
[monitor://$NAGIOS_HOME/var/service-perfdata]

sourcetype = nagios:core:serviceperf

2. Rédemarer splunk 
``sudo systemctl restart splunkd.service``

<br/>

### Installer NDoutils


``NDOUtils`` est un Add-on pour Nagios, une application permettant la surveillance système et réseau. Il permet de stocker dans une base de données MySQL ou dans un fichier plat : La configuration des serveurs supervisés Les événements Les états des éléments supervisés.


``Pres-requis``

La configuration du splunk DB connect depend de sa version car les versions antérieures nécessite des prés-réquis différents, pour notre cas nous avons la versions 3.8.0 installée.

1. Installer MySQL

NB: ``Cette étape est à dépasser si vous avez déjà Mysql installer``

lancer la commande suivante: 

a. ``sudo apt install mysql-server``

b. ``sudo mysql_secure_installation`` cette commande vous permet de configurer votre Base de données Mysql.

c. ``sudo apt install -y libmysqlclient-dev libdbd-mysql-perl`` 

Pendant l'installation, il vous sera demandé le mot de passe de l'utilisateur "root". 

pour accéder à mysql tapez la commande suivante: ``mysql -u root -p``

2. Configurer Mysql

Vérifiez qu'il est en cours d'exécution :``ps ax | grep mysql | grep -v grep``
La sortie doit ressemble à cell-ci:
 ``8142 ?        Ssl    0:01 /usr/sbin/mysqld``

NDOUtils nécessite la création d'une base de données que nous allons appelée nagios.

a. Connecter à Mysql avec la commande suivante:

 ``mysql -u root -p `` 

b. Créer une base de données:
  
* ``CREATE DATABASE nagios DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;``

c. Créer un utilisateur Ndoutils
* ``CREATE USER 'ndoutils'@'localhost' IDENTIFIED BY 'ndoutils_password';``

d. Garantire des privélége à l'utilisateur Ndoutils

* ``GRANT USAGE ON *.* TO 'ndoutils'@'localhost' IDENTIFIED BY 'ndoutils_password' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 ``

* ``MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0; ``

* ``GRANT ALL PRIVILEGES ON nagios.* TO 'ndoutils'@'localhost' WITH GRANT OPTION ; ``

e. Quitter Mysql:

``/q``

f. Assurer que la base de données à été bien créer

echo 'show databases;' | mysql -u ndoutils -p'yourPassword' -h localhost

La sortie doit ressemble à celle-ci:

Database

information_schema

nagios

test

3. Configurer Linux Kernel

a. Créer une copie de backup du fichier /etc/sysctl.conf

``sudo cp /etc/sysctl.conf /etc/sysctl.conf_backup``

b. Exécuter les commandes suivantes:

sudo sed -i '/msgmnb/d' /etc/sysctl.conf

sudo sed -i '/msgmax/d' /etc/sysctl.conf

sudo sed -i '/shmmax/d' /etc/sysctl.conf

sudo sed -i '/shmall/d' /etc/sysctl.conf

sudo sh -c 'printf "\n\nkernel.msgmnb = 131072000\n" >> /etc/sysctl.conf'

sudo sh -c 'printf "kernel.msgmax = 131072000\n" >> /etc/sysctl.conf'

sudo sh -c 'printf "kernel.shmmax = 4294967295\n" >> /etc/sysctl.conf'

sudo sh -c 'printf "kernel.shmall = 268435456\n" >> /etc/sysctl.conf'

sudo sysctl -e -p /etc/sysctl.conf

<br/>


La dernière commande doit afficher une sortie comme suit :

kernel.msgmnb = 131072000

kernel.msgmax = 131072000

kernel.shmmax = 4294967295

kernel.shmall = 268435456

NB: Ce n'est pas nécessaire de rédemarrer le serveur 

<br/>
``Installation``

<br/>

1. Télécherger Ndoutils
  

``cd /tmp ``

``wget -O ndoutils.tar.gz https://github.com/NagiosEnterprises/ndoutils/archive/ndoutils-2.1.3.tar.gz ``

``tar xzf ndoutils.tar.gz``

2. Compiler Ndoutils

``cd /tmp/ndoutils-ndoutils-2.1.3/``
c
``sudo ./configure``

``sudo make all``

3. Installer les binaires

``sudo make install``

4. Initialiser la base de données

``cd db/``

``sudo ./installdb -u 'ndoutils' -p 'ndoutils_password' -h 'localhost' -d nagios ``

``cd .. ``

La sotie ressemble à celle-ci:

DBD::mysql::db do failed: Table 'nagios.nagios_dbversion' doesn't exist at ./installdb line 52.

** Creating tables for version 2.0.1

     Using mysql.sql for installation...

** Updating table nagios_dbversion

Done!

5. Installer les fichiers des configurations

sudo make install-config

sudo mv /usr/local/nagios/etc/ndo2db.cfg-sample /usr/local/nagios/etc/ndo2db.cfg

sudo sh -c 'sed -i 's/^db_user=.*/db_user=ndoutils/g' /usr/local/nagios/etc/ndo2db.cfg'

sudo sh -c 'sed -i 's/^db_pass=.*/db_pass=ndoutils_password/g' /usr/local/nagios/etc/ndo2db.cfg'

sudo mv /usr/local/nagios/etc/ndomod.cfg-sample /usr/local/nagios/etc/ndomod.cfg


ceci install les fichiers de configuration de toute même configure Mysql credentiales  pour que Ndoutils peut connecter à la base de données.

Deux fichiers de configurations vont été créer dans le répertoire /usr/local/nagios/etc/ :  ndo2db.cfg et  ndomod.cfg

Assurer vous que les lignes de codes suivants sont bien défini dans votre fihier  ndo2db.cfg:

db_user=ndoutils

db_pass=yourPassword


6. Installer Service / Deamon

``sudo make install-init``

``sudo systemctl enable ndo2db.service``

7. Démarrer Service / Deamon 
  
``sudo systemctl start ndo2db.service``

8. Mettre à jour Nagios pour qu'il utilise NDO Broker Module

Maintenant, vous devez Indiquer à Nagios d'utiliser le module NDO broker. C'est aussi simple que d'ajouter la ligne suivante au fichier nagios.cfg 

``broker_module=/usr/local/nagios/bin/ndomod.o config_file=/usr/local/nagios/etc/ndomod.cfg``

Les commandes suivantes ajouteront cette ligne ainsi qu'une ligne supplémentaire qui explique à quoi sert le module.

``sudo sh -c 'printf "\n\n# NDOUtils Broker Module\n" >> /usr/local/nagios/etc/nagios.cfg' ``
 
`` sudo sh -c 'printf "broker_module=/usr/local/nagios/bin/ndomod.o config_file=/usr/local/nagios/etc/ndomod.cfg\n" >> /usr/local/nagios/etc/nagios.cfg' ``


9. Rédemarrer Nagios
  
``sudo systemctl restart nagios.service`` 

``sudo systemctl status nagios.service``

La dernière commande doit indiquer que nagios est bien activé.

10. Vérifier que Ndoutils est bien installer

`` echo 'select * from nagios.nagios_logentries;' | mysql -u ndoutils -p'yourPassword' ``


<br/>

### Installer et configurer Splunk DB connect

<br/>

``Splunk DB Connect`` est une extension générique de base de données SQL pour Splunk qui permet d'intégrer facilement les informations de la base de données aux requêtes et rapports Splunk.


``Prés-requis``

* Installer Jdk 8

NB: C'est uniquement pour splunk DB connect version 3 si vous avez une version différentes il faut vérifier les prés réquis sur le site officiel du splunk.

<br/>

1. Télécharger  Orale JDK 8
  
sur le site officiel de Oracle:
https://www.oracle.com/java/technologies/downloads/#java8

2. Acceder au répertoire sur le quel vous aves télécharger jdk
  
par défaut c'est dans  ``cd Downloads``

3. créer un répertoire pour l'installation de jdk
  
 `` sudo mkdir /usr/lib/jvm``

4. Accéder à ce répertoire
  
  ``  cd /usr/lib/jvm``

5. Dézipper le fichier d'instellation
  
  ``  sudo tar -xvzf ~/Downloads/jdk-8u271-linux-x64.tar.gz ``

6. Modifier l'environement du jdk

  ``  sudo gedit /etc/environment``
Si vous avez pas gedit  vous pouver le modifier avec n'importe quel editeur comme nano ou l'installer avec la ciommande suivante:  ``sudo apt-get install gedit``

7. Ajouter les bouts de code suivant au fichier d'environement:

/usr/lib/jvm/jdk1.8.0_321/bin

/usr/lib/jvm/jdk1.8.0_321/db/bin

/usr/lib/jvm/jdk1.8.0_321/jre/bin

<br/>
J2SDKDIR="/usr/lib/jvm/jdk1.8.0_321"

J2REDIR="/usr/lib/jvm/jdk1.8.0_321/jre"

JAVA_HOME="/usr/lib/jvm/jdk1.8.0_321"

DERBY_HOME="/usr/lib/jvm/jdk1.8.0_321/db"

<br/>

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"

<br/>
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/jvm/jdk1.8.0_271/bin:/usr/lib/jvm/jdk1.8.0_271/db/bin:/usr/lib/jvm/jdk1.8.0_271/jre/bin"

<br/>
J2SDKDIR="/usr/lib/jvm/jdk1.8.0_271"

J2REDIR="/usr/lib/jvm/jdk1.8.0_271/jre"

JAVA_HOME="/usr/lib/jvm/jdk1.8.0_271"

DERBY_HOME="/usr/lib/jvm/jdk1.8.0_271/db"  

Enregistrer et fermer le fichir


8. Exécuter les commandes suivantes dans votre terminal 


`` sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_271/bin/java" 0 ``

``sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk1.8.0_271/bin/javac" 0 ``

`` sudo update-alternatives --set java /usr/lib/jvm/jdk1.8.0_271/bin/java ``

``sudo update-alternatives --set javac /usr/lib/jvm/jdk1.8.0_271/bin/javac ``

9.  Verifier les setups

``update-alternatives --list java``

``update-alternatives --list javac``

10. vérifier la verison de java

``java -version``

<br/>

 ``Installer Splunk DB connect ``

1. Accéder à  ``Apps manager`` à partir de l'interface graphique de Splunk chercher `Splunk DB connect`` et cliquer sur installer
2. Rédemarrer Splunk
  

<br/>

 `` Configurer Splunk DB connect``
   
1. Ajouter le chemin d'instellation de Java à splunk

   * Ouvrir Splunk DB connect
   * Accéder à Configuration --> Settings --> General
   * Utiliser la commande suivante pour determiner le chemin d'installation de  java: ``readline -f $(whereis java)``
   * Coller le chemin d'instellation dans ``JRE Instellation Path(JAVA_HOME" ``
   * Cliquer sur save 

``NB:`` si vous aurez une erreur comme quoi le procedure à faillit, il faut rédemarrer splunk avec la commande suivante: ``sudo systemctl restart splunkd.service`` et réesayer et ça doit marcher.                                 



 2. Ajoutez un fichier mysql connector .jar

     *  télécharger  mysql connector java version 8
     *  Dézipper le dossier et vous trouverez mysql-connector-java-8.0.28.jar  de-dans
     * Copiez le fichier jar dans le dossier $SPLUNK_HOME/etc/apps/splunk_app_db_connect/drivers/, avec la commande ci dessous: ``sudo cp mysql-connector-java.jar /opt/splunk/etc/apps/splunk_app_db_connect/drivers``
     *  Rédemarer splunk
  
Consulter l'interface graphique de Splunk, splunk DB connect --> Configuration --> Settings --> Drivers

vous devez voir un symbole correct devant MySQL Driver.

3. Ajouter un fichier ojdbc.jar
  
    * Télécharger le fichier ojdbc.jar,  vous pouver le télécharger sur ``mvnRepository``
    * Placez le fichier dans $SPLUNK_HOME/etc/apps/splunk_app_db_connect/drivers/ 
    * Rédemarrer splunk


4. Créer une identité

   * Accéder à Splunk DB connect --> Configuration --> Databases --> Identities --> New identity
   * Remplissez les champs démandées en utilisant le nom d'utilisateur et le mot de passe que vous utilisez lorsque vous vous connectez à votre base de données MySQL NDOUtils.

5. Créer une connection
  
    * Accéder à Splunk DB connect --> Configuration --> Databases --> Connections --> New connection
    * Remplisez les champs en utilisant l'indentité que vous venez de créer.
    * Pour JDBC URL settings, le Host:localhost et le port par defaut c'est 3306.
    * Utilisez la base de données que vous avez créer lors de la configuration de Ndoutils comme default database.
    * Les autres options vous pouvez les laisser par defaut.

Si vous aurez l'erreur ``database connection invalid``, il faut s'assurer que la version de mysql connector est adaptée à votre Splunk DB connect version. Pour la version 3 de Splunk DB, mysql connector doit être supperieure à la version 5.

Pour contourner un begue connu de Nagios concernant le traitement des valeurs vides pour les timestamps, ajoutez la ligne suivante, exactement telle qu'elle est écrite ici, dans le fichier $SPLUNK_HOME/etc/apps/splunk_app_db_connect/local/db_connection.conf

jdbcUrlFormat = jdbc:mysql://<host>:<port>/<database>?zeroDateTimeBehavior=convertToNull

1. Créer des données d'entrées à Splunk
    * Accéder à Splunk DB connect --> DataLab --> Inputs --> New Inputs