#####################################################################
#######                AUTHOR: AICHETOU BEL                   #######                       
#####################################################################

## Installer et Configurer OPNsense

### Définition: 

OPNsense est un logiciel de pare-feu et de routage open source basé sur FreeBSD. Il est un fork de pfSense qui a été développé par les mêmes développeurs de PfSence après leur séparation de l’entreprise.
Ce logiciel, combine les riches fonctionnalités des pare-feu commerciaux avec les avantages des solutions open-source et vérifiables. OPNsense est couramment utilisé par des PME et TPE, ainsi que par des entreprises des secteurs d’activité Services ou Tertiaire.

### Installation
* Télécharger opnsense à partir du site officiel: ``https://opnsense.org/download/ `` et choisir les caractéristiques suivantes:
    * System architechture: ``amd64``
    * image type: dvd
    * choisir un Mirror (Peut import le pays)
* Ouvrir votre virtuelle machine
* Accéder à File --> New virtual Machine et choisir les options suivantes
    * Configuration  ``Typical``
    * Installer l'image d'OPNsense que vous avez téléchargé
    * choisir le nom de votre machine virtuelle et son emplacement si vous voulez le changer, par défaut les machines virtuelles ce trouve dans le dossier Documents --> Virtuelle machine
    * La capacité minimum du disque récommandé est 40 GB (Vous pouvez allouer moins ou plus selon votre utilisation et objectif)
* Cliquer sur ``Customize Hardware``
    * Ajouter un Network Adapter Bridge: VMnet0 (en vmware workstation) ou son correspondant 
    * Ajouter un Network Adapter HostOnly: VMnet1 (en vmware workstation) ou son correspondant
    * Cliquer sur Finish

NB: Le ``Bridge`` et ``HostOnly`` sont deux modes de connexion de la virtuelle machine. Le Bridge permet de connecter une machine virtuelle directement sur le réseau physique sur lequel est branchée la carte réseau physique de l’hôte. C’est en quelque sorte un partage de carte réseau, où le système d’exploitation de votre hôte physique partage sa carte physique avec le système d’exploitation de votre ou vos machines virtuelles.
Le mode de connexion HostOnly permet uniquement d’établir une connexion entre la machine virtuelle et la machine physique. Cela par l’intermédiaire de l’adaptateur virtuel de la machine virtuelle et l’adaptateur virtuel de la machine physique qui obtiendront des adresses IP via le serveur DHCP virtuel de l’hyperviseur.

Dans notre cas le Bridge vas permettre au firewall d'avoir accès à l'internet à partir de la machine physique et le mode Host only va crée une liaison entre le firewall et notre machine client qui est connecté en mode HostOnly également.

### Configurer OPNsense

1. Cliquer sur ``Power on this virtuel machine``
2. Vous allez être demandés de s'identifier connectez-vous en mode de configuration avec les identifiants suivants:
    * Login: installer
    * Password: opnsense
* cliquer sur ``Continue with default keyMap``
* cliquer sur ``install(UFS)``, une Pop-up va apparaitre sur l'écran cliquer ``Proceed anyway``et continuer
* choisissez ``da0`` et cilquez sur ok, deux Pop-up vont apparaitre ssuccessivement sur l'écran, cliquez ``Yes`` et continuer.
* cliquer sur ``Complete install``
  
Vous allez être redirigés vers l'interface du FW connecté vous avec les identifiants suivants:
* Login: root
* Password: opnsense


### Configuration de LAN et WAN

``Configurer les interfaces``

* Tapez 1 pour accéder à l'option ``Assign Interfaces``, qui vous permettent d'assigner des interfaces du Firewall à LAN et à WAN.  
*  Configurer les options suivantes comme suit:
   * Tapez N pour les options LAGGs et VLAN (sauf si vous  voulez configurer VLAN) 
   * Entrer em0 pour l'interface WAN et em1 pour l'interface LAN puis cliquer sur entrer
   * ``Do you want toproceed``: Tapez ``y``
  
``Configurer les adresses IP``

Par défaut, vous devez avoir une adresse IP WAN appartient à la plage de votre réseau internet. Si ce n'est pas le cas vous devez le configurer statiquement :

* Tapez 2 pour accéder à l'option ``Set interfaces IP address``, qui vous permet de configurer les adresses IP de votre LAN et WAN. 
* Choisissez la configuration de WAN (tapez 2) et configurer les options suivantes:
   *  Configurer IPv4 WAN adresse à partir du DHCP: ``N``
   *  Entrer l'adresse IP de WAN et son masque
   *  Entrer le gateway (Passerelle pardeafut) de votre connexion internet
   *  Les autres options laissez-les par défaut
  
