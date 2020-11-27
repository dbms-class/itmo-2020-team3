#!/bin/sh
PRJ=project$1
git clone https://github.com/dbms-class/itmo-2020-team3
cd itmo-2020-team3
git checkout -b $PRJ
mkdir $PRJ
cd $PRJ
cp "$2" $PRJ.sql
git add $PRJ.sql
git commit 
git push origin
