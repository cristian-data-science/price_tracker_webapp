#!/bin/bash

# ejecutando crawlers

#python3 ./video_cards/video_cards/spiders/autospdigital.py
python3 /home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/spiders/autopcfactory.py
python3 /home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/spiders/autowinpy.py
python3 /home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/spiders/tecnomaster.py


# ejecutando data cleaners

python3 /home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/cleaners/autocleanerPC.py
python3 /home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/cleaners/autocleanerTN.py
#python3 ./video_cards/video_cards/cleaners/autocleanerSP.py
python3 /home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/cleaners/autounify.py

# copiando resultado a directorio de la app

cp -rf /home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/resultadofinal.csv /home/ubuntu/gitprojects/price_tracker_webapp/resultadofinal.csv

# ejecutando autopush

#  copiar o mover este script a /usr/bin o /usr/local/bin y desde el directorio donde se encuentre la copia de un repo git, ejecútalo de esta manera:
# script + <ficheros>

# Comprobamos si el directorio en el que estamos es de un repositorio git
cd /home/ubuntu/gitprojects/price_tracker_webapp/

if [ ! -d '.git' ]; then
	echo 'Esta carpeta no contiene un repositorio Git'
	exit -1
fi

# Ahora comprobamos si se le paso algun parametro
if [ $# == 0 ]; then
	echo "UpToGit: ¡Error! No se le a pasado ningún parámetro"
	echo "uptogit fichero1 fichero2 ... ficheroN"
	exit -1
else
	# Recorremos los parametros para comprobar si son ficheros o directorios
	for file in $*; do
		if [ ! -e $file ]; then
			echo "UpToGit: El archivo o directorio $file no existe"
			exit -1
		fi
	done
	
	# Si llegamos hasta aquí, indicamos a Git los archivos a subir
	git add $*
	
	# Esto nos pedira el mensaje del commit
	
	git commit -m "data source update"

	# Y terminamos subiendo los archivos
	git push -u origin master

fi