De la même manière, configurés l'adresse Ip LAN, cette addresse doit appartenir à la plage réseau de HostOnly. Vous pouvez voir cette plage via vmware--> Edit --> Virtual Network editor --> VMnet1 (ou sa correspondante).

``NB:`` La passerelle(gateway) est importante uniquement pour l'interface WAN. Pour savoir votre gateway tapez ipconfig(windows) ou ifconfig(ubuntu).

Maintenant,vous devez être capable d'accéder à l'interface graphique du Firewall à partir de votre machine client avec l'adresse Ip de votre interface LAN du Firewall.Pour notre cas, notre machine client une machine virtuelle ubuntu avec une connexion HostOnly uniquement (Pas de NAT). Cette congiguration de la machine client va nous permettre de contrôler son flux d'internet à partir du Firewall.

Si vous faciez un problème d'accès à l'interface graphique du Fw, vérifier que l'adresse ip de votre machine client appartient au même réseau que l'adresse de votre interfce LAN du FW.
Si ce n'est pas le cas, vous pouver le configurer statiquement avec la commandes suivantes:
* ``ifconfig InterfaceName yourIpAdress netmask yourMask``
* ``sudo service network-manager restart``




## Tester OPNsense (Bloquer les réseaux sociaux)

Tout d'abord, vous devez activer l'internet sur votre machine client.

### Activer l'internet sur la machine client à partir du FireWall

Dans cette documentation nous allons voir comment configurer le firewall pour que l'internet sur la machine client passe par le Firewall.
Pour notre cas nous avons OPNsense Firewall et une machine ubuntu 18.04 comme machine client.
1. Configurer DHCP 
  * Accéder à l'interface graphique du Firewall -->services --> DHCPv4 --> LAN
  * Configurer les Paramètres suivants
     * Permettre le serveur DHCP  sur l'interface LAN (option à cocher)
     * Choisir la plage pour les adresses Ip qui vont être attribuées par le DHCP, assurez-vous que la plage choisit appartient au même réseau que l'adresse LAN du Firewall. 
     * Configurer les serveurs DNS  avec les adresses IP suivantes: 8.8.8.8 et 8.8.4.4
     * Configurer le gateway(Passerelle), mettre l'adresse LAN du firewall comme la passerelle par défaut
     * Cliquer sur "save"
  * Ouvrir  le terminal et tapez les commandes suivantes: ``sudo dhclient -r``  puis  `` sudo dhclient`` 
  * Vérifier que la machine client à bien une adresse Ip qui appartient à la plage des adresses IP que vous avez définies dans DHCPv4 avec la commande suivante: ``ifconfig``

2. Configurer LAN
   * Accéder à Firewall--> Rules --> LAN --> Add pour ajouter une nouvelle règle
   * Configurer la règle comme suit:
      * Action: pass
      * Interface: LAN
      * TCP/UDP version: Ipv4
      * Protocol: Any
      * Source: Any 
      * Destination: Any
      * Les autres options laissez-les par défaut  
      * Cliquer sur "Save"
      * Cliquer sur "Apply changes"
   
3. Configurer WAN 
   * Accéder à Firewall--> Rules --> WAN --> Add pour ajouter une nouvelle règle
   * Configurer la règle comme suit:
      * Action: pass
      * Interface: WAN
      * TCP/UDP version: Ipv4
      * Protocol: Any
      * Source: Any 
      * Destination: Any
      * Les autres options laissez-les par défaut  
      * Cliquer sur "Save"
      * Cliquer sur "Apply changes"
Pinger l'adresse WAN du firewall à partir de votre machine client. Si le ping passe, ça veut dire que la configuration est bonne. Sinon, vérifier votre configuration.

4. Configurer NAT
   * Accéder à Firewall--> NAT --> PortForward --> ADD
   * Configurer la règle comme suit:
      * Action: pass
      * Interface: WAN
      * TCP/UDP version: Ipv4
      * Protocol: TCP
      * Source: Any 
      * Destination port Range: From  ``HTTP `` to ``HTTP``
      * Redirect target port: HTTP
      * Les autres options laissez les par défaut  
      * Cliquer sur "Save"
      * Cliquer sur "Apply changes"
Pour tester les configurations sur notre Firewall nous allons bloquer l'accés aux réseaux sociaux à partir de notre Machine client. Pour réaliser ceci nous avons besoin de configurer un web proxy.

### Généré un certificat d'autorité CA 

* Accéder à l'interface graphique du Firewall --> System --> Trust --> Authorities et cliquer sur ``Ass or import CA`` et configurer-le comme suit:
   * Method : ``create an internal Certificate Authority ``
   * Country code: choisissez votre pays de résidence
   * choisissez votre ville et email, l'organisation est facultative
   * les autres configurations laissez-les par défaut
   * Cliquer sur  ``save`` pour l'enregistrer
  
  Vous devez voir votre certificat créer, cliquer sur l'icon exporter à votre droite pour l'enregistrer sur votre machine. Par défaut, le CA va être enregistré dans le dossier Documents

  Maintenant vous devez ajouter le certificat à votre serveur pour notre cas lunix ubuntu(si vous utilisez un serveur windows chercher la méthode correspondante):
   * Déplacer le certificat dans le dossier ``/usr/local/share/ca-certificates`` avec la commande ``cp $yourCALocation /usr/local/share/ca-certificates`` 
  
  

