#!/usr/bin/env python
import pandas as pd

# Column name mappings
total_rename_dict = {'Kön': 'sex',
                     'Åldersgrupp': 'agegroup',
                     'Totalt_antal_fall': 'total_cases',
                     'Fall_per_100000_inv': 'cases_per_100k',
                     'Totalt_antal_avlidna': 'total_deceased',
                     'Totalt_antal_intensivvårdade': 'total_icu',
                    }
day_rename_dict = {'Statistikdatum': 'date',
                   'Totalt_antal_fall': 'total_cases',
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

    # All total-data in one DataFrame
    total_df = pd.concat([region_total, sex_total, age_total])
    # Reorder columns
    total_df = total_df[['Region', 'Kön', 'Åldersgrupp',
                         'Totalt_antal_fall', 'Fall_per_100000_inv',
                         'Totalt_antal_intensivvårdade', 'Totalt_antal_avlidna']]

    # Process date-data
    region_day.Statistikdatum = pd.to_datetime(region_day.Statistikdatum)

    deaths_all_day.rename(columns={'Datum_avliden': 'Statistikdatum',
                                   'Antal_avlidna': 'Totalt_antal_avlidna'},
                          inplace=True)
    if sum(deaths_all_day.Statistikdatum == 'Uppgift saknas') > 0:
        deaths_all_day.loc[
            deaths_all_day.Statistikdatum == 'Uppgift saknas', 'Statistikdatum'
        ] = pd.NA
    deaths_all_day.Statistikdatum = pd.to_datetime(deaths_all_day.Statistikdatum)

    ic_all_day.rename(columns={'Datum_vårdstart': 'Statistikdatum',
                               'Antal_intensivvårdade': 'Totalt_antal_intensivvårdade'},
                      inplace=True)
    if sum(ic_all_day.Statistikdatum == 'Uppgift saknas') > 0:
        ic_all_day.loc[
            ic_all_day.Statistikdatum == 'Uppgift saknas', 'Statistikdatum'
        ] = pd.NA
    ic_all_day.Statistikdatum = pd.to_datetime(ic_all_day.Statistikdatum)

    # Merge datasets
    day_df = pd.merge(region_day, deaths_all_day, how='outer', on='Statistikdatum')
    day_df = pd.merge(day_df, ic_all_day, how='outer', on='Statistikdatum')

    # Rename 'Uppgift saknas'
    total_df.loc[total_df['Kön'] == 'Uppgift saknas','Kön'] = 'unknown'
    total_df.loc[total_df['Åldersgrupp'] == 'Uppgift saknas','Åldersgrupp'] = 'unknown'

    # Rename columns
    total_df.rename(columns=total_rename_dict, inplace=True)
    day_df.rename(columns=day_rename_dict, inplace=True)

    # Save data
    total_df.to_pickle('total.pkl')
    day_df.to_pickle('day.pkl')

if __name__ == '__main__':
    _main()
