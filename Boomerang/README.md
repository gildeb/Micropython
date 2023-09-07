# Projet d'instrumentation du vol d'un boomerang

L'objectif est l'enregistrement de l'accélération est de la vitesse de rotation pendant 
une durée de 10 secondes (échantillonage à 100Hz).

Les données sont fournies par l'imu MPU6050 piloté par un ESP01 sous micropython, alimenté 
par une batterie Li-ion (type bouton). Elles sont stockées sur l'ESP01 (fichiers MPU6050_xxx.dat).

Le driver du MPU6050 (module MPU6050dmp20) utilise le DMP (Digital Motion Processing).

L'envoi des commandes à l'ESP01 (démarrage acquisition, récupération/suppression de fichiers) se fait en WiFi 
(ESP01 en mode Access Point) par socket IP.

> __MPU6050_dataServer.py__ : à lancer au boot de l'ESP01
> 
> __MPU6050_dataClient.py__ : script d'envoi des commandes depuis un PC
