#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# ``  Splunk Installation & Configuration   ``


Splunk c'est un logiciel de surveillance et d'analyse de données très puissant basé sur la machine learning. 
Il permet de rechercher, surveiller, analyser et visualiser les données provenant des applications, des bases de données, des serveurs web et d'autres dispositifs.

Splunk Comprend 3 principaux composants:
* Splunk Forwarder: Il est utilisé pour collecter les journaux.
* Splunk Indexer: Il est utilisé pour analyser et indexer les données.
* Splunk search Head: Fournit une interface web pour la recherche, l'analyse et le reporting.

Par la suite nous allons découvrir la méthode d'installation de Splunk version 8.2.5 sur une machine Linux distribution ubuntu version 18.04.


### ``Les fonctionnalités phares du splunk``
* Analyser les fichiers ou tout un dossier
* créer des alertes de sécurité
* Visualiser les données sous formes des dashboards
* Configurer des tokens qui peuvent être utilisés pour envoyer les donnés sur HTTP et HTTPS.
* Ecouter le réseau sur un port.
* suivre l'utilisation des mémoires des processus des systèmes d'exploitation.
* Détecter le trafic TOR

D'autres application peuvent être ajouté à la platforme selon les besoins, comme splunk surveillance pour les administrateurs et d'autres.


## Instalation
1. Ouvrir un terminal linux et taper la commande suivante:


wget https://download.splunk.com/products/splunk/releases/7.1.1/linux/splunk-8.2.5-77015bc7a462-linux-2.6-amd64.deb

NB: pour avoir la derniere verion de splunk il faut le telecharger sur le site officiel de splunk: https://www.splunk.com . Dans notre cas, nous avons télécharger la versiom 8.2.5 de splunk. Pour faire cela, il faut créer un compte sur le site du Splunk.


1. Déplacer dans le dossier où vous avez téléchargé le fichier de Splunk et exécuter la commande ci-dessus pour installer Splunk.


`` sudo dpkg -i splunk-8.2.5-77015bc7a462-linux-2.6-amd64.deb ``

Si vous aurez la reponse suivante 

`` /var/lib/dpkg/info/splunk/.postins: line 58: curl command not found `` 

`` Complete``

Malgré que c'est indiqué que l'installation est complété mais le package indiqué sur le chemin ci-dessus n'est pas installé donc, il faut installé la commande Curl de linux et reinstaller Splunk avec la commande ``dpkg``ci-dessus.

Pour installer Curl Il faut exécuter la commande suivante:

``sudo apt-get install curl``

3. permettre à Splunk de toujours démarrer lorsque le serveur démarre

``  sudo /opt/splunk/bin/splunk enable boot-start ``

Cette commande va générer une sortie sur l'écran qui contient la licence du logiciel qu'il faut accepter. Après vous allez être démandé de créer un compte administrateur, dont il faut retenir l'identifiant et le mots de passe parce que vous allez les utiliser pour accéder à l'interface graphique.

4. Démarrer Splunk

`` sudo systemctl restart splunkd.service``

Si vous aurez l'erreur suivante:
`` Failed to start spunk.service:  spunk.service not found ``

Il faut allez dans le répertoire bin `` cd /opt/splunk/bin/ `` et exécutez la commande ci-dessous `` sudo ./splunk start`` ou  `` sudo ./splunk restart ``

à la fin de la réponse, vous trouverez le lien vers l'interface Splunk. 
Si vous aurez le nom de votre domaine comme ``aichetou-virtuel-machine:8000 `` vous pouvez le changer par localhost : ``localhost:8000`` et ça va marcher également. Par défaut l'interface de splunk est accessible via: `` http://127.0.0.1:8000 `` .

5. Vérifier que Splunk est bien installé:

`` sudo systemctl status splunkd.service ``

1. Accéder à l'interface graphique 


Dans votre navigateur ouvrir une fenêtre et tapez l'addresse suivant  `` http://ip-address:8000 `` L'interface graphique du splunk doit apparaitre.

Entrer votre identifiant et le mots de passe que vous avez choisis par avant et vous devez être capable d'acceder à l'interface graphique.
 

## ``Tester Splunk``

Dans cette section nous allons faire un test de surveillance des fichiers de journaux(log files).
Une fois que vous êtes connécté sur l'interface graphique, il faut cliquer sur ajouter les données `` "Add data" `` .

Trois options vous seront présentées : 
* Upload (Télécharger). 
* Monitor (surveiller).
* Forward (Transmettre).

