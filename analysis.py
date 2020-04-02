import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import requests
import pickle
import urllib.request


def get_dates(df):
    df = df[pd.notnull(df['DateRep'])]
    df['DateRep']=df['DateRep'].astype(str)
    df = df.sort_values(by='DateRep', ascending=False)
    dates = df['DateRep']
    return {'first': datetime.strptime(dates.iloc[-1], '%Y-%m-%d').strftime('%d-%m-%Y'), 'last': datetime.strptime(dates.iloc[0], '%Y-%m-%d').strftime('%d-%m-%Y')}

def get_total_cases(df):#
    return df['NewConfCases'].sum()

def get_total_deaths(df):#
    return df['NewDeaths'].sum()

def get_total_casesEU(df):#
    df = df[df['region'].isin(['Eastern Europe','Western Europe'])]
    return df['NewConfCases'].sum()

def get_total_deathsEU(df):#
    df = df[df['region'].isin(['Eastern Europe','Western Europe'])]
    return df['NewDeaths'].sum()

def get_total_cases_nonEU(df):
    df = df[~df['region'].isin(['Eastern Europe','Western Europe'])]
    return df['NewConfCases'].sum()

def get_total_deaths_nonEU(df):#
    df = df[~df['region'].isin(['Eastern Europe','Western Europe'])]
    return df['NewDeaths'].sum()

def get_todays_cases_EU(df):
    df=df[df['region'].isin(['Eastern Europe','Western Europe'])]
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewConfCases'].iloc[-1]

def get_todays_cases_nonEU(df):
    df=df[~df['region'].isin(['Eastern Europe','Western Europe'])]
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewConfCases'].iloc[-1]

def get_todays_cases_global(df):
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewConfCases'].iloc[-1]

def get_todays_deaths_EU(df):
    df=df[df['region'].isin(['Eastern Europe','Western Europe'])]
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewDeaths'].iloc[-1]

def get_todays_deaths_nonEU(df):
    df=df[~df['region'].isin(['Eastern Europe','Western Europe'])]
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewDeaths'].iloc[-1]

def get_todays_deaths_global(df):
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewDeaths'].iloc[-1]

def get_total_cases_per_day(df):#
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_day(df):
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    return df1

