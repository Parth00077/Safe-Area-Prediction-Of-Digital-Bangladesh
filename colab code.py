# -*- coding: utf-8 -*-
"""SAFE AREA PREDICTION: AN ANALYTICAL METHOD BY USING MACHINE LEARNING TECHNIQUES

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zKociRm7M-nXeXh16Q-Pw1MNzaJuMoRp

***********
***********

<center><h3><b>SAFE AREA PREDICTION: AN ANALYTICAL METHOD BY USING MACHINE LEARNING TECHNIQUES</b></h3></center>

***********
***********

<h5><b>Team  Members:</h5></b>

1. Protim Das (183-15-11849)
2. Mahid Ahmed Tonmoy (183-15-12041)

#### **Import all the necessary libraries**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.metrics import jaccard_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

"""#### **Import Dataset from google drive**"""

from google.colab import drive
drive.mount('/content/drive')

path ="/content/drive/MyDrive/Bangladesh Crime Rate/bangladesh crime data.csv"

df = pd.read_csv(path)



"""#### **Dataset Analysis**"""

df.shape

df.head()

df.isna().sum() #missing values

description = df.describe()
#description.to_csv (r'\Location.csv', index = False, header=True)
description

df.info()

"""#### **Initializing Feature name and Target feature Separately**"""

df = df[['Unit_Name','Year','Dacoity','Robbery','Murder','Speedy_Trial', 'Riot', 'W_&_C_Repression', 'Kidnapping', 'Police_Assault', 'Burglary', 'Theft', 'Other_Cases', 'Arms_Act', 'Explosive', 'Narcotics', 'Smuggling', 'Crime_Rate']]
df['Crime_Rate'] = df['Crime_Rate'].astype('int')
df.head(10)

"""#### **Dataset Frequency**"""

import matplotlib.pyplot as plt
import seaborn as sns
fig1, ax1 = plt.subplots()
ax1.pie(df["Crime_Rate"].value_counts(),  labels=['SAFE','UNSAFE'], autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.show()

"""#### **Features to predict**"""

X = np.asarray(df[['Unit_Name','Year','Dacoity','Robbery','Murder','Speedy_Trial', 'Riot', 'W_&_C_Repression', 'Kidnapping', 'Police_Assault', 'Burglary', 'Theft', 'Other_Cases', 'Arms_Act', 'Explosive', 'Narcotics', 'Smuggling']])
X[:5]

"""#### **Features to be Predicted**"""

y = np.asarray(df['Crime_Rate'])
y[:5]

"""#### **Normalizing Dataset**"""

X = preprocessing.MinMaxScaler().fit(X).transform(X)
X[0:5]

"""#### **Split Dataset into Train and Test**"""

X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=10)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)

"""#### **Applying Algorithms**

**K - Nearest Neighbor**
"""

n_neighbors = 5
knn = KNeighborsClassifier(n_neighbors, weights='distance')
knn.fit(X_train, y_train)
Y_pred_knn = knn.predict(X_test)
acc_knn = round(knn.score(X_test,y_test) * 100, 2)
print("K - Nearest Neighbours Accuracy: ", acc_knn)

cvs_knn = round((cross_val_score(knn, X,y,cv=10,scoring='accuracy')).mean()*100,2)
print('Cross Validated Score:', cvs_knn)

class_report = classification_report(y_test, Y_pred_knn)
print("Classificiation Report: \n", class_report)

cnf_matrix = confusion_matrix(y_test, Y_pred_knn)
print(cnf_matrix)

jac_score_knn = round(jaccard_score(y_test, Y_pred_knn, average='micro') * 100, 3)
print("Jaccard Score: ", jac_score_knn)

"""**Random Forest**"""

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, y_train)
Y_pred_rf = random_forest.predict(X_test)
acc_random_forest = round(random_forest.score(X_test,y_test) * 100, 2)
print("Random Forest Accuracy: ", acc_random_forest)

cvs_rf = round((cross_val_score(random_forest, X,y,cv=10,scoring='accuracy')).mean()*100,2)
print('Cross Validated Score:', cvs_rf)

class_report = classification_report(y_test, Y_pred_rf)
print("Classificiation Report: \n", class_report)

cnf_matrix = confusion_matrix(y_test, Y_pred_rf)
print(cnf_matrix)

