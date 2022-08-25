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

    l = []
    X_train, X_test, y_train, y_test = train_test_split(features[features.columns[:-1]], features['Clogging?'], test_size = 0.3, random_state = ri(1, 10))
    for i in range(1, 200):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        l.append(accuracy_score(y_pred, y_test) * 100)

    return np.mean(l)


if __name__ == '__main__':
    main()