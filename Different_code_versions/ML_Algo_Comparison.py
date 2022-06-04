import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

dataset = pd.read_csv('Crimes_2001_to_Present (1).csv',low_memory=False)
dataset.head(10)
# dataset.dtypes

# droping the features that are not usefull
dataset=dataset.drop(columns=['ID','Case Number','Description','Updated On','Block'])
# X.shape
print('Columns in dataset: ', dataset.columns)
dataset.shape

# droping the null value enteries
dataset.dropna(inplace=True)
dataset

# ignore latitude and logitude outside of the chicago
dataset=dataset[(dataset["Latitude"] < 45)
             & (dataset["Latitude"] > 40)
             & (dataset["Longitude"] < -85)
             & (dataset["Longitude"] > -90)]
dataset

# # listing the crimes category wise with their counts
types=dataset['Primary Type'].value_counts().sort_values(ascending=False)
types

# crime types according to their counts in dataframe
# 15 classes
# major_crimes=['THEFT','BATTERY','CRIMINAL DAMAGE','ASSAULT','OTHER OFFENSE','DECEPTIVE PRACTICE','NARCOTICS','BURGLARY','MOTOR VEHICLE THEFT'
#               ,'ROBBERY','CRIMINAL TRESPASS','WEAPONS VIOLATION','OFFENSE INVOLVING CHILDREN','PUBLIC PEACE VIOLATION','CRIM SEXUAL ASSAULT']
# 8 classes
# storing major crime types according to their counts in dataframe
# major_crimes=['THEFT','BATTERY','CRIMINAL DAMAGE','ASSAULT','OTHER OFFENSE','DECEPTIVE PRACTICE','NARCOTICS','BURGLARY']


#---> Storing Major Crimes
major_crimes=['THEFT','BATTERY','CRIMINAL DAMAGE','ASSAULT']

crime_df = dataset.loc[dataset['Primary Type'] .isin(major_crimes)]
crime_df

data = crime_df.pivot_table(index='Year', columns='Primary Type', aggfunc='count')
print(data)

# since we dont have different crimes in early years so we drop data of these years

# selecting the dataset which starts from 2015
crime_df=crime_df[crime_df['Year']>=2015]
crime_df

temp=crime_df.copy()
temp

# getting the half of our data set for random data selection
nrows= temp.shape[0]
portion=math.floor(nrows/3)
portion

first=temp.iloc[0:portion,:]
first

nextp=portion+portion+1
scnd=temp.iloc[(portion+1):nextp,:]
scnd

finalp=nextp+portion+1
third=temp.iloc[(nextp+1):finalp,:]
third

# picking random 5k enteries from the first part
index=np.random.choice(portion,replace=False,size = 30000)
df_frst=first.iloc[index]
df_frst

# picking random 5k enteries from the second half

index=np.random.choice(portion,replace=False,size = 30000)
df_scnd=scnd.iloc[index]
df_scnd

# picking random 5k enteries from the third half

index=np.random.choice(portion,replace=False,size = 30000)
df_third=third.iloc[index]
df_third

# combined all three dataframe

temp_df = pd.concat([df_frst,df_scnd],ignore_index=True)
final_df = pd.concat([temp_df,df_third],ignore_index=True)
final_df

df=final_df.copy()

# Using PCA to combine two features

from sklearn.decomposition import PCA

location = df[['Latitude','Longitude']]
pca = PCA(n_components=1,random_state=123)
locat = pca.fit_transform(location)
df['Location'] = locat
df.head(10)

# convertung date column to actual date format
df.Date=pd.to_datetime(df.Date)
df.head(10)

# extracting month and weekday from date column
df['month']=df.Date.dt.month
df['weekday'] = df.Date.dt.day_of_week
df=df.drop(columns='Date')
df

# elif t == 'OTHER OFFENSE': return '5'
    # elif t == 'DECEPTIVE PRACTICE': return '6'
    # elif t == 'NARCOTICS': return '7'
    # elif t == 'BURGLARY': return '8'
    # elif t == 'MOTOR VEHICLE THEFT': return '9'
    # elif t == 'ROBBERY': return '10'
    # elif t == 'CRIMINAL TRESPASS': return '11'
    # elif t == 'WEAPONS VIOLATION': return '12'
    # elif t == 'OFFENSE INVOLVING CHILDREN': return '13'
    # elif t == 'PUBLIC PEACE VIOLATION': return '14'
    # elif t == 'CRIM SEXUAL ASSAULT': return '15'
    
# assigning crimetype 
def crime_type(t):
    if t =='THEFT': return '1'
    elif t =='BATTERY': return '2'
    elif t =='CRIMINAL DAMAGE': return '3'
    elif t == 'ASSAULT': return '4'
    else: return '0'

cp_crime = df.copy()
cp_crime['crimeType'] = cp_crime['Primary Type'].map(crime_type)
cp_crime

labelEncoder = LabelEncoder()
locDes_enc = labelEncoder.fit_transform(cp_crime['Location Description'])
cp_crime['Location Description'] = locDes_enc
cp_crime.head()

labelEncoder2 = LabelEncoder()
arrest_enc = labelEncoder2.fit_transform(cp_crime['Arrest'])
cp_crime['Arrest'] = arrest_enc
cp_crime.head()

labelEncoder3 = LabelEncoder()
domestic_enc = labelEncoder3.fit_transform(cp_crime['Domestic'])
cp_crime['Domestic'] = domestic_enc
cp_crime.head()

# feature scaling
scaler = preprocessing.MinMaxScaler()
cp_crime[['Beat']] = scaler.fit_transform(cp_crime[['Beat']])
cp_crime[['X Coordinate', 'Y Coordinate']] = scaler.fit_transform(cp_crime[['X Coordinate', 'Y Coordinate']])
cp_crime

# using correlation for the feature selection
corelation = cp_crime.corr()
corelation

plt.figure(figsize=(10,7))
sns.heatmap(corelation,annot=True)

# month week day have low correlation they isn't effect our results so we drop them
# since beat have high correlation with district so we drop beat
# and X cordinate have high correlation with longitube and Y cordinate with latitude and location so we drop longitude and latitude

selected_cols=['Location Description','Arrest','Domestic','Beat','Ward','Community Area','Year','X Coordinate','Y Coordinate']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(cp_crime[selected_cols],cp_crime['crimeType'],test_size=0.2, random_state=0)

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(solver="saga", multi_class='ovr',max_iter=10000)
lr.fit(X_train, y_train)
print('Accuracy of Logistic Regression', lr.score(X_test, y_test))

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train,y_train)
print('Accuracy of Logistic Regression', gnb.score(X_test, y_test))

from sklearn.naive_bayes import CategoricalNB
cnb = CategoricalNB()
cnb.fit(X_train,y_train)
print('Accuracy of Logistic Regression', cnb.score(X_test, y_test))    

# knn = KNeighborsClassifier(n_neighbors = 10)
# knn.fit(X_train, y_train)
# predictions = knn.predict(X_test)
# print('Accuracy of KNN', knn.score(X_test, y_test))
# pred_train = knn.predict(X_train)
# pred_i = knn.predict(X_test)
# print('Test accuracy ', metrics.accuracy_score(y_train, pred_train))
# print('Accuracy ', metrics.accuracy_score(y_test, pred_i))