jac_score_rf = round(jaccard_score(y_test, Y_pred_rf, average='micro') * 100, 2)
print("Jaccard Score: ", jac_score_rf)

importance_rf = random_forest.feature_importances_

for i,v in enumerate(importance_rf):
    print('Feature: %0d, Score: %.5f' % (i,v))
plt.bar([x for x in range(len(importance_rf))], importance_rf)
plt.show()
std_rf = round(np.std(importance_rf), 2)
print("Standard Daviation of Feature Importance", std_rf)

"""**Naive Bayes**"""

gaussian = GaussianNB()
gaussian.fit(X_train, y_train)
Y_pred_gnb = gaussian.predict(X_test)
acc_gaussian = round(gaussian.score(X_test,y_test) * 100, 2)
print("Gaussian Naive Bayes Accuracy: ", acc_gaussian)

cvs_gnb = round((cross_val_score(gaussian, X,y,cv=10,scoring='accuracy')).mean()*100,2)
print('Cross Validated Score:', cvs_rf)

class_report = classification_report(y_test, Y_pred_gnb)
print("Classificiation Report: \n", class_report)

cnf_matrix = confusion_matrix(y_test, Y_pred_gnb)
print(cnf_matrix)

jac_score_gaussian = round(jaccard_score(y_test, Y_pred_gnb, average='micro') * 100, 2)
print("Jaccard Score: ", jac_score_gaussian)

"""**XGBoost**"""

xgb = XGBClassifier(eval_metric='mlogloss')
xgb.fit(X_train, y_train)
Y_pred_xgb = xgb.predict(X_test)
XGB_score = round(xgb.score(X_test,y_test) * 100, 2)
print("XGBoost Accuracy: ", XGB_score)

cvs_xgb = round((cross_val_score(xgb, X,y,cv=10,scoring='accuracy')).mean()*100,2)
print('Cross Validated Score:', cvs_xgb)

class_report = classification_report(y_test, Y_pred_xgb)
print("Classificiation Report: \n", class_report)

cnf_matrix = confusion_matrix(y_test, Y_pred_xgb)
print(cnf_matrix)

jac_score_xgb = round(jaccard_score(y_test, Y_pred_xgb, average='micro') * 100, 2)
print("Jaccard Score: ", jac_score_xgb)

importance_xgb = xgb.feature_importances_

for i,v in enumerate(importance_xgb):
    print('Feature: %0d, Score: %.5f' % (i,v))
plt.bar([x for x in range(len(importance_xgb))], importance_xgb)
plt.show()
std_xgb = round(np.std(importance_xgb), 2)
print("Standard Daviation of Feature Importance", std_xgb)

"""**Stochastic Gradient Descent**"""

sgd = SGDClassifier()
sgd.fit(X_train, y_train)
Y_pred_sgd = sgd.predict(X_test)
acc_sgd = round(sgd.score(X_test,y_test) * 100, 2)
print("Stochastic Gradient Descent Accuracy: ", acc_sgd)

cvs_sgd = round((cross_val_score(sgd, X,y,cv=10,scoring='accuracy')).mean()*100,2)
print('Cross Validated Score:', cvs_sgd)

class_report = classification_report(y_test, Y_pred_sgd)
print("Classificiation Report: \n", class_report)

cnf_matrix = confusion_matrix(y_test, Y_pred_sgd)
print(cnf_matrix)

jac_score_sgd = round(jaccard_score(y_test, Y_pred_sgd, average='micro') * 100, 2)
print("Jaccard Score: ", jac_score_sgd)

"""**Discriminate Analysis**"""

descr = LinearDiscriminantAnalysis()
descr.fit(X_train, y_train)
Y_pred_descr = descr.predict(X_test)
acc_descr = round(descr.score(X_test,y_test) * 100, 2)
print("Discriminate Analysis: ", acc_descr)

cvs_descr = round((cross_val_score(descr, X,y,cv=10,scoring='accuracy')).mean()*100,2)
print('Cross Validated Score:', cvs_descr)

class_report = classification_report(y_test, Y_pred_descr)
print("Classificiation Report: \n", class_report)

cnf_matrix = confusion_matrix(y_test, Y_pred_descr)
print(cnf_matrix)

jac_score_descr = round(jaccard_score(y_test, Y_pred_descr, average='micro') * 100, 2)
print("Jaccard Score: ", jac_score_descr)

