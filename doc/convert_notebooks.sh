#!/usr/bin/sh

echo "Convert all notebook files to .rst"

FILES=$(find . -name "*.ipynb" -not -path "*.ipynb_checkpoints*")

for f in $FILES
do
    echo $f
    ipython nbconvert $f --to rst --stdout 2>> /dev/null 1> "${f%.*}.txt"
done
