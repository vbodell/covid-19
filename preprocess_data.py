#!/usr/bin/env python
from re import sub

import pandas as pd

# Column name mappings
day_rename_dict = {'Statistikdatum': 'date',
                   'Datum_vårdstart': 'date',
                   'Datum_avliden': 'date',
                   'Totalt_antal_fall': 'total_cases',
                   'Totalt_antal_avlidna': 'total_deceased',
                   'Antal_avlidna': 'total_deceased',
                   'Totalt_antal_intensivvårdade': 'total_icu',
                   'Antal_intensivvårdade': 'total_icu',
                  }
total_rename_dict = {'Region': 'region',
                     'Kön': 'sex',
                     'Åldersgrupp': 'agegroup',
                     'Totalt_antal_fall': 'total_cases',
                     'Fall_per_100000_inv': 'cases_per_100k',
                     'Totalt_antal_avlidna': 'total_deceased',
                     'Totalt_antal_intensivvårdade': 'total_icu',
                    }

def _main():
    # Get data
    dfdict = pd.read_excel('data.xlsx', sheet_name=list(range(6)))

    region_day = dfdict[0]
    deaths_all_day = dfdict[1]
    ic_all_day = dfdict[2]
    region_total = dfdict[3]
    sex_total = dfdict[4]
    age_total = dfdict[5]

    # Rename columns
    ic_all_day.rename(columns=day_rename_dict, inplace=True)
    region_day.rename(columns=day_rename_dict, inplace=True)
    deaths_all_day.rename(columns=day_rename_dict, inplace=True)

    region_total.rename(columns=total_rename_dict, inplace=True)
    sex_total.rename(columns=total_rename_dict, inplace=True)
    age_total.rename(columns=total_rename_dict, inplace=True)

    # All total-data in one DataFrame
    total_df = pd.concat([region_total, sex_total, age_total])
    # Reorder columns
    total_df = total_df[['region', 'sex', 'agegroup',
        'total_cases', 'cases_per_100k', 'total_icu', 'total_deceased']]

    # Process date-data
    region_day.date = pd.to_datetime(region_day.date, errors='coerce')
    deaths_all_day.date = pd.to_datetime(deaths_all_day.date, errors='coerce')
    ic_all_day.date = pd.to_datetime(ic_all_day.date, errors='coerce')

    # Merge datasets
    day_df = pd.merge(region_day, deaths_all_day, how='outer', on='date')
    day_df = pd.merge(day_df, ic_all_day, how='outer', on='date')

    # Rename 'Uppgift saknas'
    total_df.loc[total_df['sex'] == 'Uppgift saknas','sex'] = 'unknown'
    total_df.loc[total_df['agegroup'] == 'Uppgift saknas','agegroup'] = 'unknown'

    total_df.loc[total_df.agegroup.notna(),'agegroup'] = \
        [sub(r'Ålder_([0-9]+)_([0-9]+)', r'\1-\2', x) for x
                in total_df.loc[total_df.agegroup.notna(),'agegroup']]
    total_df.loc[total_df['agegroup'] == 'Ålder_90_plus', 'agegroup'] = '90+'

    # Save data
    total_df.to_pickle('total.pkl')
    day_df.to_pickle('day.pkl')

if __name__ == '__main__':
    _main()
