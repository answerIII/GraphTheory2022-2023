from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from prepare_data import prepare_data_all
from static_features import calc_four_static_properties


def link_prediction(dataset):

    [V, adjList, nonexistent_edges, y] = prepare_data_all(dataset, s = 50, display_interm_results=False)

    # for i in range(V):
    #     print(i, ":", end=" ")
    #     print(adjList[i])

    for edge in nonexistent_edges:
        features = calc_four_static_properties(adjList, edge, display_interm_results=False)
        edge = list(edge)
        # print(edge, end=":")
        edge += features
        # print(edge)


    X_train, X_test, y_train, y_test = train_test_split(nonexistent_edges, y, test_size=0.25, random_state=1)



    logistic_model = LogisticRegression()
    logistic_model.fit(X_train, y_train)


    predictions = logistic_model.predict(X_test)

    print(classification_report(y_test, predictions))

