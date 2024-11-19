import pandas as pd
import json

"""
    ASSIGNMENT 1 (STUDENT VERSION):
    Using pandas to explore youtube trending data from GB (GBvideos.csv and GB_category_id.json) and answer the questions.
"""

csv_path = '/data/GBvideos.csv'
json_path = '/data/GB_category_id.json'

# csv_path = 'USvideos.csv'
# json_path = 'US_category_id.json'

vdo_df = pd.read_csv(csv_path)
df_category = pd.read_json(json_path)

def Q1():
    """
        1. How many rows are there in the GBvideos.csv after removing duplications?
        - To access 'GBvideos.csv', use the path '/data/GBvideos.csv'.
    """
    # TODO: Paste your code here
    df_video = pd.read_csv(csv_path)
    new_df_video = df_video.drop_duplicates()
    return int(new_df_video.shape[0])

def Q2(vdo_df):
    '''
        2. How many VDO that have "dislikes" more than "likes"? Make sure that you count only unique title!
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
    '''
    # TODO: Paste your code here
    vdo_df=pd.DataFrame(vdo_df)
    new_df_video = vdo_df.drop_duplicates()
    dislikemore = new_df_video[new_df_video['dislikes'] > new_df_video['likes']]
    unique_videos_count = dislikemore['title'].unique()
    #print(unique_videos_count.shape[0])
    return unique_videos_count.shape[0]

def Q3(vdo_df):
    '''
        3. How many VDO that are trending on 22 Jan 2018 with comments more than 10,000 comments?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
            - The trending date of vdo_df is represented as 'YY.DD.MM'. For example, January 22, 2018, is represented as '18.22.01'.
    '''
    # TODO: Paste your code here
    vdo_df=pd.DataFrame(vdo_df)
    vdo_df['trending_date']=pd.to_datetime(vdo_df['trending_date'], format='%y.%d.%m')
    vdo_df=vdo_df[ (vdo_df['comment_count']>1e4) & (vdo_df['trending_date'] == pd.to_datetime('2018-01-22'))]
    #print(vdo_df.shape[0])
    return vdo_df.shape[0]

def Q4(vdo_df):
    '''
        4. Which trending date that has the minimum average number of comments per VDO?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
    '''
    # TODO:  Paste your code here
    vdo_df=pd.DataFrame(vdo_df)
    vdo_df['trending_date']=pd.to_datetime(vdo_df['trending_date'], format='%y.%d.%m')
    mean_df=vdo_df.groupby('trending_date')['comment_count'].mean()
    sort_df=mean_df.sort_values()
    answer=sort_df.index[0]

    return answer.strftime('%y.%d.%m')

def Q5(vdo_df):
    '''
        5. Compare "Sports" and "Comedy", how many days that there are more total daily views of VDO in "Sports" category than in "Comedy" category?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
            - You must load the additional data from 'GB_category_id.json' into memory before executing any operations.
            - To access 'GB_category_id.json', use the path '/data/GB_category_id.json'.
    '''
    # TODO:  Paste your code here
    vdo_df=pd.DataFrame(vdo_df)
    df_category = pd.read_json(json_path)
    lists = df_category['items']

    # Find the id of the comedy and sports
    Comedy_id = 0
    Sports_id = 0
    for i in lists:
        if( (i['snippet']['title'] == 'Comedy') & (i['snippet']['assignable'] == True) ):
            Comedy_id = int(i['id'])
        if( (i['snippet']['title'] == 'Sports') & (i['snippet']['assignable'] == True) ):
            Sports_id = int(i['id'])

    # running to find the data
    new_df = vdo_df[ (vdo_df['category_id'] == int(Comedy_id)) | (vdo_df['category_id'] == int(Sports_id)) ]
    new_df = new_df.groupby(['trending_date','category_id'])['views'].sum().reset_index()
    transform_df = new_df.pivot(index='trending_date', columns='category_id', values='views')
    answer = transform_df[transform_df[Sports_id] > transform_df[Comedy_id]]
    return answer.shape[0]

user_input = input()
if user_input == 'Q1':
    Q1()
elif user_input == 'Q2':
    Q2(vdo_df)
elif user_input == 'Q3':
    Q3(vdo_df)
elif user_input == 'Q4':
    Q4(vdo_df)
elif user_input == 'Q5':
    Q5(vdo_df)