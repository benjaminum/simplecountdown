#!/bin/bash
CURRENT_DIR=`pwd`
DIRNAME=`basename $CURRENT_DIR`
cd ..
zip -rv simplecountdown.zip $DIRNAME -i \*.py \*.desktop
cd $CURRENT_DIR
