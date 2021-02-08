#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# ## Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from [assets/wikipedia_data.html](assets/wikipedia_data.html) and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in [assets/nfl.csv](assets/nfl.csv)), MLB (baseball, in [assets/mlb.csv](assets/mlb.csv)), NBA (basketball, in [assets/nba.csv](assets/nba.csv) or NHL (hockey, in [assets/nhl.csv](assets/nhl.csv)). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
# 
# For each sport I would like you to answer the question: **what is the win/loss ratio's correlation with the population of the city it is in?** Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with [`pearsonr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%\*4=80%) of the grade for this assignment. You should only use data **from year 2018** for your analysis -- this is important!
# 
# ## Notes
# 
# 1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# 2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# 3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# 4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# ## Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.

# In[1]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re
pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)

def nhl_correlation(): 
    # YOUR CODE HERE
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # clean up cities
    cities.rename(columns = {"Population (2016 est.)[8]":"Population"},inplace=True)
    cities.replace(regex='\[.*\]', value='',inplace=True)
    cities = cities[['Metropolitan area','Population','NHL']]
    cities["NHL"] = cities["NHL"].replace({"RangersIslandersDevils": "Rangers Islanders Devils",
                                           "KingsDucks": "Kings Ducks"})
    cities['NHL'] = cities['NHL'].apply(lambda s: s.split())
    cities = cities.explode("NHL")
    # clean up nhl_df
    nhl_df = nhl_df[nhl_df['year']==2018]
    nhl_df = nhl_df[["team","W","L","year"]]
    nhl_df = nhl_df.drop([0,9,18,26])   
    nhl_df['team'].replace("\*$","",inplace=True,regex=True)
    nhl_df['team'] = nhl_df['team'].apply(lambda s:s.split()[-1]) # get rid of city names
    nhl_df = nhl_df.astype({"W":"int64","L":"int64"})
    nhl_df['W/L'] = nhl_df['W']/(nhl_df['W']+nhl_df['L'])
    # merge two dataframes
    df = pd.merge(cities,nhl_df,left_on="NHL",right_on="team").dropna()
    df = df.groupby('Population',sort=False).agg({"W/L":np.nanmean}).reset_index()
    df['Population'] = df['Population'].astype('float64')
    
    population_by_region = df['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = df['W/L'] # pass in win/loss ratio from nhl_df
    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nhl_correlation()


# In[ ]:





# ## Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NBA** using **2018** data.

# In[2]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def nba_correlation():
    # YOUR CODE HERE
    nba_df=pd.read_csv("assets/nba.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities.rename(columns = {"Population (2016 est.)[8]":"Population"},inplace=True)
    cities.replace(regex='\[.*\]', value='',inplace=True)
    cities = cities[['Metropolitan area','Population','NBA']]
    cities["NBA"] = cities["NBA"].replace({"KnicksNets": "Knicks Nets",
                                           "LakersClippers": "Lakers Clippers"})
    cities["NBA"] = cities["NBA"].apply(lambda x: x.split())
    cities = cities.explode("NBA")

    nba_df = nba_df[nba_df["year"] == 2018]
    nba_df = nba_df[["team","W","L","year"]]
    nba_df["team"].replace("[\*\(].*\)$","",inplace=True,regex=True)
    nba_df["team"] = nba_df["team"].str.strip()
    nba_df["team"] = nba_df["team"].apply(lambda s: s.split()[-1]) # get rid of city names
    nba_df = nba_df.astype({"W":"int64","L":"int64"})
    nba_df['W/L'] = nba_df['W']/(nba_df['W']+nba_df['L'])

    df = pd.merge(cities,nba_df,how='left',left_on="NBA",right_on="team").dropna()
    df = df.groupby('Population',sort=False).agg({"W/L":np.nanmean}).reset_index()
    df['Population'] = df['Population'].astype('float64')

    population_by_region = df['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = df['W/L'] # pass in win/loss ratio from nba_df

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nba_correlation()


# In[ ]:





# ## Question 3
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **MLB** using **2018** data.

# In[3]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def mlb_correlation(): 
    # YOUR CODE HERE
    mlb_df=pd.read_csv("assets/mlb.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    cities.rename(columns = {"Population (2016 est.)[8]":"Population"},inplace=True)
    cities.replace(regex='\[.*\]', value='',inplace=True)
    cities = cities[['Metropolitan area','Population','MLB']]
    cities["MLB"] = cities["MLB"].replace({"DodgersAngels": "Dodgers Angels", 
                                               "GiantsAthletics": "Giants Athletics", 
                                               "YankeesMets": "Yankees Mets",
                                               "Red Sox": "RedSox",
                                               "CubsWhite Sox": "Cubs WhiteSox",
                                               "Blue Jays": "BlueJays"})
    cities["MLB"] = cities["MLB"].apply(lambda x: x.split())
    cities = cities.explode("MLB")

    mlb_df = mlb_df[mlb_df["year"] == 2018]
    mlb_df = mlb_df[["team","W","L","year"]]
    mlb_df['team'] = mlb_df['team'].replace({"Boston Red Sox": "RedSox",
                                             "Chicago White Sox": "WhiteSox",
                                             "Toronto Blue Jays": "BlueJays"})
    mlb_df["team"] = mlb_df["team"].apply(lambda s: s.split()[-1]) # get rid of city names
    mlb_df = mlb_df.astype({"W":"int64","L":"int64"})
    mlb_df['W/L'] = mlb_df['W']/(mlb_df['W']+mlb_df['L'])

    df = pd.merge(cities,mlb_df,how='left',left_on="MLB",right_on="team").dropna()
    df = df.groupby('Population',sort=False).agg({"W/L":np.nanmean}).reset_index()
    df['Population'] = df['Population'].astype('float64')

    population_by_region = df['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = df['W/L'] # pass in win/loss ratio from mlb_df
    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
mlb_correlation()


# In[ ]:





# ## Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NFL** using **2018** data.

# In[4]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def nfl_correlation(): 
    # YOUR CODE HERE
    nfl_df=pd.read_csv("assets/nfl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    # clean up cities
    cities.rename(columns = {"Population (2016 est.)[8]":"Population"},inplace=True)
    cities.replace(regex='\[.*\]', value='',inplace=True)
    cities = cities[['Metropolitan area','Population','NFL']]
    cities["NFL"] = cities["NFL"].replace({"49ersRaiders": "49ers Raiders", 
                                               "GiantsJets": "Giants Jets", 
                                               "RamsChargers": "Rams Chargers"})
    cities['NFL'] = cities['NFL'].apply(lambda s: s.split())
    cities = cities.explode("NFL")  
    # clean up nfl_df
    nfl_df = nfl_df[nfl_df['year']==2018]
    nfl_df = nfl_df[["team","W","L","year"]]
    nfl_df = nfl_df.drop([0,5,10,15,20,25,30,35])   
    nfl_df['team'].replace("[\*\+]$","",inplace=True,regex=True)
    nfl_df['team'] = nfl_df['team'].apply(lambda s:s.split()[-1]) # get rid of city names
    nfl_df = nfl_df.astype({"W":"int64","L":"int64"})
    nfl_df['W/L'] = nfl_df['W']/(nfl_df['W']+nfl_df['L'])
    # merge two dataframes
    df = pd.merge(cities,nfl_df,left_on="NFL",right_on="team").dropna()
    df = df.groupby('Population',sort=False).agg({"W/L":np.nanmean}).reset_index()
    df['Population'] = df['Population'].astype('float64')
    population_by_region = df['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = df['W/L'] # pass in win/loss ratio from nfl_df

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nfl_correlation()


# In[ ]:





# ## Question 5
# In this question I would like you to explore the hypothesis that **given that an area has two sports teams in different sports, those teams will perform the same within their respective sports**. How I would like to see this explored is with a series of paired t-tests (so use [`ttest_rel`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html)) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.

# In[5]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def sports_team_performance():
    # YOUR CODE HERE
    raise NotImplementedError()
    
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
    
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values


# In[ ]:




