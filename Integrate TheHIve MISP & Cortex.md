#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

# Intégrer TheHive, MISP et Cortex 
Maintenant, nous allons configurer Cortex et MISP pour qu'ils puissent se communiquer avec TheHive. 
## Configurer la communication entre Cortex et TheHive

Copiez et collez la clé(API key)créée dans le guide Cortex dans le fichier de configuration de TheHive.
* ``sudo nano /etc/thehive/application.conf``

        * play.modules.enabled += org.thp.thehive.connector.cortex.CortexModule
        cortex {
        servers: [
        {
           name: "local"        # Cortex name
           url: "http://localhost:9001" # URL of Cortex instance
           auth {
           type: "bearer"
           key: "<cortex_key>"  # Cortex API key
           }
           wsConfig {}          # HTTP client configuration (SSL and proxy)
           }
        ]
        }
* Redémarrer TheHive: ``sudo systemctl restart thehive``

## Configurer la communication entre TheHOIve et MISP

Éditer le fichier de configuration TheHive /etc/thehive/application.conf et décommentez les lignes ci-dessous.

Insérer le ``MISP_URL``(localhost sauf si vous l'avez changé) et le ``MISP_KEY`` que nous avons créé dans le déploiement du MISP.
    * play.modules.enabled += org.thp.thehive.connector.misp.MispModule

    misp {
    interval: 1 hour
    servers: [
    {
       name = "local"            # MISP name
       url = "<MISP_URL>"        # URL or MISP
       auth {
       type = key
       key = "<MISP_KEY>"        # MISP API key
    }
     wsConfig {}                 # HTTP client configuration (SSL and proxy)
        }
      ]
    }

* Rédemarrer TheHive: ``sudo systemctl restart thehive``

Vous pouvez vérifier si tout fonctionne bien en cliquant sur votre utilisateur (en haut à droite) et en cliquant sur À propos(``About``).

Si vous voyez une ERREUR dans la communication MISP, c'est parce que le certificat est attribué automatiquement. Vous pouvez acheter un certificat et le remplacer.

Vous pouvez vérifier la communication de MISP avec la commande :

$ curl --insecure -v https://https://<MISP_URL>(par défaut localhost:80)