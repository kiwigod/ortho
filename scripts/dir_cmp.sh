#!/bin/sh
#Author: Arjun Sardjoe Missier


IN=$(find $1 -type f -name '*.csv')
IN2=$2


for pat in $IN;
do
    CMP="$IN2/""$(echo $pat | awk -F '[/]' '{print $(NF-1)"/"$NF}')"

    if [ "$(md5sum $pat | awk '{print $1}')" = "$(md5sum $CMP | awk '{print $1}')" ];
    then
        echo "$pat and $CMP are matching"
    else
        echo "$pat and $CMP are different"
    fi
done
