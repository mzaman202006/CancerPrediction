# -*- coding: utf-8 -*-
"""Predicting Breast Cancer -ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/mzaman202006/CancerPrediction/blob/main/Predicting_Breast_Cancer_ML.ipynb
"""

# Commented out IPython magic to ensure Python compatibility.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import sklearn.linear_model as skl_lm
from sklearn import preprocessing
from sklearn import neighbors
from sklearn.metrics import confusion_matrix, classification_report, precision_score
from sklearn.model_selection import train_test_split

import statsmodels.api as sm
import statsmodels.formula.api as smf

sns.set(style="whitegrid", color_codes=True, font_scale=1.3)

# %matplotlib inline

df = pd.read_csv('data.csv', index_col=0)
df.head()

df.describe()
df = df.drop('Unnamed: 32', axis=1)

plt.figure(figsize=(8, 4))
sns.countplot(df['diagnosis'], palette='RdBu')

benign, malignant = df['diagnosis'].value_counts()
print('Number of cells labeled Benign: ', benign)
print('Number of cells labeled Malignant : ', malignant)
print('')
print('% of cells labeled Benign', round(benign / len(df) * 100, 2), '%')
print('% of cells labeled Malignant', round(malignant / len(df) * 100, 2), '%')

corr = df.corr().round(2)


mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True


f, ax = plt.subplots(figsize=(20, 20))

cmap = sns.diverging_palette(220, 10, as_cmap=True)

sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)

plt.tight_layout()
plt.savefig('h.png')

cols = ['radius_worst', 
        'texture_worst', 
        'perimeter_worst', 
        'area_worst', 
        'smoothness_worst', 
        'compactness_worst', 
        'concavity_worst',
        'concave points_worst', 
        'symmetry_worst', 
        'fractal_dimension_worst']
df = df.drop(cols, axis=1)

cols = ['perimeter_mean',
        'perimeter_se', 
        'area_mean', 
        'area_se']
df = df.drop(cols, axis=1)

df.columns

corr = df.corr().round(2)
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

f, ax = plt.subplots(figsize=(20, 20))
sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)
plt.tight_layout()
plt.savefig('h2.png')

df['diagnosis'] = df['diagnosis'].apply(lambda val: 1 if val == 'M' else 0)
X = df
y = df['diagnosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=40)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""#Logistic regression

"""

from sklearn.linear_model import LogisticRegressionCV

log_reg = LogisticRegressionCV()
log_reg.fit(X_train, y_train)


print('Coefficients: ', log_reg.coef_)
 

print('Variance score: {}'.format(log_reg.score(X_test, y_test)))

y_pred = log_reg.predict(X_test)

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print(accuracy_score(y_train, log_reg.predict(X_train)))

log_reg_acc = accuracy_score(y_test, log_reg.predict(X_test))
print(log_reg_acc)

print(confusion_matrix(y_test, y_pred))

print(classification_report(y_test, y_pred))

"""#KNN"""

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=200,weights="distance")
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

knn_acc = accuracy_score(y_test, knn.predict(X_test))
print(knn_acc)

print(confusion_matrix(y_test, y_pred))

print(classification_report(y_test, y_pred))

"""#SVC

"""

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

svc = SVC(C = .1, gamma = .02)
svc.fit(X_train, y_train)

y_pred = svc.predict(X_test)


svc_acc = accuracy_score(y_test, svc.predict(X_test))
print(svc_acc)

print(confusion_matrix(y_test, y_pred))

print(classification_report(y_test, y_pred))

#Decision tree

"""#Tree

"""

from sklearn.tree import DecisionTreeClassifier

dtc = DecisionTreeClassifier()

parameters = {
    'criterion' : ['gini', 'entropy'],
    'max_depth' : range(2, 32, 1),
    'min_samples_leaf' : range(1, 10, 1),
    'min_samples_split' : range(2, 10, 1),
    'splitter' : ['best', 'random']
}

grid_search_dt = GridSearchCV(dtc, parameters, cv = 5, n_jobs = -1, verbose = 1)
grid_search_dt.fit(X_train, y_train)

dtc = DecisionTreeClassifier(criterion = 'gini', max_depth = 200, min_samples_leaf = 1)
dtc.fit(X_train, y_train)

y_pred = dtc.predict(X_test)

print(accuracy_score(y_train, dtc.predict(X_train)))

dtc_acc = accuracy_score(y_test, dtc.predict(X_test))
print(dtc_acc)