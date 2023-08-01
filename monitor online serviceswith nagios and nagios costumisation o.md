#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# Surveillez des services web avec nagios
Dans cette partie nous allons voir comment configurer nagios pour surveiller des services en ligne. Le but est de vérifier l'accessibilité de ces services avec la commande check_http. Ce choix de check_http au lieu de check_ping est que la majorité des sites d'hébergement bloque le protocole ICMP et par conséquent le ping ne va pas retourner de résultat.

Tout d'abord vous allez avoir besoin du lien (URL) vers votre service: VOTREURL.
1. créer un fichier de configuration pour le service web
1. ``sudo nano /usr/local/nagios/etc/servers``
si vous n'avez pas un dossier ``servers`` vous pouvez le créer et lui donner les permissions nécessaires avec les commandes suivantes:
  
        cd /usr/local/nagios/etc
        mkdir servers
        sudo chmod 775 servers
        sudo chown nagios:nagios servers
* Décommanté  le ligne de code suivant ou en l'ajoutant s'il n'existe pas `` cfg_dir=/usr/local/nagios/etc/servers`` dan sle fichier ``sudo nano /usr/local/nagios/etc/nagios.cfg``

2. ``sudo nano webSErvice.cfg``
3. Ajouter les lignes de code suivantes dans le fichier webSErvice.cfg

        define host{
        use                     linux-server
        host_name               demande agréments
        check_command           check_http_on
        }
4. Créer un fichier pour les commandes ``sudo nano costum_cmd.cfg`` et dans ce fichier définissez la commande ``check_chttp_on`` en ajoutant les lignes de code suivantes:

        define command {
            command_name    check_http_on14
            command_line    /usr/local/nagios/libexec/check_http -H VOTREURL -S --sni
        }
changer VOTREURL par l'url vers votre web service. 

L'option -S est utlisé pour les sites qui utilise https et l'option --sni c'est pour indiquer que vous utiliser un url sans indiquer une adresse IP ou un nom de domaine.

NB: vous pouver tester la commande ``/usr/local/nagios/libexec/check_http -H VOTREURL -S --sni``à partir du terminal.

Si vous avez plusieurs services web à surveiller il faut créer un fichier VOTRESERVICE.cfg pour chaque service contrairement aux commandes, vous pouvez les regroupez tous dans le même fichier.

NB: n'oubliez pas de changer le nom de la commande ici ``check_http_on`` car elle include le url de votre service web dans sa définition donc vous ne pouvez pas l'utiliser deux fois. Donc, pour chaque site web que vous voulez surveillez, vous devez créer une commande correspondante dans le fichier costum_cmd.cfg. Ceci peut être optimisé mais ce n'est pas le sujet de notre documentation. 
 
5. Rédemarrer Nagios: ``sudo systemctl restart nagios.service`` 

# customiser Nagios

## Mettre nagios accessible publiquement via un Nom de Domaine (DN)

Par défaut nagios fait l'installation et la configuration nécessaire pour être liée au serveur apache, vous le trouvez dans le fichier ``/etc/apache2/sites-enabled/nagios.conf``. De ce fait, pas de prés configuration nécessaire.
Tout d'abord vous devez avoir un nom de domaine valide et lié à votre addresse ip.
1. ``sudo nano /etc/apache2/sites-enabled/nagios.conf`` 
2. Au début du fichier de configuration ajouter les lignes suivantes:

       <VirtualHost *:80> 
       ServerName status.example.com --> changer ceci par votre nom de domaine

    et ajouter la balise suivante toute en bas du fichier:  
    
       </VirtualHost> 
NB: si vous aurez l'erreur: ``apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message`` 

* Ouvrez le fichier ``sudo nano /etc/apache2/apache2.conf``
* Ajouter la ligne de code suivante ``ServerName localhost``

3. Ajouter la ligne suivante: ``ServerName VotreNomDeDOMAINE``
4. lancer la commande ``sudo apache2ctl configtest`` pour vérifier que la configuration d'apache2 est la bonne, la sortie doit être ``Syntax OK``.
5. Redemarrer apache2: ``sudo systemctl restart apache2.service``



## Changer l'URL chemin(path) de nagios
par défaut nagios est accessible via l'adresse suivant ``VOTREIPADDRESSE/nagios`` mais dans la majorité des cas il est plus pratique de le faire accessible directement à partir de VOTREIPADDRESSE sans /nagios.

Pour faire ceci il faut procéder comme suit:
1. changer le chemin dans le fichier de configuration cgi.cfg

    * `` sudo nano /usr/local/nagios/etc/cgi.cfg`` puis changé la ligne de code ``url_html_path=/nagios`` par ``url_html_path=/``

