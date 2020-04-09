# Data is updated at 2pm every day, only update if file doesn't exist
# or we didn't update yesterday or it's after 2pm and we haven't updated
datafile=data.xlsx

if [ ! -f $datafile ]; then
    echo "Data doesn't exist, fetching latest"
    ./_update_data.sh
else
    curtime=$( date "+%s" )
    updatetime=$( date -v14H -v0M -v0S "+%s" )
    yesterupdate=$( date -v-1d -v0H -v0M -v0S "+%s" )
    lastupdate=$( date -r $datafile "+%s" )

    if [ $lastupdate -lt $yesterupdate ] || \
       [ $curtime -gt $updatetime -a $lastupdate -lt $updatetime ]; then
        echo "Data has been updated since last fetch, updating..."
        ./_update_data.sh
    else
        echo "Data is updated, starting playground..."
    fi
fi

jupyter notebook
