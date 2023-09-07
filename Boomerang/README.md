# Projet d'instrumentation du vol d'un boomerang

L'objectif est l'enregistrement de l'accélération est de la vitesse de rotation pendant 
une durée de 10 secondes (échantillonage à 100Hz).

Les données sont fournies par l'imu MPU6050 piloté par un ESP01 sous micropython, alimenté 
par une batterie Li-ion (type bouton). Elles sont stockées sur l'ESP01 (fichiers MPU6050_xxx.dat)

> __MPU6050dmp20.py__ : transcription sous micropython du driver Arduino de Jeff Rowberg. Le module est trop lourd pour être chargé en RAM et doit être integré au firmware.
> 
> __firmware-combined.bin__ : firmware micropython pour l'ESP01/ESP8266 contenant, entre autres, le module MPU6050dmp20
