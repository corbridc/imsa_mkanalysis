#-------------------------------------------------------------
 # 
 #   .SYNOPSIS
 #   Data analysis for MarketPntl.
 #   
 #   .NOTES
 #   Author: Cameron Corbridge
 #   Required Dependencies: pandas, numpy, requests
 #   
#-------------------------------------------------------------

#==========================================
#  PARMETERS / VARIABLES
#==========================================

# Initialize libraries.
import pandas as pd
import numpy as np
import random
import scipy.stats as stats
import time
import json
import requests
from datetime import date
import os

#==========================================
#  FUNCTIONS: APIs
#==========================================

# Pulls the data for the given hs code from the UN Comrade API. 
def imports_api(hs_code):

    # Get API data.
    year_ = date.today().year
    year = str(year_ - 2) + '%2C' + str(year_ - 3) + '%2C' + str(year_ - 4)
    params = {
        'r': 'all',
        'px': 'HS',
        'ps': year,
        'p': 0,
        'rg': 1,
        'cc': hs_code,
        'type': 'C',
        'freq': 'A',
    }
    url = 'https://comtrade.un.org/api/get?'
    for key in params.keys():
        url += (key + '=' + str(params[key]) + '&')
    url = url[:-1]
    resp = requests.get(url)

    # Process API dat.
    normalized = pd.json_normalize(resp.json()['dataset'])
    if (resp.status_code != 200) or (len(normalized) < 1):
        raise Exception("Import data inaccessible. Invalid HS code?")
    
    return normalized

# Pulls EODB data from the World Bank API.
def eodb_api():   

    # Get API data.
    url = 'https://api.worldbank.org/v2/en/country/all/indicator/IC.BUS.DFRN.XQ?format=json&per_page=20000&source=2'
    resp = requests.get(url)
    if (resp.status_code != 200):
        raise Exception("Ease of business data inaccessible.")

    # Process API data.
    normalized = pd.json_normalize(resp.json()[1])
    normalized.dropna(inplace=True)
    a = normalized.groupby(['country.value']).agg({'date': 'max'})
    a = a.reset_index()
    both = pd.merge(a, normalized, how='right')
    length = normalized.groupby(['country.value']).max().shape[0]
    eodb = both[:length][['country.value', 'value', 'date']]
    
    return eodb

# Pulls LPI data from the World Bank API.
def lpi_api():

    # Get API data.
    url = 'https://api.worldbank.org/v2/en/country/all/indicator/LP.LPI.OVRL.XQ?format=json&per_page=20000&source=2'
    resp = requests.get(url)
    if (resp.status_code != 200):
        raise Exception("Logistic performance data inaccessible.")

    # Process API data.
    normalized = pd.json_normalize(resp.json()[1])
    normalized.dropna(inplace=True)
    a = normalized.groupby(['country.value']).agg({'date': 'max'})
    a = a.reset_index()
    both = pd.merge(a, normalized, how='right')
    length = normalized.groupby(['country.value']).max().shape[0]
    lpi = both[:length][['country.value', 'value', 'date']]

    return lpi 

# Pulls economic and political risk data from a pre-created Excel sheet by InternationalHub.
def epr_api():

    # Get API data.
    try:
        df = pd.read_excel('https://marketanalysis.internationalhub.org/data-econrisk.xlsx')
    except:
        raise Exception("Economic risk data inaccessible.")

    # Setting column names.
    col_names = df.iloc[6]
    col_names[1] = "Country"
    df.columns = col_names
    
    # Cleaning out the page, leaving just the data.
    df = df.loc[7:].reset_index()
    a=df.columns[:2]
    df = df.drop(columns=a, axis=1)
    
    # Edit commercial risk column to be numeric. 
    df.replace(['A','B','C'],[1,2,3],inplace=True)
    
    # Filling in the blanks from tiny countries that are not classifed. 
    df['Expropriation and Government Action Risk'].replace('-',2,inplace=True)
    df['Political Violence Risk'].replace('-',2,inplace=True)
    df['Premium classification OECD'].replace('-',2,inplace=True)
    df.rename(columns={'Political Risk\nShort Term' : 'Short Term Political Risk',
                       'Political Risk\nMedium/Long\nTerm' : 'Long Term Political Risk',
                       'Political Risk\nSpecial\ntransactions' : 'Political Risk, Special Transactions',
                       'Premium classification OECD' : 'OECD Country Risk'},
             inplace=True)
    df.drop('Political Risk, Special Transactions', axis=1, inplace=True)
    
    return df