2.  Modifier le fichier nagios.conf:
    * ``sudo nano /etc/apache2/sites-enabled/nagios.conf``
    * Changer la ligne de code suivante:  ``ScriptAlias /nagios/cgi-bin "/usr/local/nagios/sbin"`` par `` ScriptAlias /cgi-bin "/usr/local/nagios/sbin" ``

    * Commenter la ligne:  ``Alias /nagios "/usr/local/nagios/share"`` et puis ajouter la ligne de code toute en bas de la ligne précédente ``DocumentRoot /usr/local/nagios/share``

    * Modifier le fichier ``/usr/local/nagios/share/config.inc.php`` en changeant  `` $cfg['cgi_base_url']='/nagios/cgi-bin'; `` par `` $cfg['cgi_base_url']='/cgi-bin'; ``

    * Rédemarrer Apache and Nagios: ``sudo systemctl restart apache2.service `` et puis ``sudo systemctl restart nagios.service``

    Maintenant vous devez être capable d'accéder à nagios en tapant juste votre adresse ip.

## Changer la page par défaut de nagios
Par défaut, nagios pointe vers une page de publisité vers les différents produits de nagios sur le marché. Dans cette partie o,n va voir comment on peut changer ça. Les configurations concernant l'url de base sont dans le fichier ``index.php``.
Pour savoir l'emplacement du fichier index.php exécuter la commande: ``locate index.php | grep nagios``

1. sudo nano /usr/local/nagios/share/index.php
2. `` changer $url = 'main.php'; `` par `` $url = 'cgi-bin/status.cgi?hostgroup=all&style=overview'; `` ceci va vous permettre d'avoir la page de ``hosts`` comme votre home page dans nagios.
3. Redémarrer nagios ``sudo systemctl restart nagios.service``

Si vous voulez avoir une autre page comme la deafult page de nagios, ci-dessous les paramètres d'URL pour les pages communes du menu Nagios:

    Tactical Overview 	        cgi-bin/tac.cgi
    Map 	                    map.php?host=all
    Hosts 	                    cgi-bin/status.cgi?hostgroup=all&style=hostdetail
    Services 	                cgi-bin/status.cgi?host=all
    Host Groups      	        cgi-bin/status.cgi?hostgroup=all&style=overview
    Host Groups – Summary 	    cgi-bin/status.cgi?hostgroup=all&style=summary
    Host Groups – Grid 	        cgi-bin/status.cgi?hostgroup=all&style=grid
    Service Groups 	            cgi-bin/status.cgi?servicegroup=all&style=overview
    Service Groups – Summary 	cgi-bin/status.cgi?servicegroup=all&style=summary
    Service Groups – Grid 	    cgi-bin/status.cgi?servicegroup=all&style=overview

## Ajouter SSL certification à apache 
L'ajout d'un certificat ssl va permettre à notre nagios domaine name d'être accessible uniquement via une connexion https. Ceci est extrémement important pour la sécurité, car le protocole https sécurise les communications afin que les parties malveillantes ne puissent pas observer les données envoyées. Par conséquent, les noms d'utilisateur et les mots de passe ne peuvent pas être volés en transit lorsque l'utilisateur les saisit dans un formulaire.
Pour faire ceci nous allons utiliser  Certbot
1. Installer Certbot: ``sudo apt install certbot python3-certbot-apache``, python3-certbot-apache est un plugin qui est utilisé pour intégrer certbot et apache.
2. accéder à votre fichier de configuration ``sudo nano /etc/apache2/sites-available/your_domain.conf`` pour notre cas ``sudo nano /etc/apache2/sites-available/nagios.conf``
Vérifier l'existence de la ligne suivante si non vous devez l'ajouter: 
`` ServerName votre_nom_de_domaine ``
3. Vérifier la configuration de votre fichier apache ``sudo apache2ctl configtest`` .

Si vous aurez l'erreur: ``apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message`` 
    * Ouvrez le fichier ``sudo nano /etc/apache2/apache2.conf``
    * Ajouter la ligne de code suivante ``ServerName localhost``

4. Rédemarer apache ``sudo systemctl reload apache2``
5. Permettre https à travers du pare-feu
    * ``sudo ufw status ``
    * ``sudo ufw allow 'Apache Full' ``
    * ``sudo ufw delete allow 'Apache' ``
6. Obtenir un certificat SSL
    * ``sudo certbot --apache``
    * Vous aurez une sortie sur votre terminale pour renseigner votre address e-mail. Choisissez un address mail valide, car cet e-mail sera utilisé pour les notifications de renouvellement et les avis de sécurité.
    * Vous serez ensuite invité à confirmer si vous acceptez les conditions de service de ``Let's Encrypt``. Vous pouvez confirmer en appuyant sur A et ensuite sur ENTER.
    * Ensuite, il vous sera demandé si vous souhaitez partager votre adresse électronique avec l'``Electronic Frontier Foundation`` pour recevoir des nouvelles et d'autres informations. Si vous ne souhaitez pas vous abonner à leur contenu, tapez N. Sinon, tapez Y. Ensuite, appuyez sur ENTER.
    * L'étape suivante vous demandera d'indiquer à Certbot les domaines pour lesquels vous souhaitez activer HTTPS. Choisissez le numéro correspondant à votre domaine name de nagios.
    La sortie est similaire à celle-ci:

            Congratulations! You have successfully enabled https://your_domain and
            https://www.your_domain

            You should test your configuration at:
            https://your_domain
            https://www.your_domain

