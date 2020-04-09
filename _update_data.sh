echo "Fetching data from folkhälsomyndigheten..."
wget -q -O data.xlsx https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data

echo "Fetched data"
echo "Processing..."
python3 preprocess_data.py
echo "leDone!"
