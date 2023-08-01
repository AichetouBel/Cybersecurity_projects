#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# Instellation de Cortex

* Installer Cortex:  ``sudo apt install cortex``
* Changer la configuration de Cortex pour qu'il reconnu elasticsearsh. `` sudo nano !etc!cortex!qpplicqtions.``

        * # uncomment the configuration key
        play.http.secret.key="***CHANGEME***"search {
        # Name of the index
        index = cortex
        # ElasticSearch instance 
        address.
        # For cluster, join address:port with ',': "http://ip1:9200,ip2:9200,ip3:9200"
        uri = "http://<elk_ip>:9200"
* Démarrer cortex
    * sudo systemctl start cortex
    * sudo systemctl enable cortex

Accéder à l'interface graphique de cortex 127.0.0.1:9000/, si le port 9000 est utilisé par une application, cortex va utiliser le port suivant par défaut à partir du port 9000 par exemple tester 127.0.0.1:9001/ .

Quand vous vous connectez sur le cortex pour la première fois vous avez besoin de créer un compte administrateur. Par la suite, vous devez créer une organisation et un utilisateur dedans cette organisation, en se connectant avec l'organisation par défaut ``Cortex`` vous pouvez pas faire grand-chose car certaines options sont cachées.
À la base l'organisation par défaut sert uniquement à vous identifier pour cee connecter pour la première fois.

générer un API key à partir de l'organisation que vous venez de créer. Vous allez avoir besoin de cet API key pour se connecter avec The hive. Cliquer sur l'organisation pour générer l'API key.

## Configurer les analyseurs
Les analyseurs sont les moteurs qui vont vérifier toutes les bases de données pour trouver des artefacts malveillants.

1. Pour configurer les Analyseurs, installez les paquets prérequis:

        * sudo apt-get install -y --no-install-recommends python-pip python2.7-dev python3-pip python3-dev ssdeep libfuzzy-dev libfuzzy2 libimage-exiftool-perl libmagic1 build-essential git libssl-dev
        * sudo pip install -U pip setuptools && sudo pip3 install -U pip setuptools
2. Télécharger le répertoire de Cortex-Analyzer
* cd /opt
* sudo git clone https://github.com/TheHive-Project/Cortex-Analyzers

3. Pour fonctionner correctement, chaque analyseur a besoin de certains paquets de dépendances. Installez tous les paquets requis avec le script ci-dessous:
``` sh
* for I in $(find Cortex-Analyzers -name 'requirements.txt'); do sudo -H pip2 install -r $I; done && \
for I in $(find Cortex-Analyzers -name 'requirements.txt'); do sudo -H pip3 install -r $I || true; done
```

3. Attendez un peu , que Cortex télécharge et configure les Analyseurs. Dans le fichier de configuration de Cortex, changez le chemin vers les Analyseurs.

        * $ vim /etc/cortex/application.confanalyzer {
        # analyzer location
        # url can be point to:
        # - directory where analyzers are installed
        # - json file containing the list of analyzer descriptions
        path = ["/opt/Cortex-Analyzers/analyzers/"]
        #"https://download.thehive-project.org/analyzers.json"
        #"/absolute/path/of/analyzers"
    
        [...]responder {
        # responder location (same format as analyzer.urls)
        path = ["/opt/Cortex-Analyzers/responders/"]
        #"https://download.thehive-project.org/responders.json"
        #"/absolute/path/of/responders"

4. Redémarrer la service de Cortex
    * sudo systemctl restart cortex

En allant dans le menu Organisation > Analyseurs, vous pouvez voir un grand nombre d'analyseurs installés.

NB: le champs ``Analyzers`` dans le bar menu contient uniquement les analysers que vous activez à partir de `` Organisation > Analysers`` 
Vous devez les activer et les configurer. Certains Analyseurs sont payants, vous aurez besoin d'une API pour vous connecter à ces services. Généralement, ces APIs sont activées après avoir payé le service.

Pour activer un Analyseur cliquez simplement sur ``+Enable`` et cliquez sur Save.