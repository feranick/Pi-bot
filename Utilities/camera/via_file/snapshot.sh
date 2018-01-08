#!/bin/bash
FILENAME=$(echo `TZ='AMERICA/New_York' date +%d_%m_%Y_%H_%M_%S`".jpg")
#FILENAME="image.jpg"

raspistill -o $FILENAME --nopreview --exposure sports --timeout 1 -w 768 -h 768

convert -rotate "180" $FILENAME $FILENAME
convert -set colorspace Gray -separate -average $FILENAME $FILENAME

convert -resize 20x20  $FILENAME $FILENAME

python3 image_data.py $FILENAME
mv $FILENAME* /var/www/html

