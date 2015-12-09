#!/bin/bash

echo "start"
num=0
for entry in *
do
  ext=`echo $entry | rev | cut -d "." -f 1 | rev`
  name=`echo $entry | rev | cut -d "." -f 2 | rev`
  if [ "$ext" = "bmp" ]; then
  	i=$(($i + 1))
  fi
  # sips -s format png img/g10.bmp --out img/g10.png
  sips -s format png $entry --out $name.png
done
echo "total = $i"
echo "done"