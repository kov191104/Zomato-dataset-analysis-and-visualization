#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[3]:


df = pd.read_csv(r'C:\Users\Kovarthana\Downloads\zomato.csv', nrows=20000)
df.head()


# In[4]:


df.info()


# In[5]:


df.shape


# In[6]:


df.columns


# ## DROPING OF COLUMNS

# In[7]:


df=df.drop(['url','address','phone','menu_item','dish_liked','reviews_list'], axis=1)
df.head()


# In[8]:


df.info()


# ## DROPPING DUPLICATES

# In[9]:


df.drop_duplicates(inplace=True)
df.shape


# ## CLEANING RATE COLUMN

# In[10]:


df['rate'].unique()


# In[11]:


def handlerate(value):
    if(value=='NEW'or value=='-'):
        return np.nan
    else:
        value=str(value).split('/')
        value=value[0]
        return float(value)
df['rate']=df['rate'].apply(handlerate)
df['rate'].head()


# ## FILLING NULL VALUE IN RATE COLUMN WITH MEAN

# In[12]:


df['rate'].fillna(df['rate'].mean(),inplace= True)
df['rate'].isnull().sum()


# ## DROPPING NULL VALUES

# In[14]:


df.dropna(inplace=True)
df.head()


# In[26]:


df.rename(columns={'approx_cost(for two people)':'cost of 2ppl','listed_in(type)':'type'},inplace=True)
df.head()


# In[17]:


df['location'].unique()


# ## DROPPING listed_in(city) COLUMN

# In[ ]:


df = df.drop(['listed_in(city)'],axis=1)


# In[31]:


df.head()


# In[39]:


df['cost of 2ppl'].unique()


# In[38]:


def handlecomma(value):
    value=str(value)
    if ',' in value:
        value=value.replace(',' , '')
        return float(value)
    else:
        return float(value)

df['cost of 2ppl']=df['cost of 2ppl'].apply(handlecomma)
df['cost of 2ppl'].unique()


# In[43]:


df.tail()


# ## CLEANING REST TYPE COLUMN

# In[44]:


df['rest_type'].value_counts()


# In[46]:


rest_types=df['rest_type'].value_counts(ascending = True)
rest_types


# ## CLUSTERING VALUES LESS THAN 1000 

# In[47]:


restTypes_LT_1000=rest_types[rest_types<1000]
restTypes_LT_1000


# ### MAKING REST TYPES <1000 IN FREQUENCY AS OTHERS 

# In[48]:


def handle_restTypes(value):
    if(value in restTypes_LT_1000):
        return 'other'
    else:
        return value

df['rest_type']=df['rest_type'].apply(handle_restTypes)
df['rest_type'].value_counts()
    


# ## CLEANING LOCATION COLUMN

# In[49]:


location=df['location'].value_counts(ascending = True)
location


# In[58]:


location_LT_200=location[location<200]


def handle_location(value):
    if(value in location_LT_200):
        return 'other'
    else:
        return value

df['location']=df['location'].apply(handle_location)
df['location'].value_counts()
    


# In[52]:


df.head()


# ## CLEANING CUISINES COLUMN 

# In[53]:


df['cuisines'].unique()


# In[54]:


cuisines=df['cuisines'].value_counts(ascending = True)

cuisines_LT_100=cuisines[cuisines<100]


def handle_cuisines(value):
    if(value in cuisines_LT_100):
        return 'other'
    else:
        return value

df['cuisines']=df['cuisines'].apply(handle_cuisines)
df['cuisines'].value_counts()


# In[56]:


df['type'].value_counts()


# # VISUALIZATION

# ## COUNT PLOT FOR VARIOUS LOCATIONS

# In[67]:


plt.figure(figsize=(16,10))
ax = sns.countplot(data=df, x='location', order = df['location'].value_counts().index)
plt.xticks(rotation=55)


# ## VISUALIZING ONLINE ORDERS

# In[97]:


plt.figure(figsize=(10,10))
pl = sns.color_palette("Purples")
sns.countplot(data=df,x='online_order',order=df['online_order'].value_counts().index,palette=pl)


# ## VISUALIZING BOOK TABLE

# In[103]:


plt.figure(figsize=(10,10))
pl = sns.color_palette("Blues")
sns.countplot(data=df,x='book_table',order=df['book_table'].value_counts().index,palette =pl)


# ## VISUALIZING ONLINE ORDER VS RATE

# In[101]:


plt.figure(figsize=(10,10))
sns.boxplot(x='online_order',y='rate',data=df)


# ## VISUALIZING BOOK TABLE VS RATE

# In[104]:


plt.figure(figsize=(10,10))
sns.boxplot(x='book_table',y='rate',data=df)


# ### VISUALIZING ONLINE ORDER FACILITY ,LOCATION WISE

# In[105]:


df1 = df.groupby(['location','online_order'])['name'].count()
df1.to_csv('location_online.csv')
df1 = pd.read_csv('location_online.csv')
df1 = pd.pivot_table(df1, values=None, index=['location'], columns=['online_order'], fill_value=0, aggfunc=np.sum)
df1


# In[107]:


df1.plot(kind = 'bar', figsize = (15,10))


# In[111]:


df2 = df.groupby(['location','book_table'])['name'].count()
df2.to_csv('location_bookTable.csv')
df2 = pd.read_csv('location_bookTable.csv')
df2 = pd.pivot_table(df2, values=None, index=['location'], columns=['book_table'], fill_value=0, aggfunc=np.sum)
df2



# In[113]:


df2.plot(kind = 'bar', figsize = (15,10))


# ### VISUALIZING TYPES OF RESTAURANTS VS RATE

# In[114]:


plt.figure(figsize=(10,10))
sns.boxplot(x='type',y='rate',data=df)


# ## GROUPING TYPES OF RESTAURENTS, LOCATION WISE

# In[115]:


df3 = df.groupby(['location','type'])['name'].count()
df3.to_csv('location_type.csv')
df3 = pd.read_csv('location_type.csv')
df3 = pd.pivot_table(df3, values=None, index=['location'], columns=['type'], fill_value=0, aggfunc=np.sum)
df3


# In[122]:


df3.plot(kind = 'bar', figsize = (25,8))


# ## NO. OF VOTES,LOCATION WISE

# In[128]:


df4 = df[['location', 'votes']]
df4.drop_duplicates()
df5 = df4.groupby(['location'])['votes'].sum()
df5 = df5.to_frame()
df5 = df5.sort_values('votes', ascending=False)
df5.head()


# In[125]:


plt.figure(figsize=(15, 8))
sns.barplot(x=df5.index, y=df5['votes'])
plt.xticks(rotation=90)
plt.show()


# ## Visualizing Top Cuisines

# In[129]:


df6 = df[['cuisines', 'votes']]
df6.drop_duplicates()
df7 = df6.groupby(['cuisines'])['votes'].sum()
df7 = df7.to_frame()
df7 = df7.sort_values('votes', ascending=False)
df7.head()


# In[130]:


#iloc-to remove the others and plot everything
df7 = df7.iloc[1:, :]
df7.head()


# In[133]:


plt.figure(figsize=(15, 8))
sns.barplot(x=df7.index, y=df7['votes'])
plt.xticks(rotation=90)
plt.show()


# In[ ]:




