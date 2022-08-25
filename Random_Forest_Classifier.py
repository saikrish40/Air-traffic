from imports import *


def main():
    data = pd.read_csv('flight3.csv')

    features = data[["N_Traffic","NE_Traffic","E_Traffic","SE_Traffic","S_Traffic","SW_Traffic","W_Traffic","NW_Traffic","Clogging?"]]

    d = {'Yes': 1, 'No': 0}

    features = features.replace({'S_Traffic': d})
    features = features.replace({'N_Traffic': d})
    features = features.replace({'E_Traffic': d})
    features = features.replace({'W_Traffic': d})
    features = features.replace({'Clogging?': d})
    features = features.replace({'NE_Traffic': d})
    features = features.replace({'SE_Traffic': d})
    features = features.replace({'SW_Traffic': d})
    features = features.replace({'NW_Traffic': d})

    X, y = features[features.columns[:-1]], features['Clogging?']

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.30,random_state=ri(1,50))

    clf = RandomForestClassifier(n_estimators=2)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)#Accuracy

    return accuracy_score(y_test,y_pred) * 100

    # cm = confusion_matrix(y_test, y_pred)
    # print(cm)


if __name__ == '__main__':
    print(main())