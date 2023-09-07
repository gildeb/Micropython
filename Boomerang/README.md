# Projet d'instrumentation du vol d'un boomerang

L'objectif est l'enregistrement de l'accélération est de la vitesse de rotation pendant 
une durée de 10 secondes (échantillonage à 100Hz).

Les données sont fournies par l'imu MPU6050 piloté par un ESP01 sous micropython, alimenté 
par une batterie Li-ion (type bouton).

> MPU6050dmp20.py : transcrytpion sous micropython du driver Arduino de Jeff Rowberg. Le module est trop lourd pour être chargé en RAM et doit être integré au firmware.
> firmware-combined.bin : firmware micropython pour l'ESP01 contenant, entre autres, le module MPU6050dmp20
