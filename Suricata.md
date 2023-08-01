#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

## Suricata

## Définition du logiciel
Suricata c'est un moteur de détection et de prévention des intrusion créee en 2009 par OSFI, dans une tentive de repondre aux demandes de marché avec l'émergence de moderne infrastructure. L'IDS ou Intrusion detection system, ce sont des logiciels qui sont capables de détecter les intrusions dans un system donné comme les malwares les virus et d'autre. Tandis que l'IPS (Intrusion Prevention System) vont prévenir notre system dans le cas d'existence des malwares et ils nous donnent la possibilité de bloquer ou rejeter le traffic selon les règles de configuration qu'on définit.

Les fonctionnalités Principales:
* Multithreading: c'est un point fort de suricata qui lui permet de processer simultanement plusieurs règles de détection sur le traffic trés rapidements dans un temps minimal, ce qui est idéal pour le trafic très volumineux. Cette fonctionnalité on  la trouve pas dans les autres IDS & IPS les plus populaire comme Snort par exemple.

* Suricata utilise la language lua script ce qui lui permet de créer des règles qui sont très complexes pour les mettre en place ce qui lui permet de répondre parfaitement à la complexité des menaces de  nos jours.

* Il supporte la détection au niveau de la couche d'application par exemple il peut détecter le trafic ssh et http sur les ports qui ne sont pas standard.

## Instellation
Comme notre firewall OPNsense utilise Suricata comme IDS&IPS nous allons pas besoin d'installer Suricata car il est intégré dans OPNsense. Juste des configurations vont être requises.

* Accéder à l'interface graphique de OPNsense. Services --> Intrusion detection --> Administration --> Settings
     *Cochez la case ``advanced mode``
     * Cochez la case ``Enabled`` pour activer la détection des intrusions
     * Cochez la case ``IPS mode`` pour activer la prévention des intrusions
     * Cochez la case ``Promiscuous mode``
     * Cochez la case ``Enable syslog alerts``
     * Pattern matcher: ``Hyperscan``
     * Interface: LAN
     * Home network: saissisez votre plage d'adresse IP exemple: ``192.168.10.0/24``
     * Les autres options laissaient les par défaut
     * Cliquer sur ``Apply``

La détection des intrusions est maintenant activée sur notre firewall.

OPNsense contient un ensemble de plugins prêts à être téléchargé pour détecter les intrusions de plusieurs types comme le socialNetworking et autres. Pour les télécharger accéder à  Services --> Intrusion detection --> Administration --> ``Dowloads``.

## Tester suricata
Pour tester que suricata est bien activé et travail correctement nous allons essayer de télécharger un fichier de test eicar file et voir si suricata va détecter le fichier ou non.

Eicar file: est fichier de test destiné à tester le bon fonctionnement des logiciels antivirus. 

OPNsense à un plugin qui s'appelle ``OPNsense-App-detect/test`` qui à pour but de tester le fonctionnement de suricata. Nous allons utiliser ce plugin de test.
* Accéder à Services --> Intrusion detection --> Administration --> ``Dowloads``.
* balayer vers le bas pour chercher ``OPNsense-App-detect/test`` et cochez cette option.
* Cliquer sur ``Enable selected``
* Cliquer sur ``Dowloads&Update Rules``
* Créer un ``schedule`` une fenêtre va apparaitre cliquer sur ``enable`` et ``save``
* Ouvrir une terminale et taper la commande suivante: Curl http://pkg.opnsense.org/test/eicar.com.txt

``NB:`` Si vous aurez une erreur comme quoi la commande Curl n'est pas reconnue. Il faut juste l'installer avec la commande: ``sudo apt instlall curl``

* Accéder à Services --> Intrusion detection --> Administration --> ``Alert``. Une nouvelle alerte doit être créée avec la spécification du fichier(La source, la destination, le temps du téléchargement...).
