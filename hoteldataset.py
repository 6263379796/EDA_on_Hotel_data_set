#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[3]:


hotel_data = pd.read_csv('hotel_bookings.csv')
hotel_data.head()


# In[4]:


pwd


# In[5]:


hotel_data.shape


# In[6]:


hotel_data.info()


# In[7]:


hotel_data.describe()


# In[8]:


hotel_data.isnull().sum()


# In[9]:


#Dropping Company Column because more than 90% of data is missing
hotel_data.drop('company', inplace=True, axis=1)
hotel_data.drop('arrival_date_week_number',inplace=True,axis=1)


# In[10]:


hotel_data.head(7)


# In[11]:


hotel_data.shape


# In[12]:


#Filling children and agent missing values with median values
def impute_median(series):
    return series.fillna(series.median())


# In[13]:


hotel_data.children = hotel_data['children'].transform(impute_median)
hotel_data.agent = hotel_data['agent'].transform(impute_median)


# In[14]:


hotel_data.isnull().sum()


# In[15]:


#Filling country missing values with mode

print(hotel_data['country'].mode())
hotel_data['country'].fillna(str(hotel_data['country'].mode().values[0]),inplace=True)


# In[16]:


hotel_data.isnull().sum()


# In[17]:


#We will try to answer the following questions:
#What type of hotel has more bookings?
#Which are the most busy months?
#Cancellation rates in the two types of hotels.
#Total Num of Confirmed Bookings as per year


# In[18]:


# Enlarging the pie chart
plt.rcParams['figure.figsize'] = 10,10
print(set(hotel_data['hotel']))
# assigning labels and converting them to list 
labels = hotel_data['hotel'].value_counts().index.tolist()
print(labels)
# assigning magnitude and converting to list
sizes = hotel_data['hotel'].value_counts().tolist()
print(sizes)
# assigning pie chart color
colors = ["darkorange","lightskyblue"]

## We have only 2 sections so anglestart does not matter
# textprops will adjust the size of text
plt.pie(sizes,labels=labels,colors=colors,autopct='%1.1f%%',startangle=90, textprops={'fontsize': 14})


# In[19]:


type(hotel_data)


# In[20]:


#2. Which are the most busy months?


# In[21]:


# Useing a countplot as we are visualising categorical data
plt.figure(figsize=(20,10))


l1 = ['hotel','arrival_date_month']
 
#plotting

sns.countplot(data= hotel_data[l1],x= "arrival_date_month",hue="hotel",order=["January","February","March","April","May","June","July","August","September","October","November","December"]).set_title(
'Illustration of Number of Visitors Each Month')
plt.xlabel('Month')
plt.ylabel('Count')


# In[22]:


#so here we can clearly see that august is the busiest month for both Resort hotal and city hotel


# In[23]:


#🏨 Cancellation rates in the two types of hotels.


# In[24]:


print(set(hotel_data['is_canceled']))


# In[25]:


#so here we can see that we have two values in is_canceled '0' & '1' as they denoting "Cancelled" & "Not Cancelled"


# In[26]:


## Replacing the 1s and 0s in the is_cancelled column to cancelled and not cancelled. 
hotel_data['is_canceled'] = hotel_data.is_canceled.replace([1,0],["Cancelled","Not Cancelled"])
cancelled_data = hotel_data['is_canceled']

# Plotting a countplot
sns.countplot(cancelled_data).set_title("Cancellation Overview")
plt.xlabel("Bookings Cancelled")


# In[27]:


# cancelled is seen to be more than 50 % which is bad sign but also a constant fair with hotel industry 


# In[28]:


lst1 = ['is_canceled', 'hotel']
type_of_hotel_canceled = hotel_data[lst1]
canceled_hotel = type_of_hotel_canceled[type_of_hotel_canceled['is_canceled'] == 'Cancelled'].groupby(['hotel']).size().reset_index(name = 'count')
canceled_hotel


# In[29]:


hotel_data['arrival_date_year'].unique()


# In[30]:


confirmed_booking = hotel_data[hotel_data.is_canceled=='0']


# In[31]:


confirmed_booking['arrival_date_year'] = hotel_data['arrival_date_year']
Last=confirmed_booking['arrival_date_year'].value_counts().sort_index()
Last