# Pulls GDP data from the World Bank API.
def gdp_percap_api():   

    # Get API data.
    url = 'https://api.worldbank.org/v2/en/country/all/indicator/NY.GDP.PCAP.PP.CD?format=json&per_page=20000&source=2'
    resp = requests.get(url)
    if (resp.status_code != 200):
        raise Exception("GDP data inaccessible.")

    # Shapping the data to get the most recent year available.
    normalized = pd.json_normalize(resp.json()[1])
    normalized.dropna(inplace=True)
    a = normalized.groupby(['country.value']).agg({'date': 'max'})
    a = a.reset_index()
    both = pd.merge(a, normalized, how='right')
    length = normalized.groupby(['country.value']).max().shape[0]
    gdp_percap = both[:length][['country.value','value']]
    
    return gdp_percap

# Pulls population data from the World Bank API.
def population_api():
    
    # Get API data.
    url = 'https://api.worldbank.org/v2/en/country/all/indicator/SP.POP.TOTL?format=json&per_page=20000&source=2'
    resp = requests.get(url)
    if (resp.status_code != 200):
        raise Exception("Population data inaccessible.")
    
    # Process JOSN file.
    normalized = pd.json_normalize(resp.json()[1])
    normalized.dropna(inplace=True)
    
    # Shape data.
    a = normalized.groupby(['country.value']).agg({'date': 'max'})
    a = a.reset_index()
    both = pd.merge(a, normalized, how='right')
    length = normalized.groupby(['country.value']).max().shape[0]
    population = both[:length][['country.value','value']]
    
    return population

#==========================================
#  FUNCTIONS: ANALYSIS
#==========================================

# Fetch and transform import statistics.
def import_stats(hs_code):
    
    year_ = date.today().year
    
    try:
        normalized = imports_api(hs_code)
    except Exception as e:
        raise e
    
    description = normalized["cmdDescE"][0]
    num_years = normalized[normalized['rtTitle']=="USA"].shape[0]

    home_country = 'USA'
    normalized = normalized[(normalized['rtTitle'] != home_country)]
    normalized = normalized[normalized['rtTitle'] != 'Other Asia, nes'] # Pulling this out because it isn't very clear.
    
    df = pd.pivot_table(normalized, ['TradeValue'], ['rtTitle'], aggfunc=np.sum)
    df_average = df['TradeValue']/num_years
    df_average = pd.DataFrame(df_average)
    
    df_average = df_average.sort_values(['TradeValue'], ascending=False)
    df = pd.pivot_table(normalized, ['TradeValue'], ['rtTitle'], ['yr'], aggfunc=np.sum)
    df = df['TradeValue']
    df['change'] = (df[year_ - 2] - df[year_ - 3]) / df[year_ - 3]
    df = df.merge(df_average, on='rtTitle').fillna(0).reset_index()
    
    mp_indicators = df #DEBUG
    if num_years == 2:
        mp_indicators = df.drop(columns=[year_ - 2,year_ - 3])
    elif num_years == 3: 
        mp_indicators = df.drop(columns=[year_ - 2,year_ - 3,year_ - 4])
    
    df_top = df_average[:30]
    top_30 = pd.DataFrame(df_top.index)
    
    df = top_30.merge(df, on='rtTitle', how='left')
    
    output = top_30.merge(mp_indicators, on='rtTitle', how='left')
    output.reset_index(inplace=True)
    output.rename(columns={"rtTitle": "country", "TradeValue" : "tradevalue", "index" : "rank"}, inplace=True)
    output.set_index('country', inplace=True)
    output = output.to_json(orient='index')
    
    return output, description # Returns JSON with all the UN Comtrade data for the top 30 countries.

# Combine parametric weights.
def parametric_weights(EODBvMP,EODBvEPR, MPvEPR): # Accept these three values
    index = ['EPR', 'MP', 'EODB', 'Totals'] # Creating a pairwise table.
    d = {'EPR' : [50,MPvEPR,EODBvEPR],
         'MP' : [(100-MPvEPR), 50, EODBvMP],
         'EODB' : [(100-EODBvEPR),(100-EODBvMP),50]}  
    
    pairwise = pd.DataFrame(data=d,index=['EPR','MP','EODB'])
    pairwise_totals = [pairwise['EPR'].sum(),pairwise['MP'].sum(),pairwise['EODB'].sum()] 
    
    normalized_table = pd.DataFrame(pairwise / pairwise_totals)
    normalized_totals = pd.DataFrame(normalized_table.sum(axis=1))
    normalized_table['average'] = pd.DataFrame(normalized_table.mean(axis=1))
    
    eps_values = normalized_table.iloc[0]
    mp_values = normalized_table.iloc[1]
    eodb_values = normalized_table.iloc[2]
    
    eps_values = np.array([eps_values[1], eps_values[2]])
    mp_values = np.array([mp_values[0], mp_values[2]])
    eodb_values = np.array([eodb_values[0], eodb_values[1]])
    
    st_dev = [[np.std(eps_values)],[np.std(mp_values)],[np.std(eodb_values)]]
    st_dev = pd.DataFrame(st_dev, index = ['EPR','MP','EODB'], columns = ['St. Dev'])
    normalized_table['st_dev'] = st_dev
    
    norm_inv = []
    
    for i in range(normalized_table.shape[0]):
        if (normalized_table['st_dev'][i] <= 0.00001):
            stdv_temporary = 0.01
        else:
            stdv_temporary = normalized_table['st_dev'][i]
        
        random.seed(time.time())
        norm_inv.append(stats.norm.ppf(random.random(), loc=normalized_table['average'][i], scale=stdv_temporary))
        
    return norm_inv # Results in a list of weights (EPR, MP, EODB).

#==========================================
#  FUNCTIONS: MAIN
#==========================================

# Collect all data for initial presentation.
def pull_all_data(hs_code):   
    
    # Define rename dictionary.
    rename_dict = {
        'Viet Nam' : 'Vietnam', 
        'Hong Kong, China' : 'Hong Kong',
        'China, Hong Kong SAR' : 'Hong Kong',
        'Hong Kong SAR, China' : 'Hong Kong',
        'Korea (South)' : 'South Korea',
        'Rep. of Korea' : 'South Korea',
        'Korea, Rep.' : 'South Korea',
        'Korea, South' : 'South Korea',
        'Korea, North' : 'North Korea',
        'Korea (North)' : 'North Korea',
        'Lao PDR' : 'Laos',
        'Russian Federation' : 'Russia',
        'UAE - United Arab Emirates' : 'United Arab Emirates',
        'Czechia' : 'Czech Republic',
        'Dominican Rep.' : 'Dominican Republic',
        'Venezuela, RB' : 'Venezuela',
        'Iran, Islamic Rep.' : 'Iran',
        'State of Palestine' : 'Palestine',
        'Slovak Republic' : 'Slovakia',
        'Egypt, Arab Rep.' : 'Egypt',
        'Burma':'Myanmar',
        'Yemen, Rep.':'Yemen',
        'Bahamas, The':'Bahamas',
        'China, Macao SAR' : 'Macau',
    }
    
    # Process import data.
    try:
        hs_output, prod_description = import_stats(hs_code)
    except Exception as e:
        return str(e)
    df = pd.read_json(hs_output).transpose().reset_index().rename(columns={'index':'country'})
    top_30 = pd.DataFrame(df['country'])
    
    # Process market potential data.
    try:
        gdp_percap = gdp_percap_api().rename(columns={'country.value':'country'})
    except Exception as e:
        return str(e)
    names = pd.DataFrame(gdp_percap.set_index('country').rename(rename_dict).index)
    gdp_percap['country'] = names
    gdp_percap = top_30.merge(gdp_percap, on='country')
    
    # Process population data.
    try:
        population = population_api().rename(columns={'country.value':'country'})
    except Exception as e:
        return str(e)
    names = pd.DataFrame(population.set_index('country').rename(rename_dict).index)
    population['country'] = names
    population = top_30.merge(population, on='country')

    tradevalue = df[['country','tradevalue']]
    change = df[['country','change']]

    mp = gdp_percap.merge(population, on='country')
    mp = mp.merge(tradevalue, on='country')
    mp_data = mp.merge(change, on='country')
    mp_data.rename(columns={'value_x':'gdp_percap', 'value_y':'population'}, inplace='True')
    
    # Process logistics performance indicator data.
    try:
        lpi = lpi_api().rename(columns={'country.value':'country'})
    except Exception as e:
        return str(e)
    names = pd.DataFrame(lpi.set_index('country').rename(rename_dict).index)
    lpi = lpi.assign(country = names)
    lpi = top_30.merge(lpi, on='country')
    
    # Process ease of doing business data.
    try:
        eodb = eodb_api().rename(columns={'country.value':'country'})
    except Exception as e:
        return str(e)
    names = pd.DataFrame(eodb.set_index('country').rename(rename_dict).index)
    eodb = eodb.assign(country = names)
    eodb = top_30.merge(eodb, on='country')
    
    # Process country risk data.
    try:
        country_risk = pd.read_excel('https://marketanalysis.internationalhub.org/data-countryrisk.xls').rename(columns={'Country Name':'country'})
    except:
        return "Country risk data inaccessible."
    country_risk.rename(columns={ country_risk.columns[6]: "value"}, inplace=True)
    names = pd.DataFrame(country_risk.set_index('country').rename(rename_dict).index)
    country_risk = country_risk.assign(country = names)
    country_risk = top_30.merge(country_risk, on='country')
    country_risk = country_risk[['country', 'value']]
    
    eodb_data = lpi.merge(eodb, on='country')
    eodb_data = eodb_data.merge(country_risk, on='country')
    eodb_data.drop(axis=1, columns=['date_x', 'date_y'], inplace=True)
    eodb_data.rename(columns={'value_x':'lip_score',
                          'value_y':'eodb_score',
                          'value':'country_risk_score'}, inplace=True)
    
    # Merging data.
    epr = epr_api().rename(columns={'Country':'country'}) # Read in data.
    names = pd.DataFrame(epr.set_index('country').rename(rename_dict).index) # Cleaning country names.
    epr['country'] = names
    epr_data = top_30.merge(epr, on='country') # Removing excess countries.
    merged = mp_data.merge(eodb_data, on='country')
    merged = merged.merge(epr_data, on='country')
    merged = merged.round({"gdp_percap":0, "population":0, "tradevalue":0, "change":2, "eodb_score":2}) 
    merged = merged.to_dict(orient='records')
    result = dict({'data' : merged,
            'title' : prod_description})
    
    return result

