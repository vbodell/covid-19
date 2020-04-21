# Data is updated at 2pm every day, only update if file doesn't exist
# or we didn't update yesterday or it's after 2pm and we haven't updated

run_github_update () {
    ./_update_data.sh
    jupyter nbconvert --to notebook --execute covid-playground.ipynb --inplace
    git add covid-playground.ipynb
    git commit -m "Update"
    git push
}

datafile=data.xlsx

if [ ! -f $datafile ]; then
    echo "Data doesn't exist, fetching latest"
    run_github_update
else
    curtime=$( date "+%s" )
    updatetime=$( date -v14H -v0M -v0S "+%s" )
    yesterupdate=$( date -v-1d -v0H -v0M -v0S "+%s" )
    lastupdate=$( date -r $datafile "+%s" )

    if [ $lastupdate -lt $yesterupdate ] || \
       [ $curtime -gt $updatetime -a $lastupdate -lt $updatetime ]; then
        echo "Data has been updated since last fetch, updating..."
        run_github_update
    else
        echo "Data is already updated. Exiting..."
        exit 1
    fi
fi