# In[32]:


#Cancelled Booking


# In[33]:


hotel_data['is_canceled'].value_counts()


# In[34]:


#How many bookings confirmed in both the hotels Year and month wise is as follows
hotel_data.groupby(["hotel","arrival_date_year"])["arrival_date_month"].value_counts()


# In[60]:


hotel_data.head(54)


# In[36]:


#Types of visitors? (No. of adults, children, babies)
sns.countplot(data=hotel_data,x='adults',hue='hotel').set_title("Illustration of number of adults visiting each hotel")


# In[37]:


sns.countplot(data=hotel_data,x='children',hue='hotel').set_title("Illustration of number of adults visiting each hotel")


# In[38]:


plt.pie(hotel_data['required_car_parking_spaces'].value_counts(),
        explode=[0.05]*5,
        shadow=True,
        autopct='%1.1f%%',
        labels=None)

labels=hotel_data['required_car_parking_spaces'].value_counts().index
plt.title('% Distribution of required car parking spaces')
plt.legend(bbox_to_anchor=(0.85, 1), loc='upper left', labels=labels)
plt.show()


# In[ ]:


# satatistic of no of booking changes made by a guest


# In[40]:


booking_changes_df = hotel_data['booking_changes'].value_counts().reset_index().rename(columns={'index':'number_booking_changes', 'booking_changes':'count'})
plt.figure(figsize=(12, 8))
sns.barplot(x=booking_changes_df['number_booking_changes'], y=booking_changes_df['count']*100/hotel_data.shape[0])
plt.title("% of booking changes")
plt.xlabel("Number of booking changes")
plt.ylabel("Percentage(%)")
plt.show()


# In[ ]:


#Almost 85% of the bookings were not changed by guests.


# In[48]:


#Now we will find a percentage of type of deposit made by a Guest
xty=set(hotel_data['deposit_type'])
print(xty)


# In[49]:


# so now we know that their are three types of deposit in our data frame i.e 
#1. No Deposit
#2. Refundable
#3. Non Refund


# In[52]:


plt.pie(hotel_data['deposit_type'].value_counts(),
        explode=(0.05, 0.05,0.05),
        shadow=True,
        autopct='%1.1f%%')
plt.title("% Distribution of deposit type")
labels=hotel_data['deposit_type'].value_counts().index.tolist()
plt.legend(bbox_to_anchor=(0.9, 1), loc='upper left', labels=labels)
plt.show()


# In[53]:


# 87.6% of guests prefer "No deposit" type of deposit.
# 0.1% of guest prefer "Refundable" type of deposit.
# 12.2% of guest prefer "Non refund" type of deposit 


# In[54]:


#which year has the most number of booking made by a guest
xttyx= set(hotel_data['arrival_date_year'])
print(xttyx)


# In[56]:


plt.figure(figsize=(12, 8))
sns.countplot(x=hotel_data['arrival_date_year'], hue=hotel_data['hotel'])
plt.title('Year Wise Bookings')
plt.ylabel('Bookings')


# In[58]:


plt.figure(figsize=(18, 10))
sns.heatmap(hotel_data.corr(), annot=True)
plt.title('Co-relation of columns')


# In[66]:


#adr : Average Daily Rate as defined by dividing the sum of all lodging transactions by the total number of staying nights


# In[ ]:


# ADR across the different month!


# In[69]:


bookings_by_month_df = hotel_data.groupby(['arrival_date_month', 'hotel'])['adr'].mean().reset_index()
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

bookings_by_month_df['arrival_date_month'] = pd.Categorical(bookings_by_month_df['arrival_date_month'],
                                                            categories = months, 
                                                            ordered=True)

bookings_by_month_df = bookings_by_month_df.sort_values('arrival_date_month')
print(bookings_by_month_df)


# In[65]:


plt.figure(figsize=(20, 8))
sns.lineplot(x=bookings_by_month_df['arrival_date_month'], 
             y=bookings_by_month_df['adr'], 
             hue=bookings_by_month_df['hotel'])

plt.title('ADR across each month')
plt.xlabel('Month')
plt.ylabel('ADR')


# In[70]:


hotel_data.head(10)


# In[ ]:




