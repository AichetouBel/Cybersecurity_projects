#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# Instellation de TheHive

## prérequis:
* Ajouter les références d'apache répertoire

        * curl -fsSL https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
        * echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
* Mise à jour les packages d'instellation: ``sudo apt update``

### ElasticSearsh
1. Instellation
* Mettre à jour les packages d'installation: ``sudo apt update -y``
* Install java: ``sudo apt install default-jdk -y``

NB: la version minimum pour cette installation c'est java 11. Si vous avez java 8 ne le désinstaller pas, vous pouvez avoir plusieurs versions de java.
* Vérifier la version du java: ``java -version``
* Vérifier JAVA_HOME: ``echo $JAVA_HOME``
* Si le chemin de java home n'est pas établi ou il affiche une version différente de celle du ``java -version``, vous pouvez le changer avec la commande suivante: ``export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64``
* installer le package apt-transport-https qui va sécuriser la communication.
``sudo apt-get install apt-transport-https -y``
* Ajouter la clé GPG à votre system. 

        * ``curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -``
* Télécharger Elasticsearsh:

         * ``echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list``
* Mettre à jour apt-package: ``sudo apt update -y``
* Installer elasticsearch: ``sudo apt install elasticsearch -y``

2. Configuration 
* Accéder au fichier de configuration d'elasticsearch: ``sudo nano /etc/elasticsearch/elasticsearch.yml``
* Décommenter et changer les lignes suivantes: 
   * network.host: localhost
   * http.port:9200

* exécuter les commandes suivantes:
    * sudo systemctl daemon-reload
    * sudo systemctl restart elasticsearch
NB: si la dernière commande retour une erreur, accédez à ``cd /usr/share/elasticsearch`` et tapez la commande suivante  `` sudo ./bin/elasticsearch --version`` et si vous aurez l'erreur suivant: ``insufficient memory for the Java Runtime Environment``, redémarrer votre ordinateur et réexécuter la commande puis vérifiez que tout va bien avec la comande: ``sudo systemctl status elasticsearch.service``.

* Vérifier que le port 9200 est bien activé: ``netstat -plntu | grep "9200"``
 NB: Si 



### Cassandra 
* Installer Cassandra: ``sudo apt install cassandra``
* Configurer Cassandra: 

    * Changez le nom du cluster en entrant les commandes suivantes: ``cqlsh localhost 9042`` et puis ``UPDATE system.local SET cluster_name = 'thp' where key='local';``

    * Exister et tapez la commande suivante: ``nodetool flush``
    * Accéder au  fichier de configuration de Cassandra: ``sudo nano /etc/cassandra/cassandra.yaml``

            * cluster_name: 'thp'
            listen_address: localhost # address for nodes
            rpc_address: localhost # address for clients
            seed_provider:
                    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
            parameters:
                 \# Ex: "<ip1>,<ip2>,<ip3>"
                 - seeds: 127.0.0.1 # self for the first node
            data_file_directories:
                - '/var/lib/cassandra/data'
            commitlog_directory: '/var/lib/cassandra/commitlog'
            saved_caches_directory: '/var/lib/cassandra/saved_caches'
            hints_directory: '/var/lib/cassandra/hints'
    * Exécuter les commandes suivantes pour redémarrer et activer Cassandra.
        * sudo systemctl restart cassandra.
        * sudo systemctl enable cassandra.

## Instellation 

* Créez un dossier pour stocker les données:
        * mkdir -p /opt/thp_data/files/thehive
* Télécharger la clé et le répertoire pour TheHIive

        * curl https://raw.githubusercontent.com/TheHive-Project/TheHive/master/PGP-PUBLIC-KEY | sudo apt-key add -
        * echo 'deb https://deb.thehive-project.org release main' | sudo tee -a /etc/apt/sources.list.d/thehive-project.list

* Méttre à jour les packages: ``sudo apt-get update``
*Installer theHive: ``sudo apt install thehive4``

## Configuration 

        * nano /etc/thehive/application.conf
        db {
           provider: janusgraph
           janusgraph {
             storage {
                backend: cql
                hostname: [
                "127.0.0.1"
                 ] # seed node ip addresses

                #username: "<cassandra_username>" # login to connect to database (if    configured in Cassandra)
                #password: "<cassandra_passowrd"

        cql {
                cluster-name: thp       # cluster name
                keyspace: thehive           # name of the keyspace
                local-datacenter: datacenter1   # name of the datacenter where TheHive runs (relevant only on multi datacenter setup)
                # replication-factor: 2 # number of replica
        read-consistency-level: ONE
        write-consistency-level: ONE
                }
              }
           }
        }
* Exécuter la commande suivante: 
`` chown -R thehive:thehive /opt/thp_data/files/thehive``.

* Changer la configuration de theHive pour qu'il reconnut elasticsearsh. ``sudo nano /etc/thehive/application.conf``

        * # Elasticsearch
        search {
        ## Basic configuration
        # Index name.
        index = the_hive
        # ElasticSearch instance address.
        uri = "http://<elk_ip>:9200/"
  
        # Scroll keepalive
        keepalive = 1m
        # Size of the page for scroll
        pagesize = 50
        # Number of shards
        nbshards = 5
        # Number of replicas
        nbreplicas = 1
        # Arbitrary settings
        settings {
        # Maximum number of nested fields
        mapping.nested_fields.limit = 100
        }
  
        ## Authentication configuration
        #search.username = ""
        #search.password = ""

        ## SSL configuration
        #search.keyStore {
        #  path = "/path/to/keystore"
        #  type = "JKS" # or PKCS12
        #  password = "keystore-password"
        #}
        #search.trustStore {
        #  path = "/path/to/trustStore"
        #  type = "JKS" # or PKCS12
        #  password = "trustStore-password"
        #}
        }
* Indiquez l'emplacement où les fichiers vont être enregistrés en ajoutant les lignes de codes suivants dans le fichier de configuration de TheHive: 

````sudo nano /etc/thehive/application.conf````

        * storage {
        provider = localfs
        localfs.location = /opt/thp_data/files/thehive
        }
* Ajouter les configurations suivantes pour configurer la base de données:

``sudo nano /etc/thehive/application.conf``

        * # Datastore
        datastore {
        name = data
        # Size of stored data chunks
        chunksize = 50k
        hash {
        # Main hash algorithm /!\ Don't change this value
        main = "SHA-256"
        # Additional hash algorithms (used in attachments)
        extra = ["SHA-1", "MD5"]
        }
        attachment.password = "malware"
        }
* Démarrer TheHive: 
   * sudo systemctl start thehive
   * sudo systemctl enable thehive

Accéder à /etc/thehive : ``cd /etc/thehive`` et puis exécuter la commande suivante `` cat secret.conf`` cette clé vous allez l'utiliser par la suite pour integret cortex.
Si vous aurez rien, vérifiez votre instellation.
Accéder à l'interface graphique de TheHive http://127.0.0.1:9000/ et connecter avec les identifiants par défaut: 

* Login: admin@thehive.local
* Password: secret
