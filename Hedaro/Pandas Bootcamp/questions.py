# imports
import pandas as pd
from numpy import random

# logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Without this the html links get truncated....wak
pd.set_option("display.max_colwidth",100000)

###############################################################################
###############################################################################

def pd_create_dataset(seed=None):
    """ make sample data """
    
    if seed==None:
        seed = random.randint(low=0,high=1000)
    random.seed(seed)
    
    pool1 = ['boy', 'girl']
    pool2 = ['blue','red','green','yellow','purple']
    pool3 = pd.date_range('1/1/2014', periods=1000)
    
    d = {'num':[random.randint(low=0,high=1000) for i in range(50)],
         'num2':[random.randint(low=0,high=1000) + random.sample() for i in range(50)],
         'str':[pool1[random.randint(low=0,high=len(pool1))] for i in range(50)],
         'str2':[pool2[random.randint(low=0,high=len(pool2))] for i in range(50)],
         'date':[pool3[random.randint(low=0,high=len(pool3))] for i in range(50)]}

    df = pd.DataFrame(d)

    return seed, df
    
def pd_create_table(seed, df):
    """ get avg of df """
    df['seed'] = seed
    return df.drop(labels=['seed'], axis=1).to_html(index=False,escape=False, classes=['table table-condensed table-striped table-hover'])    
    
def pd_create_questions(df):
    """ get avg of df """

    # q1
    #################
    q1_str = r'What is the average of column num?'
    q1 = df['num'].mean()
    
    #q2
    #################
    q2_str = r'What is the average of column num2?'
    q2 = df['num2'].mean()
    
    #q3
    #################
    q3_str = r'Group by str and find the sum of column num where the index is boy.'
    group = df.groupby('str').sum()
    q3 = group['num'].loc['boy']
    
    #q4
    #################
    q4_str = r'Find the row with the smallest date. Subtract num - num2.'
    # get smallest date
    mask = df['date'] == df['date'].min()

    #subtract num - num2
    ans = df['num'][mask] - df['num2'][mask]
    q4 = ans.values
    
    #q5
    #################
    q5_str = r'Find the least popular string in column str2. Filter by str2 where the string equals the least popular string. Find the sum of column num.'    
    # find least popular str2
    leastpop = pd.DataFrame(df['str2'].value_counts()).sort(columns=0).head(1).index.values

    # filter least popular string
    mask = df['str2'].apply(lambda x: x in leastpop)
    q5 = df['num'][mask].sum()
    
    #q6
    #################
    q6_str = r'Create a new column called "Letter". This column is the sum of the lengths of columns str and str2. Then divide the column num by Letter. Pick the second smallest number.'   

    # add len of str and str2
    df['letter'] = df['str'].apply(lambda x: len(x)) + df['str2'].apply(lambda x: len(x))

    # divide num by letter
    ans = df['num'].div(df['letter'])

    # pick second smallest number
    q6 = ans.order().head(2).max()  

    #q7
    #################
    q7_str = r'Create a new column called "diff". This column returns 1 if column num > column num2 and 0 if it does not. What is the sum of column diff?'   

    # is num greater than num2
    df['diff'] = df.apply(lambda x: 1 if x['num'] > x['num2'] else 0, axis=1)
    q7 = df['diff'].sum()    
    
    # q8
    #################
    q8_str = r'What is the maximum of column num?'
    q8 = df['num'].max()    
    
    
    ############################################################################################    
    ############################################################################################ 
    q = pd.DataFrame({'question':[q1_str,q2_str,q3_str,q4_str,q5_str,q6_str,q7_str,q8_str],
                      'ans':[q1,q2,q3,q4,q5,q6,q7,q8]})

    q['id'] = q.index

    return q    
   
    


      