importance_descr = descr.coef_[0]
for i,v in enumerate(importance_descr):
    print('Attribute: %0d, Score: %.5f' % (i,v))
plt.bar([x for x in range(len(importance_descr))], importance_descr)
plt.show()
std_descr = round(np.std(importance_descr), 2)
print("Standard Daviation of Feature Importance", std_descr)

"""#### **Mean Absolute Error and Mean Squared Error for the Algorithms**"""

knn_mae = round((mean_absolute_error(y_test, Y_pred_knn)*100), 2)
knn_mse = round((mean_squared_error(y_test, Y_pred_knn)*100), 2)

rf_mae = round((mean_absolute_error(y_test, Y_pred_rf)*100), 2)
rf_mse = round((mean_squared_error(y_test, Y_pred_rf)*100), 2)

gnb_mae = round((mean_absolute_error(y_test, Y_pred_gnb)*100), 2)
gnb_mse = round((mean_squared_error(y_test, Y_pred_gnb)*100), 2)

xgb_mae = round((mean_absolute_error(y_test, Y_pred_xgb)*100), 2)
xgb_mse = round((mean_squared_error(y_test, Y_pred_xgb)*100), 2)

sgd_mae = round((mean_absolute_error(y_test, Y_pred_sgd)*100), 2)
sgd_mse = round((mean_squared_error(y_test, Y_pred_sgd)*100), 2)

descr_mae = round((mean_absolute_error(y_test, Y_pred_descr)*100), 2)
descr_mse = round((mean_squared_error(y_test, Y_pred_descr)*100), 2)

"""#### **All reports Table**"""

models = pd.DataFrame({
    'Algorithm Name': ['KNN', 'Random Forest', 'Naive Bayes', 'XGBoost Classifier', 'Stochastic Gradient Decent', 'Discriminate Analysis'],
    'Accuracy Score (%)': [acc_knn, acc_random_forest, acc_gaussian, XGB_score, acc_sgd, acc_descr],
    'Jaccard Score (%)' : [jac_score_knn, jac_score_rf, jac_score_gaussian, jac_score_xgb, jac_score_sgd, jac_score_descr],
    'Cross Validated Score (%)' : [cvs_knn, cvs_rf, cvs_gnb, cvs_xgb, cvs_sgd, cvs_descr],
    'Misclassification (%)': [(abs(acc_knn-100)), (abs(acc_random_forest-100)), (abs(acc_gaussian-100)), (abs(XGB_score-100)), (abs(acc_sgd-100)), (abs(acc_descr-100))],
    'Mean Absolute Error (%)' : [knn_mae, rf_mae, gnb_mae, xgb_mae, sgd_mae, descr_mae],
    'Mean Squared Error (%)' : [knn_mse, rf_mse, gnb_mse, xgb_mse, sgd_mse, descr_mse],
    'Standard Deviation' : ['--', std_rf, '--', std_xgb, '--', std_descr]
})
models.to_csv (r'F:\Necessary All\Research Works\Bangladesh Crime\All_Important_Info_Table.csv', index = False, header=True)                                                                                                                                                                                                                                                                                                                                                                                                                                               
models

"""**ROC Curve**"""

auc_knn = roc_auc_score(y_test, Y_pred_knn)
fpr_knn, tpr_knn, thresholds_knn = roc_curve(y_test, Y_pred_knn)

auc_rf = roc_auc_score(y_test, Y_pred_rf)
fpr_rf, tpr_rf, thresholds_rf = roc_curve(y_test, Y_pred_rf)

auc_gnb = roc_auc_score(y_test, Y_pred_gnb)
fpr_gnb, tpr_gnb, thresholds_gnb = roc_curve(y_test, Y_pred_gnb)

auc_xgb = roc_auc_score(y_test, Y_pred_xgb)
fpr_xgb, tpr_xgb, thresholds_xgb = roc_curve(y_test, Y_pred_xgb)

auc_sgd = roc_auc_score(y_test, Y_pred_sgd)
fpr_sgd, tpr_sgd, thresholds_sgd = roc_curve(y_test, Y_pred_sgd)

"""#### **Visualization**"""

Tfont = {'fontname':'Cambria', 'fontsize':20} #initializing font and font size
Lfont = {'fontname':'Cambria', 'fontsize':16}

