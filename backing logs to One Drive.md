#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# Backing Logs to One drive

Dans cette documentation nous allons créer un sauvegarde pour les journeaux sur One drive et nous allons automatiser cette tâche qu'on peut la diviser en deux parties.

## Partie 1: Automatiser le stockage de données à partir du splunk sur la machine locale 

Splunk à un CLI dans le dossier /opt/splunk/bin à partir de la quelle on peut lancer un enssemble des commandes. Le script suivant, que nous avons crier vous permet de sauvegarder les journeaux sur la machine locale dans un fichier dont le nom est le date du jour en question pour différencier entre les journeaux et c'est plus facile pour la recherche et le traitement.

```bash
#!/bin/bash

export TZ=Africa/Nouakchott
filename=$(date +"%m_%d_%Y")
cd /opt/splunk/bin && ./splunk user SplunkUser -password SplunkPWD search "index=IndexName - earliest=07/06/2022:12:32:00 latest=07/06/2022:12:34:37" -output csv > WhereYouWantToSaveTheFile/$filename.csv

```

## Partie 2: Automatiser le stockage de données à partir de la machine locale sur One Drive

Pour faire ceci, nous allons utiliser rclone qui est une commande line programmer pour gérer les fichiers sur un stockage cloud. 



1. Méttre à jour le systeme 

* ``sudo apt update``

* ``sudo apt upgrade``

2. Télécharger rclone 

* Soit à partir du paquet manager avec la commande suivante:
 ``sudo apt install rclone``
* Soit en téléchargeant la dernière  version avec wget `` wget https://downloads.rclone.org/v1.59/rclone-v1.59-linux-amd64.deb `` à la date de la rédaction de cette documentation la dernière version de rclone est la version ``v1.59``. Puis l'installer avec la commande suivante:
* ``sudo apt install ./rclone-v1.42-linux-amd64.deb``


3. Ajouter un niveau One Drive remote à rclone

* Ouvrez un terminal et tapez la commande suivante: ``rclone config``
* Tapez ``n`` pour choisir une nouvelle remote
* Donnez un nom à votre remote example  ``onedrive`` 
* Une liste de moyens de stockage cloud va s'afficher, chercher ``Microsoft OneDrive`` et entrez le numero correspondant, pour notre version c'est le numéro 32.
* Par la suite, vous allez être demander à entrer Microsoft App client ID et Secret tapez entrer car vous n'avez pas besoin de renseinger ces informtions.
* Choisissez le type de service Miccrosoft que vous voulez ou vous pouver le laisser par defaut ``Microsoft Cloud Global``
* Laisser les configurations avancées par défaut en tapant ``n``
* Choisisez l'auto-configuration en tapant ``y``sauf si vous accéder au terminal via un remote, vous aurez besoin d'une configuration special, voir le lien suivant: ``https://askubuntu.com/questions/804421/mounting-onedrive-on-ubuntu-linux-command-line``

* Une nouvelle fenêtre va s'ouvrir à partir de votre navigateur web par défaut. Vous aller être demander à s'identifier, puis à donner accés à rclone. Cliquer sur oui, si tous vas bien vous aurez la message suivante: ``Success! All done. Please go back to rclone.``
* Revenez au terminale et choisissez le type de votre connection One Drive.
* Choisissez le drive que vous voulez utiliser si vous en aurez plusieurs comptes. Dans le cas contraire, vous n'aurez qu'une seule option, une autre question de reconfirmation va s'afficher cliquer sur ``y``.
* Un token va s'afficher et vous aurez être demander à confirmer l'ensembles d'informations. Si tous vous convient tapez ``y`` pour confirmer.
* Tapez ``q`` pour quitter rclone

4. Créer un dossier de partage entre votre fichier en locale et ceux sur le drive

 * créer un dossier de partage avec la commande suivante: `` mkdir ~/OneDrive   ``
 * Tapez la commande suivante `` rclone --vfs-cache-mode writes mount onedrive: ~/OneDrive``

 NB: Vous pouvez tester la configuration en ajoutant un fichier dans le dossier one drive et voir s'il va être ajouter sur votre drive en ligne.

 Vous n'aurez pas besoin à lancez la commande ci-dessus à chaque fois, vous pouvez l'ajouter à votre crontab. Ce qu'il nous avons fait pour automatiser cette tâche à l'aide du script bash ci-dessus.

Au début nous avons importer RCLONE comme un variable d'environnement car son chemin n'est pas reconnu. Le chemin par défaut est le suivant:`` /home/smart/.config/rclone/rclone.conf``


```bash
#!/bin/bash

export TZ=Africa/Nouakchott
# RClone Config file
RCLONE_CONFIG=/home/smart/.config/rclone/rclone.conf
export RCLONE_CONFIG

rclone --vfs-cache-mode writes mount YourRcloneRemoteName: YourOneDRiveFolder --allow-non-empty
#reclone config file location in : /home/smart/.config/rclone/rclone.conf
#The commande "rclone config file" gives you the reclon conf file actual location
```

5. Ajouter les deux scripts que vous voulez exécutés dans crontab
* Ouvrez un terminale et tapez la commande suivante: ``crontab -e``
* Ajoutez les script que vous voulez ajoutés, voir crontab, si vous n'êtes pas famillier avec crontab, faitez des recherches pour mieux comprendre son fonctionnement.
     * Example:  40 10 * * * /home/root/Desktop/rclone.sh 
     * Ce script va être exécuter chaque jour à 10:40

``NB:`` N'oublier pas de changer l'emplacement, dans la quelle va être sauvegarder le fichier de journeaux dans le premier script bash ci-dessus avec celui de votre dossier de partage ``onedrive``

# Troublshooting
Parfois crontab ne marche pas même si votre code est correcte et c'est dans la plus part de cas dû à la  différence de temps entre celui de votre système et celui du crontab.
Pour corriger ceci il faut indiquer votre region dans votre bash script en ajoutant le ligne de code suivant:  ``export TZ=Africa/Nouakchot``et égalment dans votre fichier crontab comme ceci ``CRON_TZ=Africa/Nouakchot`` .

# References
*``https://www.fosslinux.com/24391/how-to-sync-microsoft-onedrive-from-command-line-in-linux.htm``

*``https://askubuntu.com/questions/804421/mounting-onedrive-on-ubuntu-linux-command-line``