7.  Vérification de l'auto-renouvellement de Certbot
    * ``sudo systemctl status certbot.timer``, vous aurez une sortie similaire à celle-ci.

            certbot.timer - Run certbot twice daily
            Loaded: loaded (/lib/systemd/system/certbot.timer; enabled; vendor preset: enabled)
            Active: active (waiting) since Wed 2022-10-12 11:15:37 UTC; 4h 19min ago
            Trigger: Wed 2022-10-12 23:24:31 UTC; 7h left
            Triggers: ● certbot.service
            Oct 12 11:15:37 aiinfra1 systemd[1]: Started Run certbot twice daily.
8. Pour tester le processus de renouvellement, vous pouvez effectuer un essai à sec avec certbot : ``sudo certbot renew --dry-run``, si vous ne voyez aucune erreur, vous êtes prêt.


## Changer l'apparence de l'interface graphique de Nagios
Dans cette partie nous allons voir comment changer l'apparence de l'interface web de Nagios. Pour faire cela, nous allons télécharger la template vautour qui est un template proposé par la communauté de Nagios sur Nagios Exchange. Le site web Nagios Exchange propose une grande sélection de plug-ins pour différents scénarios de surveillance et de gestion pour les produits de Nagios.

1. Télécharger le template de Vautour: ``wget https://dl.dropboxusercontent.com/s/qf1jateayqg0n35/vautour_style.zip`` 
Vous pouvez trouver plus des détails sur la template d'ici: ``https://exchange.nagios.org/directory/Addons/Frontends-%28GUIs-and-CLIs%29/Web-Interfaces/Themes-and-Skins/Vautour-Style/details``
2. Faire une copie de votre répertoire de nagios actuel, pour en fait recoure au cas où. C'est d'ailleur une trés bonne habitude de faire des backups.
* ``cd /usr/local``
* ``tar -cvf nagios_backup.tar nagios``

3. Accéder à l'endroit où vous avez téléchargé le fichier Vautour et exécuter la commande suivante: ``unzip vautour_style.zip -d /usr/local/nagios/share``, puis choissez l'option ``A`` et cliquer sur Entré.
C'est dans le dossier ``/usr/local/nagios/share`` ce trouve tous les composants concernant le design de l'interface graphique de nagios. 

4. Redémarrer Nagios core: ``sudo systemctl restart nagios.service``

``NB:`` Si vous en aurez besoin de revenir à votre ancienne version de nagios template, il suffit de supprimer le dossier nagios et décompresser l'archive puis redémarrer nagios:
* ``sudo rm -r nagios``
* ``sudo tar xvf nagios_backup``
* ``sudo systemctl restart nagios.service``


Après vous pouvez customiser les couleurs et les images à votre besoin. Il suffit juste d'ouvrir l'interface graphique, faire une clique droit sur ce que vous voulez changer et sélectionner ``inspect``. Vous tous les détaillez du code HTML et le style CSS et à partir de là vous pouvez savoir le fichier où ces informations sont enregistrées et les customiser selon vos besoins.

``NB:`` Si vous avez changé la page par défaut de nagios comme documenter ci-dessus, vous aures besoin de changer certaines choses pour qu'il fonctionne correctement. Normalement si vous voulez accéder à la page hosts par exemple vous aurez l'erreur ``NOT Found``. Ceci est dû au fait que vous avez changé le path vers ces pages.
Pour corriger ceci, tapez la commande suivante: ``sudo grep -rnw '/usr/local/nagios/share' -e '/nagios/cgi-bin' ``.

La sortie doit ressembler à celle-ci:

    * /usr/local/nagios/share/js/trends.js:37:			cgiurl: '/nagios/cgi-bin/', 
    * /usr/local/nagios/share/js/map.js:100:			cgiurl: '/nagios/cgi-bin/',
    * /usr/local/nagios/share/js/histogram.js:27:		cgiurl: '/nagios/cgi-bin/',
``/usr/local/nagios/share/js/trends.js``: représente le fichier 

``cgiurl: '/nagios/cgi-bin/' ``: représente la ligne dans le fichier qui contient "/nagios/cgi-bin/"

cette commande va vous permettre d'afficher tous les fichiers où le lien racine de nagios est `` /nagios/cgi-bin ``. Par la suite vous devez changer tous ces fichiers un par un, en changeant ``/nagios/cgi-bin' `` par ``/cgi-bin' ``.

Une astuce qui peut vous faciliter le travail, est de chercher la ligne que vous devez changer directement. si vous utilisez ``nano``, c'est ``ctr+w``, puis ``ctr+shift+v`` pour coller la ligne. Avec ``gedit`` c'est ``ctr+F`` pour la recherche.