# Analyze all data for final results.
def analyze_all_data(all_data, main_weights, sub_weights):

    # Unique function for weighting values accordingly.
    def weighted_value(indicator, weight):
        min_score = indicator.min()[1]
        range_score = float(indicator.max()[1]) - float(indicator.min()[1])
        indicator.rename(columns={'value':'value','tradevalue':'value','change':'value'},inplace=True)
        new = (indicator.loc[:,'value'] - min_score) / range_score
        indicator = indicator.assign(adjusted_rank = new)
        new = (indicator.loc[:,'adjusted_rank'] * (weight/100))
        indicator = indicator.assign(weighted_rank=new) 
        return indicator
    
    # Combine indicator weights. They should add to 1.
    mp_w1, mp_w2, mp_w3, mp_w4 = sub_weights['mp']
    eodb_w1, eodb_w2, eodb_w3 = sub_weights['eodb'] 
    pr = sub_weights['pr']
    er = sub_weights['er']
    
    epr_weight = []
    for i in pr:
        i = i/2
        epr_weight.append(i)
    
    f = []
    for i in er:
        i = i/2
        f.append(i)
    
    for i in f:
        epr_weight.append(i)
    
    prod_description = all_data['title']
    all_data = pd.DataFrame(all_data['data'])
    
    # Market potential analysis.
    population = all_data.iloc[:,[0,2]]
    population = population.rename(columns={'population':'value'})
    gdp_percap = all_data.iloc[:,[0,1]]
    gdp_percap = gdp_percap.rename(columns={'gdp_percap':'value'})
    tradevalue = all_data.iloc[:,[0,3]]
    tradevalue = tradevalue.rename(columns={'tradevalue':'value'})
    change = all_data.iloc[:,[0,4]]
    change = change.rename(columns={'change':'value'})
    
    mp_population = weighted_value(population, mp_w3)
    mp_gdp_percap = weighted_value(gdp_percap, mp_w4)
    mp_tradevalue = weighted_value(tradevalue, mp_w1)
    mp_change = weighted_value(change, mp_w2)

    mp_final = pd.DataFrame(all_data.iloc[:,0])
    score_total = mp_population.loc[:,'weighted_rank'] + mp_gdp_percap.loc[:,'weighted_rank'] + mp_tradevalue.loc[:,'weighted_rank'] + mp_change.loc[:,'weighted_rank']
    mp_final = mp_final.assign(weighted_score_total=score_total)
    minimum = mp_final['weighted_score_total'].min()
    value_range = (mp_final['weighted_score_total'].max() - mp_final['weighted_score_total'].min())
    score_total = ((mp_final.loc[:,['weighted_score_total']] - minimum) / value_range)
    mp_final = mp_final.assign(mp_adjusted_rank=score_total)

    # EODB analysis.
    lpi = all_data.iloc[:,[0,5]]
    lpi = lpi.rename(columns={'lip_score':'value'})
    eodb = all_data.iloc[:,[0,6]]
    eodb = eodb.rename(columns={'eodb_score':'value'})
    country_risk = all_data.iloc[:,[0,7]]
    country_risk = country_risk.rename(columns={'country_risk_score':'value'})
    
    eodb_lpi = weighted_value(lpi, eodb_w1)
    eodb_eodb = weighted_value(eodb, eodb_w2)
    eodb_country_risk = weighted_value(country_risk, eodb_w3)

    eodb_final = pd.DataFrame(all_data.iloc[:,0])
    score_total = eodb_lpi.loc[:,'weighted_rank'] + eodb_eodb.loc[:,'weighted_rank'] + eodb_country_risk.loc[:,'weighted_rank'] #We will need to add more here once there are more indicators
    eodb_final = eodb_final.assign(weighted_score_total = score_total)
    minimum = eodb_final['weighted_score_total'].min()
    value_range = (eodb_final['weighted_score_total'].max() - eodb_final['weighted_score_total'].min())
    score_total = ((eodb_final['weighted_score_total'] - minimum) / value_range)
    eodb_final = eodb_final.assign(eodb_adjusted_rank = score_total)


    # Economic and political risk analysis.
    epr = all_data.iloc[:,[0,8,9,10,12,11,13,14]]
    cols = epr.columns[1:] # Making a list of all data columns.
    df_empty = pd.DataFrame(columns=['country', 'values', 'adjusted_rank', 'weighted_rank', 'indicator']) # Creating an empty Dataframe with column names only, for appending to.
    num=0

    # Calculating the weighted and adjusted weight scores. This is a classic weighted analysis.
    for i in cols:
        indicator = pd.DataFrame(epr[i])
        min_score = indicator.min()
        range_score = float(indicator.max()) - float(indicator.min())
        new = abs(((indicator - min_score) / range_score ) - 1) + 0.0001
        indicator = indicator.assign(adjusted_rank = new)
        new = (indicator.loc[:,'adjusted_rank'] * epr_weight[num])
        indicator = indicator.assign(weighted_rank=new)
        indicator = pd.DataFrame(epr['country']).join(indicator)
        indicator.rename(columns={i:'values'},inplace=True)
        indicator['indicator'] = i
        df_empty = df_empty.append(indicator, ignore_index=True)
        num = num + 1

    # Adding together the weighted scores for every country. 
    epr_totals = df_empty[df_empty['indicator'] == 'Short Term Political Risk']['weighted_rank'].reset_index().drop(columns='index')
    totals = pd.DataFrame(columns=['total'])
    
    for i in cols[1:]:
        totals = totals + df_empty[df_empty['indicator'] == i]['weighted_rank'].reset_index().drop(columns='index')

    epr_totals.rename(columns={'weighted_rank':'weighted_score_total'}, inplace=True) # Renaming column with scores.
    epr_final = pd.concat([epr['country'],epr_totals], axis=1) # Add country names to weighted scores.

    # Calculate final weighted scores.
    minimum = epr_final['weighted_score_total'].min()
    value_range = (epr_final['weighted_score_total'].max() - epr_final['weighted_score_total'].min())
    score_total = ((epr_final.loc[:,['weighted_score_total']] - minimum) / value_range)
    epr_final = epr_final.assign(epr_adjusted_rank=score_total)
    
    epr_final = epr_final.sort_values('epr_adjusted_rank', ascending=False) # Sort.

    top_30 = pd.DataFrame(all_data.iloc[:,0])
    score_matrix = pd.DataFrame(top_30).set_index('country')
    for i in range(0,30):
        score_matrix[str(i)] = 0

    MPvEODB, EODBvEPR, EPRvMP = main_weights
    EODBvMP = 100 - MPvEODB
    MPvEPR = 100 - EPRvMP
    
    for i in range(200):
        erp_weight, mp_weight, eodb_weight = parametric_weights(EODBvMP, EODBvEPR, MPvEPR)
        overall_scores = pd.merge(epr_final, eodb_final, on='country')
        overall_scores = pd.merge(overall_scores, mp_final, on='country')
        overall_scores = overall_scores[['country','epr_adjusted_rank', 'eodb_adjusted_rank', 'mp_adjusted_rank']]
        scores_total = (overall_scores.loc[:,'epr_adjusted_rank'] * erp_weight) + (overall_scores.loc[:,'eodb_adjusted_rank'] * eodb_weight) + (overall_scores.loc[:,'mp_adjusted_rank'] * mp_weight)
        overall_scores = overall_scores.assign(weighted_sum = scores_total)
        max_weighted_sum = overall_scores['weighted_sum'].max()
        scores_total = (overall_scores['weighted_sum'] / max_weighted_sum)
        overall_scores = overall_scores.assign(weighted_score = scores_total)
        overall_scores = overall_scores.sort_values(['weighted_score'], ascending=False)
        overall_scores = overall_scores.reset_index().reset_index().drop('index', axis=1).rename(columns={'level_0':'rank'})
        need = overall_scores[['rank','country']].set_index('country')

        for i in range(top_30.shape[0]):
            score_matrix.loc[need.index[i]][str(need.loc[str(need.index[i])]['rank'])] = score_matrix.loc[need.index[i]][str(need.loc[str(need.index[i])]['rank'])] + 1

    score_matrix.columns = range(30)

    final_ranking = []
    for i in range(score_matrix.shape[0]-1):
        final_ranking.append(score_matrix[i].idxmax(axis=1))
        score_matrix.drop(score_matrix[i].idxmax(axis=1), axis=0, inplace=True)
        score_matrix[i+1] = score_matrix[i+1] + score_matrix[i] + 0.001
        score_matrix.drop(i, axis=1, inplace=True)
    final_ranking.append(score_matrix.index[0])

    final_ranking = pd.DataFrame(final_ranking)
    final_ranking = final_ranking.reset_index().rename(columns={'index':'rank', 0:'country'})
    final_ranking['rank'] = final_ranking['rank'] + 1

    final_ranking[['overall_score', 'mp_score', 'eodb_score', 'epr_score']] = overall_scores[['weighted_score', 'mp_adjusted_rank', 'eodb_adjusted_rank', 'epr_adjusted_rank']]

    names = ['overall_score', 'mp_score', 'eodb_score', 'epr_score']
    for name in names:
            final_ranking[name] = round(final_ranking[name], 2)

    # Making some of the values more easier to read.
    mp_population['value'] = mp_population['value'].apply(lambda x: '%.0f' % x)
    mp_gdp_percap['value'] = mp_gdp_percap['value'].round(2)
    mp_tradevalue['value'] = mp_tradevalue['value'].apply(lambda x: '%.0f' % x)
    mp_change['value'] = mp_change['value'].round(2)
    eodb_eodb['value'] = eodb_eodb['value'].round(2)

    dfs = [mp_population, mp_gdp_percap, mp_tradevalue, mp_change, eodb_lpi, eodb_eodb, eodb_country_risk]
    df_names = ['Population', 'GDP Per Capita', 'Import Value', 'Import % Change', 'Logistics Performance Index', 'Ease of Doing Business Index', 'Country Risk Index']
    merged = final_ranking

    for idx in range(len(dfs)):
        df = dfs[idx]
        merged = merged.merge(df[['country','value']], on='country')
        merged = merged.rename(columns={"value": df_names[idx]})

    merged = merged.merge(epr, on='country')
    merged = merged.to_dict(orient='records')
    result = dict({'data' : merged,
            'title' : prod_description})
    
    return result