Chaque option est indéxée par une  courte description de son objectif. 
Dans notre cas, notre tâche est de surveiller les journaux du dossier ``/var/log``, nous allons donc sélectionner l'option ``Monitor``.
Pour faire cela il faut procéder comme suit:
1. cliquer sur " ``file & directories`` "
2. naviguer vers le dossier dont vous voulez analyser
3. Dans la page suivante, Splunk affichera les données avant de les indexer. Si vous êtes satisfait de tous les paramètres, cliquez sur "Next".
4. La page suivante est celle des "Input Sittings". Cliquez sur "Review" pour avoir un aperçu de vos paramètres avant de commencer l'indexation.
5. La page de "Review" vous donnera un bref résumé des principaux paramètres que vous avez sélectionnés. Cliquez sur "Submit".
6.Les statistiques basées sur les paramètres que vous avez choisis commenceront à s'afficher.

Vous pouvez filtrer vos recherches selon plusieurs critères comme la date.

Les commandes de splunk: 
* sudo systemctl status splunkd.service
* sudo systemctl start splunkd.service
* sudo systemctl restart splunkd.service
* sudo systemctl stop splunkd.service



## ``Splunk Entreprise security(ES)``

Une fois que nous avons installé Splunk entreprise on ajoute Splunk entreprise security qui est l'une des larges applications offertes par la platforme Splunk.

Splunk Enterprise Security (ES) résout une large gamme de cas d'utilisation de l'analyse et des opérations de sécurité.

``Principales fonctionnalités``
* la surveillance continue de la sécurité
* la détection des menaces avancées et des anomalies
* L'examination et la réponse aux incidents
* La visualisation des événements sous formes des tableaux de bord dynamiques.
* L'intégration de UBA(user behavior analytics): analyseur de comportements des utilisateurs.
* La Création des alertes priorisée par gravité de l'incident déroulé.
* Avoir la visibilité à travers votre environnement hybride avec la surveillance de la sécurité multi-cloud.
* Mise à jour de façon continue des cas d'utilisations(use case)

      
      

### ``prés-réquis``

* Licence de Splunk: parceque splunk ES est une solution de sécurité premium nécessitant une licence payante
* Splunk Base: c'est un site où les utilisateurs peuvent partager des applications et des add-on avec la communauté de Splunk.

``add on`` :un composant qui joue le rôle d'un support pour les applications de splunk. IL fournit des capacités spécifiques à d'autres applications, telles que l'entrée de données et le mappage de données.

``Les étapes d'installation ``

1. Sur la page d'accueil  de l'interface graphique de la platforme il y'a un icon en haut à gauche pour l'ajout des nouvelles applications on clique là-dessus.
2. Dans le bar de recherche on cherche ``Splunk Entreprise Security`` 
3. Comme splunk entreprise secrity est une application payante elle n'est pas valable pour l'installation mais on peut l'avoir sur splunk base. pour faire cela il faut cliquer sur "view on Splunkbase".
4. Vous allez être dirigé vers la page d'accueil de splunk base. Naviguer en bas et vous allez trouver un button pour installer Splunk ES. Il suffit juste de se connecter avec votre compte de la platforme Splunk.
5. Une fois connecté, vous aurez l'option de contacter les vendeurs pour avoir votre licence payante


Toutefois, il y a une possibilté de voir les fonctionnalités qu'offre splunk ES avant de l'acheter. Il suffit de chercher "Splunk Entreprise Security Guided Product Tour".



# Troubleshooting

* Si vous aurez l'erreur suivante : ``Unable to stop splunk helpers``. Ceci implique que splunk a été arrêté de manière incorrecte et il laisse parfois derrière lui un fichier PID corrompu dans le répertoire $SPLUNK_HOME/var/run/splunk et cette erreur s'affiche lorsque vous essayez de démarrer ou redémarrer splunk. Pour corriger cette erreur suivez les étapes suivantes :
    * Assurez-vous que Splunkd et Splunkweb ne sont pas en cours d'exécution en exécutant les commandes suivantes :
        * ``ps -es | grep splunkd`` et ``ps -ef | grep splunkweb`` s'ils sont exécutés vous devez tuer le processus qui l'exécute  ``kill -9 PID ``.

    * Déplacez ensuite ``splunkd.pid`` et ``splunkweb.pid`` du répertoire $SPLUNK_HOME/var/run/splunk vers un répertoire temporaire. Par défaut ``$SPLUNK_HOME``est ``/opt/splunk``.
    * Accéder à ``/opt/splunk/bin`` puis exécuter la commande ``./splunk status``.







