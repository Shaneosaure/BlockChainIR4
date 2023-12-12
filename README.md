# BlockChainIR4
Ce projet de 4 ème année à l'ESAIP permet a pour consigne suivante:
Développer votre bloc chain dans le language de votre choix.
Votre programme doit permettre de :
* D’ajouter une transaction => Add(transaction)
* De vérifier une transaction => Check(id_transaction)
* D’afficher les 10 derniers transactions => Show()
* D’altérer un bloc => Tamper (id_transaction)
* De valider la bloc chain
Toutes les dix transactions un nouveau bloc est créé.

Ce programme est destiné à tourner dans une machine docker mais s'execute également en local.
Il faut avoir installer à l'aide de `pip` ou `pip3` les libs suivantes:
* hashlib
* pycryptodome

Si vous avez le problème suivant: AttributeError: module 'time' has no attribute 'clock'
--> 
* désinstaller PyCrypto si installé: `pip3 uninstall PyCrypto`
* installer PyCryptodome: `pip3 install -U PyCryptodome`

Pour run le projet dans un docker container:
```shell
docker pull shaneosaure/blockchainproject
docker run -it shaneosaure/blockchainproject
```

Ou si vous voulez build l'image docker en local:
```shell
docker build -t DOCKERFILE shaneosaure/blockchainproject .
```

Projet réalisé par :
* [Aymeric BOURDIN](https://github.com/warzazate)
* [Rémi JARDRET](https://github.com/RemiESAIP)
* [Stéphane SIMON](https://github.com/Shaneosaure)
* [Thomas PERRAULT](https://github.com/BethGarion)
