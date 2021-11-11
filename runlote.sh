#!/bin/bash
#BeginScript

# Changing the work directory
cd "/root/hardfinger/"

# Warning threshold (integer value)
warningPercent="6"

freeSpace=`df /opt/home | awk '/[0-9]%/{print $(NF-2)}'`
totalSpace="1610612736" # 1.5TB

freePercent=`echo "($freeSpace / $totalSpace) * 100.0" | bc -l`
#echo $freePercent
flag=`echo $freePercent'<'$warningPercent | bc -l`
#echo $flag

if [ "$flag" = "1" ]; then
   logger -s "[HardFinger] ($freePercent) Low space! Sending e-mails now."
   python run.py 1 & python run.py 2 & python run.py 3;
   python run.py 4 & python run.py 5 & python run.py 6;
   python run.py 7 & python run.py 8 & python run.py 9;
   python run.py 10 & python run.py 11 & python run.py 12;
   logger -s "[HardFinger] Finished"
fi

# EndScript