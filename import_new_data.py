import pandas as pd

def get_new_format():
    ecdc = pd.read_excel('data/ecdcdata.xlsx')
    # print (ecdc.columns)
    ecdc = ecdc.rename(columns={'dateRep':'DateRep','day':'Day', 'month':'Month', 'year':'Year', 'cases':'Cases', 'deaths':'Deaths',
       'countriesAndTerritories':'Countries and territories', 'geoId':'GeoId','popData2018':'Pop_Data.2018'})
    # print (ecdc.columns)
    ecdc.to_csv('data/ecdcdata.csv',index=False)

def preprocess_codes():
    ecdc = pd.read_csv('data/ecdcdata.csv')
    codes = pd.read_csv('data/newcodes.csv')
    df = ecdc.groupby(['Countries and territories','GeoId'])['Cases'].sum().reset_index()
    countryDict = {}
    for i,r in df.iterrows():
        countryDict[r['GeoId']]=r['Countries and territories']
    # codes['Country'] = codes['Alpha-2 code'].map(countryDict)
    # codes.to_csv('newcodes.csv')
    allcodes = codes['Alpha-2 code']
    newcodes=[]
    for i,r in codes.iterrows():
        if r['Alpha-2 code'] in countryDict:
            pass
        else:
            countryDict[r['Alpha-2 code']]=r['Country']
    codes['Country'] = codes['Alpha-2 code'].map(countryDict)
    codes.to_csv('newcodes.csv',index=False)

def get_iso_2_3_codes():
    df = pd.read_csv('data/newcodes.csv')
    iso2Dict= {}
    iso3Dict = {}
    for i,r in df.iterrows():
        iso2Dict[r['Alpha-2 code']]=r['Country']
        iso3Dict[r['Alpha-3 code']]=r['Country']
    return (iso2Dict,iso3Dict)

def merge_countries_borders_ecdc():
    borders = pd.read_csv('data/country-borders.csv')
    borders = borders.fillna('None')
    codes = pd.read_csv('data/newcodes.csv')
    codeDict = {}
    for i,r in codes.iterrows():
        codeDict[r['Alpha-2 code']]=r['Country']
    borders['country_name']=borders['country_code'].map(codeDict)
    borders.to_csv('borders.csv')
    ecdc = pd.read_csv('data/ecdcdata.csv')
    ecdc=ecdc.drop(['Day','Month','Year'],axis=1)
    df0 = borders.groupby(['country_code','country_name'])['country_border_code'].apply(','.join).reset_index()
    borderDict = {}
    for i,r in df0.iterrows():
        codelist = r['country_border_code'].split(',')
        if 'None' in codelist or 'SS' in codelist:
             borderDict[r['country_name']]='None'
        else:
            borderDict[r['country_name']]=[codeDict[c] for c in codelist]
    df0['countries_border_names'] = df0['country_name'].map(borderDict)
    allcodes = df0['country_border_code'].tolist()
    newcodes=[]
    for a in allcodes:
        if 'None' not in a:
            newcodes.append(a.split(','))
        else:
            newcodes.append('None')
    df0['country_border_code']=newcodes
    df0 = df0.rename(columns={"country_name":"Countries and territories","country_border_code":"countries_border_codes","country_border_name":"countries_border_names"})
    df_final = pd.merge(ecdc,df0,on='Countries and territories',how='left')
    return df_final #THIS DATAFRAME CONTAINS INFORMATION FOR BORDER COUNTRIES AND CASES-DEATHS-POPULATION OF EACH COUNTRY

def read_data():
    get_new_format()
    iso2,iso3 = get_iso_2_3_codes()
    ecdc = pd.read_csv('data/ecdcdata.csv')
    ecdc=ecdc.drop(['Day','Month','Year'],axis=1)
    whr = pd.read_csv('data/whr2019.csv')
    hfr = pd.read_csv('data/human_freedom.csv')
    bank = pd.read_csv('data/world_bank_data.csv')
    oecd = pd.read_csv('data/oecd_data.csv')
    codes = pd.read_csv('data/newcodes.csv')
    whr = whr.rename(columns={"Log of GDP\nper capita":"Log of GDP per capita","Healthy life\nexpectancy":"Healthy life expectancy",'country':'Countries and territories'})
    codes = codes.rename(columns={'Country':'Countries and territories'})
    ecdc_loc = pd.merge(ecdc,codes,on='Countries and territories',how='left') #THIS DATAFRAME CONTAINS ECDC DATA AND THE ISO CODES AND LOCATION DATA
    ecdc_whr = pd.merge(ecdc,whr,on='Countries and territories',how='left') #THIS DATAFRAME CONTAINS ECDC DATA MERGED WITH THE WORLD HAPPINESS RECORDS
    ecdc_hfr = pd.merge(ecdc,hfr,on='Countries and territories',how='left') #THIS DATAFRAME CONTAINS ECDC DATA AND THE HUMAN FREEDOM INDICES
    ecdc_bank = pd.merge(ecdc,bank,on='Countries and territories',how='left') #THIS DATAFRAME CONTAINS ECDC DATA MERGED WITH THE WORLD DATA BANK DATA
    ecdc_oecd = pd.merge(ecdc,oecd,on='Countries and territories',how='left') #THIS DATAFRAME CONTAINS ECDC DATA MERGED WITH THE OECD DATA
    return ecdc_loc,ecdc_whr,ecdc_hfr,ecdc_bank,ecdc_oecd,ecdc,oecd,hfr,bank,whr,codes


ecdc_borders = merge_countries_borders_ecdc()
ecdc_loc,ecdc_whr,ecdc_hfr,ecdc_bank,ecdc_oecd,ecdc,oecd,hfr,bank,whr,codes = read_data()
