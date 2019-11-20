import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def question_1(need_print = True):
    if need_print:
        print("--------------- question_1 ---------------")
        
    olympics1_df = pd.read_csv('Olympics_dataset1.csv', skiprows = 1)
    olympics2_df = pd.read_csv('Olympics_dataset2.csv', skiprows = 1)
    olympics1_df.rename(columns = {olympics1_df.columns[0]:'Country'}, inplace = True)
    olympics2_df.rename(columns = {olympics2_df.columns[0]:'Country'}, inplace = True)

    df = pd.merge(olympics1_df, olympics2_df, how = 'right', left_on = ['Country'], right_on = ['Country'])
    df.drop(df.columns[12:], inplace = True, axis = 1)
    df.columns = ['Country', 'summer_rubbish', 'summer_participation', 'summer_gold', \
                  'summer_silver', 'summer_bronze','summer_total', 'winter_ participation', \
                  'winter_gold', 'winter_silver', 'winter_bronze', 'winter_total']
    df.drop(df.index[-1],inplace = True)
    
    if need_print:
        print(df.head(5).to_string())
    write_in_csv(df, 'question_1.csv')
    return df


def question_2(need_print = True):
    if need_print:
        print("--------------- question_2 ---------------")
    df = question_1(need_print = False)
    
    df['Country'] = df['Country'].str.replace(r"\([^\)]*\)", "")
    df['Country'] = df['Country'].str.replace(r"\[[^\]]*\]", "")
    clean_data = df['Country'].str.strip()
    df['Country'] = clean_data
    
    df.set_index('Country', inplace = True)
    columns_to_drop = ['summer_rubbish', 'summer_total' , 'winter_total']
    df.drop(columns_to_drop, inplace=True, axis=1)
    
    if need_print:
        print(df.head(5).to_string())
    write_in_csv(df, 'question_2.csv')
    return df

def question_3(need_print = True):
    if need_print:
        print("--------------- question_3 ---------------")
    df = question_2(need_print = False)

    df = df.dropna()
    if need_print:
        print(df.tail(10).to_string())      
    write_in_csv(df, 'question_3.csv')
    
    return df

def question_4():
    df = question_3(need_print = False)
    
    print("--------------- question_4 ---------------")
    df['summer_gold'] = df['summer_gold'].str.replace(',', '')
    df['summer_gold'] = to_numeric(df, 'summer_gold')
    print(df['summer_gold'].idxmax())
        
def question_5():
    df = question_3(need_print = False)
    print("--------------- question_5 ---------------")
    df['summer_gold'] = df['summer_gold'].str.replace(',', '')
    df['summer_gold'] = to_numeric(df, 'summer_gold')
    df['winter_gold'] = to_numeric(df, 'winter_gold')
    print((df['summer_gold'] - df['winter_gold']).abs().idxmax(),end = '')
    print(', ',end = '')
    print((df['summer_gold'] - df['winter_gold']).abs().max())

    
def question_6():
    df = question_3(need_print = False)
    print("--------------- question_6 ---------------")
    df['summer_gold'] = df['summer_gold'].str.replace(',', '')
    df['total_number_of_medals'] =to_numeric(df, 'summer_gold') + to_numeric(df, 'summer_silver') + to_numeric(df, 'summer_bronze') +\
                                   to_numeric(df, 'winter_gold') + to_numeric(df, 'winter_silver') +  to_numeric(df, 'winter_bronze')

    df = df.sort_values('total_number_of_medals',ascending=False)
    print(df.head(5).loc[:,['total_number_of_medals']].to_string())
    print(df.tail(5).loc[:,['total_number_of_medals']].to_string())
    ##print(pd.concat([df.head(5), df.tail(5)]).to_string())

def question_7():
    df = question_3(need_print = False)
    print("--------------- question_7 ---------------")
    df['summer_gold'] = df['summer_gold'].str.replace(',', '')

    df['total_number_of_medals'] =to_numeric(df, 'summer_gold') + to_numeric(df, 'summer_silver') + to_numeric(df, 'summer_bronze') +\
                                   to_numeric(df, 'winter_gold') + to_numeric(df, 'winter_silver') +  to_numeric(df, 'winter_bronze')
    df['Summer games'] = to_numeric(df, 'summer_gold') + to_numeric(df, 'summer_silver') + to_numeric(df, 'summer_bronze')
    df['Winter games'] = to_numeric(df, 'winter_gold') + to_numeric(df, 'winter_silver') +  to_numeric(df, 'winter_bronze')
    df = df.sort_values('total_number_of_medals',ascending=False)
    ##df = df.swapaxes('index', 'columns')

    df.head(10).sort_values('total_number_of_medals')[['Summer games', 'Winter games']].plot.barh(stacked=True)
    plt.title('Medals for Winter and Summer Games')
    plt.show()

