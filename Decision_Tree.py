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
    
    
    X_train, X_test, Y_train, Y_test = train_test_split(features[features.columns[:-1]], features['Clogging?'], test_size=0.3, random_state=ri(1,100))
    
    # clf = DecisionTreeClassifier(random_state = 5)
    # clf.fit(X_train, Y_train)
    
    # fig = plt.figure(figsize=(25,20))
    # _ = tree.plot_tree(clf, 
    #                    feature_names= features.columns[:-1],
    #                    class_names='Clogging?',
    #                    filled=True)
    
    # fig.savefig('output.pdf')
    
    l = list()
    
    clf = DecisionTreeClassifier(max_depth = 8, random_state = 10)
    clf.fit(X_train, Y_train)
    y_pred = clf.predict(X_test)#Accuracy
    l.append(accuracy_score(y_pred, Y_test) * 100)
    cm = confusion_matrix(Y_test, y_pred)
    
    return l[0]
    

if __name__ == '__main__':
    main()

