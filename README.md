# Supervised Temporal Link Prediction (Graph Theory Project)

I know, I know, it was asked that we use a single programming language,
but unfortunately I did not find the good Node.js / JavaScript library
for machine learning that would be as easy to use as SciKit Learn, so I
decided that while the logic of the project is written in JavaScript,
the machine learning will be done in Python.

## Directores

-   `data` &mdash; The features and the answers generated via `index.js`.
-   `sets` &mdash; The datasets used in the project (from http://konect.cc).

## Links

-   https://link.springer.com/article/10.1007/s13278-021-00787-3

## Steps

To generate features and answers, in Node.js REPL (command: `node`):
(also, do not forget to replace `ra` with the desired dataset name)

```js
require("./index.js").nodeGenerateFeaturesAnswers("ra");
```

To generate information about a graph, in Node.js REPL (command: `node`):
(also, do not forget to replace `ra` with the desired dataset name)

```js
require("./index.js").nodeGenerateGraphInformation("ra");
```

To run the logistic regression, just run the Python file `index.py`.