def question_8():
    df = question_3(need_print = False)
    print("--------------- question_8 ---------------")
    df['summer_gold'] = df['summer_gold'].str.replace(',', '')

    df['Gold'] = to_numeric(df,'winter_gold')
    df['Silver'] = to_numeric(df,'winter_silver')
    df['Bronze'] = to_numeric(df,'winter_bronze')
    df = df.loc[['United States','Australia','Great Britain','Japan','New Zealand'], ['Gold','Silver','Bronze']]
    df.plot.bar(rot = 0)
    plt.title('Winter Games')
    plt.show()

def question_9():
    df = question_3(need_print = False)
    df['summer_gold'] = df['summer_gold'].str.replace(',', '')
    print("--------------- question_9 ---------------")
    df['rate'] = (to_numeric(df, 'summer_gold')*5 + to_numeric(df, 'summer_silver')*3 + \
                          to_numeric(df, 'summer_bronze')*1)/ to_numeric(df,'summer_participation')
    df = df.sort_values('rate',ascending=False)
    df = df.head()
    country = df.index.tolist()
    rate = df['rate'].tolist()
    for i in range(5):
        print('({0}, {1})'.format(country[i],rate[i]))
    
    
def question_10():
    df = question_3(need_print = False)
    df['summer_gold'] = df['summer_gold'].str.replace(',', '')
    continent_df = pd.read_csv('Countries-Continents.csv')
    print("--------------- question_10 ---------------")
    df['points per participation for summer games'] = (to_numeric(df, 'summer_gold')*5 + to_numeric(df, 'summer_silver')*3 + \
                          to_numeric(df, 'summer_bronze')*1)/ to_numeric(df,'summer_participation')
    df['points per participation for winter games'] = (to_numeric(df, 'winter_gold')*5 + to_numeric(df, 'winter_silver')*3 + \
                          to_numeric(df, 'winter_bronze')*1)/ to_numeric(df,'winter_ participation')

    
    df.fillna(0, inplace = True)
    df = pd.merge(df, continent_df, how='left', left_on=['Country'], right_on=['Country'])
    df.set_index('Country', inplace = True)
    df.replace(to_replace=[None], value='Unknown', inplace=True)

    df = change_color(df)
    write_in_csv(df,'question_10.csv')
    ax = df.plot.scatter(x = 'points per participation for summer games', y = 'points per participation for winter games', \
                         c = df['Color'])
    
    
    for i, txt in enumerate(df.index):
        ax.annotate(txt, (df.loc[txt]['points per participation for summer games'], df.loc[txt]['points per participation for winter games']))

    
    plt.show()

def change_color(df):
    color = np.zeros(df.shape[0])
    new_color = ["%.2f" % number for number in color]
    df_change = df
    
    for x in range(len(df_change['Continent'])):
        if df_change['Continent'][x] == 'Unknown':
            new_color[x] = 'gray'
        elif df_change['Continent'][x] == 'Africa':
            new_color[x] = 'black'
        elif df_change['Continent'][x] == 'Asia':
            new_color[x] = 'white'
        elif df_change['Continent'][x] == 'Europe':
            new_color[x] = 'green'
        elif df_change['Continent'][x] == 'North America':
            new_color[x] = 'yellow'
        elif df_change['Continent'][x] == 'Oceania':
            new_color[x] = 'purple'
        elif df_change['Continent'][x] == 'South America':
            new_color[x] = 'brown'
    df.insert(df.shape[1]-1,'Color',new_color)
    return df_change

    

def to_numeric(dateframe, column_name):
    return pd.to_numeric(dateframe[column_name])
          
def write_in_csv(dataframe, file):

    dataframe.to_csv(file, sep=',', encoding='utf-8',index = False)
    

if __name__ == "__main__":
    question_1()
    question_2()
    question_3()
    question_4()
    question_5()
    question_6()
    question_7()
    question_8()
    question_9()
    question_10()
