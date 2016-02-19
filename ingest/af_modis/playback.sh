cat $1 | while read line
do
    echo $line | sed "s|--date,time--|$(date --utc +%m/%d/%Y),$(date --utc +%H%M)|" > oneline.csv
    sleep 1
done
