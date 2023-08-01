#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# Envoyer les journaux d'OPNsense à splunk 

Dans cette phase nous allons envoyer tous les données collecter par OPNsense à Splunk pour centraliser les données.
Ces données collectées, vont être analysées par la suite pour détecter toute activité mallicious ou les dysfonctionnements dans notre système. 

## Configuration du Splunk 
 1. Créer un index dans splunk
 Splunk divise les données en plusieurs indexes, ceci facilite et accélère la recherches et l'analyse de données. Par défaut, splunk enregistre tous les données dans l'index main.
 * Accéder au répertoire suivant:  ``cd /opt/splunk/etc/system/local/``
 * Modifier le fichier de configuration indexes.conf: ``sudo nano indexes.conf ``. s'il n'existe pas, il faut le créer et modifie la propriété du fichier à ``splunk`` et lui donné accès avec les commandes suivantes:
     * ``sudo chown splunk:splunk indexes.conf ``
     * ``sudo chmod 775 indexes.conf``
 * Ajouter les lignes de code suivant un par un dans le fichier ``indexes.conf``:

    [fw]

    homePath   = $SPLUNK_DB/fwdb/db

    coldPath   = $SPLUNK_DB/fwdb/colddb

    thawedPath = $SPLUNK_DB/fwdb/thaweddb

``fw`` c'est le nom de l'index.
2. Configuerer les donnés des entrées
Dans cette étape, nous allons configurer les données d'entrée pour collecter les données de OPNsense. De ce fait, nous allons créer une nouvelle application opnsense_fw_inputs
* créer un dossier opnsense_fw_inputs: `` sudo mkdir /opt/splunk/etc/apps/opnsense_fw_inputs``
* créer un répertoire local: `` sudo mkdir /opt/splunk/etc/apps/opnsense_fw_inputs/local``
* Dans le répertoire  local nous allons créer le fichier d'entrée:  
     * ``cd /opt/splunk/etc/apps/opnsense_fw_inputs/local``
     * ``sudo nano inputs.conf``
* Ajouter le bout du code suivant dans le fichier inputs.conf: 
``[udp://:514] ``
``index=fw``
``sourcetype=opnsense``
3. Rédemarer Splunk
* ``sudo systemctl restart splunkd.service``

## Configuration d'OPNsense
OPNsense à une option qui s'appelle ``remote logging`` qu'on va utiliser pour envoyer les journaux. Elle est valable  à partir de la version 22 d'OPNsense.
* Accéder à l'interface graphique du pare-feu: System --> Settings --> logging/targetS
* Ajouter une nouvelle destination:
     * Transport: UDP
     * Hostname: Ajouter l'adresse IP de la machine sur laquelle vous avez installé Splunk 
     * Port:514
     * Les autres options laissaient les par défaut. Pour ``Applications`` et ``Facilities`` si vous ne sélectionner rien, toutes les applications et les facilities vont être séléctionnés par défaut.
     * Cliquer sur enregistrer
* Cliquer sur ``Apply`` pour enregistrer les modifications.

OPNsense envoie les journaux sur le port 514 avec le protocole UDP. De ce fait, on doit laisser passer le trafic sur ce port. 
* Accéder à Firewall --> NAT --> Port Forward et et ajouter une nouvelle régle.
* Interface: LAN
* TCP/IP version:  IPv4
* Protocol: UDP
* Source: LAN net 
* Source port range: other, from ``514`` to ``514``
* Destination: LAN net
* Destination port range: other, from ``514`` to ``514``
* Redirect target IP: ``Single host or Network` Ajouter l'adresse LAN du Firewall.
* Redirect target port: HTTP
* NAT Reflection: enable 
* Filter rule association: Rule
Cliquer sur ``save``

## Visualisation des données
Splunk visualise les données sous leur forme brute. Pour la visualisation sous forme des tableaux de bord, des configurations et des filtrages de données sont requises.

Maintenant nous allons vérifier que splunk reçoit bien les données.

* Accéder à l'interface graphique de Splunk --> Searsh&Reporting 
* Dans le bar de recherche entrer le filtre suivant ``iundex=fw``
Vous devez être capable de visualiser les données envoyées par OPNsense sur le port 514.

## Troublshooting

* Vérifiez que le Firewall d'ubuntu ou de votre system d'exploitation est désactivé. Pour ubuntu vous pouvez le vérifier avec la commande ``sudo ufw status``.
S'il est activé vous pouvez le désactiver avec la commande ```sudo ufw disable ``
* Rédemarez splunk à partir du répertoire ``bin`` 
     * ``cd /opt/splunk/bin``
     * ``sudo ./splunk restart``
* vérifiez que le FW envoie bien les données sur le port 514 et que ce n'est pas lui l'origine de la faille: ``sudo nc -lvu 514``. Après quelques instants, vous devez voir les données sur le terminal. Si ce n'est pas le cas, vérifier votre configuration du firewall.
* Choisissez l'option ``All time`` ou ``Real time`` pour le type de données visualiser par la recherche sur splunk. Par défaut, cette option est mise à ``Last 24 hour``