def get_total_cases_per_country_per_day(df):#
    df1 = df.groupby(['DateRep','CountryExp'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_country_per_day(df):#
    df1 = df.groupby(['DateRep', 'CountryExp'])['NewDeaths'].sum().reset_index()
    return df1

def get_total_cases_per_country(df):
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_EU(df):
    df1 = df[df['EU']=='EU']
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_nonEU(df):
    df1 = df[df['EU']!='EU']
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_hf(df):
    df1 = df.groupby(['CountryExp','hf_score'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_cap(df):
    df1 = df.groupby(['CountryExp','Corruption'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_country(df):
    df1 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    return df1

def get_total_deaths_per_country_EU(df):
    df1 = df[df['EU']=='EU']
    df1 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    return df1

def get_total_deaths_per_country_nonEU(df):
    df1 = df[df['EU']!='EU']
    df1 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    return df1

def get_cases_per_specific_country(df,country):
    df1 = df[df['CountryExp']==country]
    df2 = df1.groupby(['DateRep','CountryExp'])['NewConfCases'].sum().reset_index()
    return df2

def get_deaths_per_specific_country(df,country):
    df1 = df[df['CountryExp']==country]
    df2 = df1.groupby(['DateRep','CountryExp'])['NewDeaths'].sum().reset_index()
    return df2

def get_total_distribution_of_cases(df):
    dfa = get_total_cases_per_country(df)
    # print (dfa)
    val = 'NewConfCases'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_cases_per_specific_country(df,country):
    dfa = get_cases_per_specific_country(df,country)
    # print (dfa)
    val = 'NewConfCases'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_deaths(df):
    dfa = get_total_deaths_per_country(df)
    # print (dfa)
    val = 'NewDeaths'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_deaths_per_specific_country(df,country):
    dfa = get_deaths_per_specific_country(df,country)
    # print (dfa)
    val = 'NewDeaths'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_cases_per_capita(df):
    df1 = df.groupby('logCapita')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_life_expectancy(df):
    df1 = df.groupby('Healthy life expectancy')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_generosity(df):
    df1 = df.groupby('Generosity')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_social_support(df):
    df1 = df.groupby('Social support')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_corruption(df):
    df1 = df.groupby('Corruption')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_freedom(df):
    df1 = df.groupby('Freedom')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_human_freedom(df):
    # print (df['hf_score'],df['NewConfCases'])
    # df['NewConfCases']+=1
    # df['NewConfCases']=df['NewConfCases'].apply(np.log10)
    df1 = df.groupby('hf_score')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_rank(df):
    df1 = df.groupby('Ladder')['NewConfCases'].sum().reset_index()
    return df1

def get_countries_per_capita(df):
    df0 = df
    df0 = df0[df0['logCapita']>-1]
    df1 = df0.groupby('CountryExp')['logCapita'].mean().to_frame('capita').reset_index()
    return df1

def get_recovered_cases_in_greece():
    data = requests.get("https://covid19.mathdro.id/api/countries/Greece/recovered").json()
    return data[0]['recovered']

def get_recovered_cases_world():
    data = requests.get("https://covid19.mathdro.id/api").json()
    return data['recovered']['value']

def get_mapped_data(df):
    df1 = df.groupby(['CountryExp','lat','lon'])['NewDeaths','NewConfCases'].sum().reset_index()
    return df1

def map_greek_data():
    import pandas as pd
    from geopy.geocoders import Nominatim
    import pickle
    grcases = pd.read_csv('static/data/Greece.csv')
    locs = grcases['cities'].tolist()
    geolocator = Nominatim(user_agent="COVID")
    mapping={}
    for l in locs:
        try:
            location = geolocator.geocode(l)
            print (l)
            mapping[l]=(location.latitude, location.longitude)
        except:
            print ('none')
    maps = pickle.dump(mapping,open('mappingGR','wb'))

def get_greek_data():
    mapping = pickle.load(open('static/data/mappingGR','rb'))
    df = pd.read_csv('static/data/Greece.csv')
    latdict={}
    londict={}
    for k,v in mapping.items():
        latdict[k]=round(v[0],3)
        londict[k]=round(v[1],3)
    df['lat']=df['cities'].map(latdict)
    df['lon']=df['cities'].map(londict)
    return (df)

def get_total_cases_per_countryEU_per_day(df):
    df1 = df.groupby(['DateRep','region'])['NewConfCases'].sum().reset_index()
    return df1

def get_days_deaths_after_first_death():
    df = pickle.load(open('static/data/df.pickle','rb'))
    countries = ['Greece','Germany','Italy','Spain','United Kingdom of Great Britain and Northern Ireland','United States of America']
    firstdeath = pickle.load(open('static/data/firstdeath.pickle','rb'))
    first = min(firstdeath.values())
    adf =df[df['CountryExp'].isin(countries)]
    adf=adf.drop(['GeoId', 'region', 'iso2', 'Ladder', 'SD of Ladder', 'Positive affect',
       'Negative affect', 'Social support', 'Freedom', 'Corruption',
       'Generosity', 'logCapita', 'Healthy life expectancy', 'lat',
       'lon', 'hf_score'], axis=1)
    adf['DateRep'] =  pd.to_datetime(adf['DateRep'])
    adf = adf.sort_values(by='DateRep')
    adf = adf[adf['DateRep']>=first]
    adf['total_deaths'] = adf.groupby(['CountryExp'])['NewDeaths'].cumsum()
    dates = sorted(list(set(adf['DateRep'].tolist())))
    datedict={}
    i=0
    for d in dates:
        datedict[d]=i
        i+=1
    adf['Days']=adf['DateRep'].map(datedict)
    deathdict={}
    for d in adf['Days'].tolist():
        res = adf[adf['Days']==d]
        countryDeaths = []
        countrydict ={}
        for c in countries:
            for i,r in res.iterrows():
                if r['CountryExp']==c:
                    val = r['total_deaths']
                    countrydict[c]=round(np.log(val+1),2)
        deathdict[str(d)] = countrydict
    return deathdict

def get_cases_after_100():
    df = pickle.load(open('static/data/df.pickle','rb'))
    countries = ['Greece','Germany','Italy','Spain','United_Kingdom','United_States_of_America']
    adf =df[df['CountryExp'].isin(countries)]
    adf=adf.drop([ 'GeoId', 'region', 'iso2', 'Ladder', 'SD of Ladder', 'Positive affect',
       'Negative affect', 'Social support', 'Freedom', 'Corruption',
       'Generosity', 'logCapita', 'Healthy life expectancy', 'lat',
       'lon', 'hf_score'], axis=1)
    adf['DateRep'] =  pd.to_datetime(adf['DateRep'])
    adf = adf.sort_values(by='DateRep')
    adf['total_cases'] = adf.groupby(['CountryExp'])['NewConfCases'].cumsum()
    adf = adf.sort_values(by='DateRep')
    for i,r in adf.iterrows():
            if r['total_cases']>100:
                first=r['DateRep']
                break
    adf = adf[adf['DateRep']>=first]
    dates = sorted(list(set(adf['DateRep'].tolist())))
    datedict={}
    i=0
    for d in dates:
        datedict[d]=i
        i+=1
    adf['Days']=adf['DateRep'].map(datedict)
    casedict={}
    for d in adf['Days'].tolist():
        res = adf[adf['Days']==d]
        countryDeaths = []
        countrydict ={}
        for c in countries:
            for i,r in res.iterrows():
                if r['CountryExp']==c:
                    val = r['total_cases']
                    countrydict[c]=round(np.log(val+1),2)
        casedict[str(d)] = countrydict
    return casedict

def get_all_countries(df):
    return sorted(list(set(df['CountryExp'].tolist())))

def get_correlation_after_x_deaths(df,column,other_data,limit):
    df=df[df['region'].isin(['Eastern Europe','Western Europe'])]
    if other_data=='oecd':
        other = pd.read_csv('data/oecd_data.csv')
        other = other.rename(columns={'Countries and territories':'CountryExp'})
        other = other[['CountryExp',col]]
        other = other.dropna()
    else:
        other = pd.read_csv('data/world_bank_data.csv')
        other = other.rename(columns={'Countries and territories':'CountryExp'})
        other = other[['CountryExp',col]]
        other = other.dropna()
    df0 = pd.merge(df,other,on='CountryExp',how='left')
    df1 =df0.groupby(['CountryExp','Pop_Data.2018',col])['NewDeaths'].sum().reset_index()
    df1['percentage']=df1['NewDeaths']/df1['Pop_Data.2018']
    df1=df1[df1['NewDeaths']>=limit]
    from scipy.stats import spearmanr
    if col in ['Hospital Beds','Life expectancy']:
        corr, _ = spearmanr(df1[column], df1['NewDeaths'])
    else:
        corr, _ = spearmanr(df1[column], df1['percentage'])
    return corr, df1['NewDeaths'],df1[column]

def get_correlation_after_x_cases(df,column,other_data,limit):
    df=df[df['region'].isin(['Eastern Europe','Western Europe'])]
    if other_data=='oecd':
        other = pd.read_csv('data/oecd_data.csv')
        other = other.rename(columns={'Countries and territories':'CountryExp'})
        other = other[['CountryExp',col]]
        other = other.dropna()
    else:
        other = pd.read_csv('data/world_bank_data.csv')
        other = other.rename(columns={'Countries and territories':'CountryExp'})
        other = other[['CountryExp',col]]
        other = other.dropna()
    df0 = pd.merge(df,other,on='CountryExp',how='left')
    df1 =df0.groupby(['CountryExp','Pop_Data.2018',col])['NewConfCases'].sum().reset_index()
    print (df1.head(100))
    df1['percentage']=df1['NewConfCases']/df1['Pop_Data.2018']
    df1=df1[df1['NewConfCases']>=limit]
    from scipy.stats import spearmanr
    if col in ['Hospital Beds','Life expectancy']:
        corr, _ = spearmanr(df1[column], df1['NewConfCases'])
    else:
        corr, _ = spearmanr(df1[column], df1['percentage'])
    return corr, df1['NewConfCases'],df1[column]

def doubling_rate_deaths(df,limit):
    df['DateRep'] = pd.to_datetime(df['DateRep'])
    df=df.sort_values('DateRep')
    df['total_deaths'] = df.groupby(['CountryExp'])['NewDeaths'].cumsum()
    # df['total_cases'] = df.groupby(['CountryExp'])['NewConfCases'].cumsum()
    df=df[df['total_deaths']>limit]
    df['days']=np.nan
    for c in list(set(df['CountryExp'].tolist())):
        j=0
        for i,r in df.iterrows():
            if r['CountryExp']==c:
                j+=1
                df.at[i,'days'] = j
    df =df[['CountryExp','total_deaths','days']]
    df=df.sort_values(by='days')
    mydict={}
    for d in df['days']:
        df0 = df[df['days']==d]
        mydict[d]=dict(zip(df0.CountryExp, df0.total_deaths))
    return mydict

def doubling_rate_cases(df,limit):
    df['DateRep'] = pd.to_datetime(df['DateRep'])
    df=df.sort_values('DateRep')
    df['total_cases'] = df.groupby(['CountryExp'])['NewConfCases'].cumsum()
    # df['total_cases'] = df.groupby(['CountryExp'])['NewConfCases'].cumsum()
    df=df[df['total_cases']>limit]
    df['days']=np.nan
    for c in list(set(df['CountryExp'].tolist())):
        j=0
        for i,r in df.iterrows():
            if r['CountryExp']==c:
                j+=1
                df.at[i,'days'] = j
    df =df[['CountryExp','total_cases','days']]
    df=df.sort_values(by='days')
    mydict={}
    for d in df['days']:
        df0 = df[df['days']==d]
        mydict[d]=dict(zip(df0.CountryExp, df0.total_cases))
    return mydict

