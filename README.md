# Covid-19 data playground

A small python playground for the latest swedish covid-19 data from
[folkhälsomyndigheten](https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/).

## Dependencies
The following packages are used to facilitate playing

- [Pandas](https://pandas.pydata.org): To process data
- [Matplotlib](https://matplotlib.org): To plot graphs
- [Seaborn](https://seaborn.pydata.org): To plot high-level graphs
- [Jupyter notebook](https://jupyter.org): To 

To install these using [pip](https://pip.pypa.io/en/stable/) run
`pip install -r requirements.txt`

If you're using [conda](https://docs.conda.io/en/latest/) run
`conda install --file requirements.txt`

## How to run

1. Clone this repo
1. Run `./run_playground.sh`
1. The command will update the data source if there is new data available and
Jupyter notebook will launch, start a new notebook or 
keep editing `covid-playground.ipynb`

## Future work

- Track daily changes (interesting for total
- Come up with more fun graphs
