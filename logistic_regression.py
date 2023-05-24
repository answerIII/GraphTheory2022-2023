from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from prepare_data import prepare_data_all, prepare_data_at_dist_2
from static_features import calc_four_static_properties


def link_prediction(dataset, s):

    # [V, adjList, nonexistent_edges, y] = prepare_data_all(dataset, s, display_interm_results=False)
    [V, adjList, nonexistent_edges, y] = prepare_data_at_dist_2(dataset, s, display_interm_results=False)

    # for i in range(V):
    #     print(i, ":", end=" ")
    #     print(adjList[i])

    X = []
    for edge in nonexistent_edges:
        features = calc_four_static_properties(adjList, edge, display_interm_results=False)
        X.append(features)
        

    # for i in range(len(nonexistent_edges)):
    #     print(nonexistent_edges[i], ":", X[i])



    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)



    logistic_model = LogisticRegression()
    logistic_model.fit(X_train, y_train)


    predictions = logistic_model.predict(X_test)

    print(classification_report(y_test, predictions))