### Configuration de web proxy:

``NB:`` aprés chaque modification dans la configuration il faut cliquer sur ``Apply`` sinon, ils ne seront pas enregistrée.

* Accéder à l'interface graphique du Firewall --> Service --> Web proxy --> Administration 
   *  Accéder à General proxy settings et activé le proxy, en cochant la case `` Enable proxy``
   *  Accéder à ``Local cache settings`` et activé le cache en locale, en cochant la case `` Enable local cache ``
   *  Accéder à ``Forward proxy`` et activé HTTP proxy Transparent et l'inspection SSL en cochant les cases ci-dessus:
      * Enable Transparent HTTP proxy
      * Enable SSL inspection  

A cette étape votre proxy est configuré mais il peut être contourné par l'utilisation de HTTP et HTTPs, donc il faut ajouter des règles qui bloc HTTP et HTTPs traffic.
* Accèder à Firewall --> Rules --> LAN, cliquer sur le symbole + pour ajouter une nouvelle règle et le configurer comme suit:
   *  Action: Block
   *  Interface: LAN
   *  TCP/UDP version: IPv4
   *  Protocol TCP/UDP
   *  Source: any
   *  Destination:any
   *  Destination port range: from ``HTTP`` to ``HTTP``
   *  Les autres options laissez-les par défaut
   *  Cliquer sur ``save``
  
* Cloner la règle que vous venez de créer et changer HTTP par HTTPS
* Déplacer les deux régles que vous venez de créer au début des règles
* Cliquer sur ``Apply changes``
  
``NB:`` Le firewall lit les règles une par une, donc les premières règles seront les premières à appliquer si le trafic accorde la description de cette règle.

Par la suite, vous devez ajouter le certificat que vous avez créé par avant à votre proxy:
* Accéder à Web proxy --> Forward proxy --> General Forward Settings, dans le champ ``CA to use`` sélectionner le certificat
* A côté de ``Enable Transparent HTTP proxy`` vous allez voir un petit icon rouge avec la lettre i, cliquer là-dessus où vous devez voir une description,cliquer sur cette écriture rouge pour générer automatiquement les règles à configurer. Faite la même chose avec ``Enable SSL inspection``et n'oubliez pas d'appliquer les changements que vous avez éffectués. 

Une dernière étape c'est d'ajouter le certificat aux certificats reconnu par votre navigateur. Pour notre cas,  nous utilisons  Mozilla Firefox comme navigateur.

* Ouvrir le navigateur et accéder à settings --> Privacy & Security 
* Balayer en bas pour trouver Certificates --> View Certificates 
* Cliquer sur  Authorities --> Import, choisisez votre certificat
* Cliquer ``OK``
  
### Ajouter une blacklist

Le filtrage web par catégorie dans OPNsense est effectué en utilisant le proxy intégré et l'une des listes noires disponibles gratuitement ou commerciales. Vous pouvez trouver plus d'informations sur le site d'OPNsense  ``https://docs.opnsense.org/manual/how-tos/proxywebfilter.html``. Pour cette démo, nous avons utilisé UT1 catégorie dont le lien du téléchargement est le suivqnt: ``ftp://ftp.ut-capitole.fr/pub/reseau/cache/squidguard_contrib/blacklists.tar.gz ``. Jusqu'a la rédaction de cette readme le lien du téléchargement est le lien ci-dessus, il faut vérifier sur le site officiel.

* Accéder à l'interface graphique du Firewall --> Service --> Web proxy --> Remote Access Control List, cliquer sur l'icon + pour ajouter une balacklist
* Dans l'URL metter le lien du téléchargement de la catégorie UT1 et cliquer ``save`` 

Toujours sur la même page cliquait sur ``DownloadsACLs``. Cette opération peut durer quelques minutes selon la taille de la liste que vous télécharger et la puissance de votre connexion internet bein sûr! ;) 
Une fois que la liste est téléchargée, cliquer sur modifier et vous pouvez sélectionner les catégories à bloquer de votre liste. Pour notre cas c'est ``Socialmedia``

N'oubliez pas de cliquer sur ``DownloadsACLs&Apply`` à chaque fois que vous faites une modification sur la liste.

Vous pouvez tester d'accéder au site des réseaux sociaux comme Facebook,instagram ou twitter et vous devez recevoir un message d'erreur.