plt.figure(figsize=(12, 7))
plt.plot(fpr_knn, tpr_knn, label=f'AUC (K-Nearest Neighbours) = {auc_knn:.2f}')
plt.plot(fpr_rf, tpr_rf, label=f'AUC (Random Forests) = {auc_rf:.2f}')
plt.plot(fpr_gnb, tpr_gnb, label=f'AUC (Gaussian Naive Bayes) = {auc_gnb:.2f}')
plt.plot(fpr_xgb, tpr_xgb, label=f'AUC (XGBoost) = {auc_xgb:.2f}')
plt.plot(fpr_sgd, tpr_sgd, label=f'AUC (SGD) = {auc_sgd:.2f}')

plt.title('ROC AUC Score')
plt.plot([0, 1], [0, 1], color='blue', linestyle='--', label='Baseline')
plt.legend()

"""**Algorithm's Chart**"""

plt.figure(figsize=(16, 8))
splot=sns.barplot(y="Accuracy Score (%)",x="Algorithm Name",data=models)
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.2f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   size=12,
                   xytext = (0, -12), 
                   textcoords = 'offset points')

plt.xticks(rotation=90)
plt.title("Accuracy Chart",**Tfont)
plt.ylabel("Accuracy (%)",**Lfont)
plt.xlabel("Algorithm Name",**Lfont)

plt.show()

"""**Misclassification Score Chart for Algorithms**"""

plt.figure(figsize=(16, 8))
splot=sns.barplot(y="Misclassification (%)",x="Algorithm Name",data=models)
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.2f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   size=12,
                   xytext = (0, -12), 
                   textcoords = 'offset points')

plt.xticks(rotation=90)

plt.title("Misclassification Chart",**Tfont)
plt.ylabel("Misclassification (%)",**Lfont)
plt.xlabel("Algorithm Name",**Lfont)

plt.show()

"""**Jaccard Score Chart for Algorithms**"""

plt.figure(figsize=(16, 8))
splot=sns.barplot(y="Jaccard Score (%)",x="Algorithm Name",data=models)
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.2f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   size=12,
                   xytext = (0, -12), 
                   textcoords = 'offset points')

plt.xticks(rotation=90)

plt.title("Jaccard Similarity Index Chart",**Tfont)
plt.ylabel("Jaccard Score (%)",**Lfont)
plt.xlabel("Algorithm Name",**Lfont)

plt.show()

"""**Cross Validation Score Cahrt for Algorithms**"""

plt.figure(figsize=(16, 8))
splot=sns.barplot(y="Cross Validated Score (%)",x="Algorithm Name",data=models)
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.2f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   size=12,
                   xytext = (0, -12), 
                   textcoords = 'offset points')

plt.xticks(rotation=90)

plt.title("Cross Validation Chart",**Tfont)
plt.ylabel("Cross Validated Score (%)",**Lfont)
plt.xlabel("Algorithm Name",**Lfont)

plt.show()

"""**Heatmap to show Correlation**"""

plt.figure(figsize=(12,8))
sns.heatmap(df.iloc[:,0:10].corr(),cmap="rocket", annot=True, fmt ='.0%', linecolor='Blue')

df.corr() #correlation

numeric_cols1= ['Dacoity','Robbery','Murder','Speedy_Trial', 'Riot', 'W_&_C_Repression', 'Kidnapping', 'Police_Assault', 'Burglary', 'Theft', 'Other_Cases', 'Arms_Act', 'Explosive', 'Narcotics', 'Smuggling']

def hist_for_nums(data, numeric_cols1):
    col_counter = 0
    data = data.copy()
    for col in numeric_cols1:
        data[col].hist()
        plt.xlabel(col)
        plt.title(col)
        plt.show()
        col_counter += 1
    print(col_counter, "variables have been plotted")
hist_for_nums(df, numeric_cols1)

"""**Year-wise Crime Rate**"""

#plt.style.use(['dark_background'])
Year = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
Crime_Rate = [162898,169667,183407,179199,183729,179835,181168,213529,221419,17484,167316,171786]
  
plt.plot(Year, Crime_Rate, color='red')
plt.title('Crime Rate Vs Year')
plt.xlabel('Year')
plt.ylabel('Crime Rate')
plt.show()