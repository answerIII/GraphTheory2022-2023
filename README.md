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

To just create a graph instance, in Node.js REPL (command: `node`):
(also, do not forget to replace `ra` with the desired dataset name)

```js
require("./index.js").nodeCreateGraphInstance("ra");
```

To run the logistic regression, just run the Python file `index.py`.
(SciKit Learn and matplotlib are required to be installed to run it)

The tests (used for running the tests and getting their values):

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("socfb-45.txt", "test", {
    forceExact: true,
    skipEstimates: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         3075
Edges number:                         124610
Unique edges number:                  124610
Density:                              0.02636537230694363
WCCs number:                          4
LWCC size:                           3069
LWCC relative size:                   0.9980487804878049
LWCC exact                d / r / p:  7 4 3
LWCC average clustering coefficient:  0.282179987534055
Assortativity coefficient:            0.07848305830139335
================================================================================
[ 2, 0.011049723756906077, 8262, 0.3824839729980579 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("socfb-98.txt", "test", {
    forceExact: true,
    skipEstimates: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         962
Edges number:                         18812
Unique edges number:                  18812
Density:                              0.04069738513026754
WCCs number:                          1
LWCC size:                           962
LWCC relative size:                   1
LWCC exact                d / r / p:  6 4 3
LWCC average clustering coefficient:  0.31836022727227925
Assortativity coefficient:            0.02343391176630078
================================================================================
[ 19, 0.18627450980392157, 3504, 4.724067092686206 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("team_08.txt", "test", {
    forceExact: true,
    skipEstimates: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         1039
Edges number:                         53830
Unique edges number:                  53830
Density:                              0.09982549546492199
WCCs number:                          1
LWCC size:                           1039
LWCC relative size:                   1
LWCC exact                d / r / p:  3 2 2
LWCC average clustering coefficient:  0.09951291125169902
Assortativity coefficient:            -0.005335689000095349
================================================================================
[ 11, 0.06077348066298342, 9215, 2.3627690898122466 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("testgraph_1.txt", "test", {
    oneEstimate: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         9
Edges number:                         13
Unique edges number:                  13
Density:                              0.3611111111111111
WCCs number:                          1
LWCC size:                           9
LWCC relative size:                   1
LWCC exact                d / r / p:  3 2 3
LWCC estimated (random)   d / r / p:  3 2 3
LWCC estimated (snowball) d / r / p:  3 2 3
LWCC average clustering coefficient:  0.4
Assortativity coefficient:            -0.2037037037037037
================================================================================
[ 2, 0.2857142857142857, 18, 1.820478453253675 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("testgraph_2.txt", "test", {
    forceExact: true,
    skipEstimates: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         34
Edges number:                         78
Unique edges number:                  78
Density:                              0.13903743315508021
WCCs number:                          1
LWCC size:                           34
LWCC relative size:                   1
LWCC exact                d / r / p:  5 3 4
LWCC average clustering coefficient:  0.5706384782076823
Assortativity coefficient:            -0.47561309768461435
================================================================================
[ 7, 0.3888888888888889, 144, 6.130716871863356 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("testgraph_3.txt", "test", {
    forceExact: true,
    skipEstimates: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         77
Edges number:                         254
Unique edges number:                  254
Density:                              0.08680792891319207
WCCs number:                          1
LWCC size:                           77
LWCC relative size:                   1
LWCC exact                d / r / p:  5 3 4
LWCC average clustering coefficient:  0.5731367499320134
Assortativity coefficient:            -0.16522513442236963
================================================================================
[ 0, 0, 10, 0 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("testgraph_4.txt", "test", {
    forceExact: true,
    skipEstimates: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         62
Edges number:                         159
Unique edges number:                  159
Density:                              0.08408249603384453
WCCs number:                          1
LWCC size:                           62
LWCC relative size:                   1
LWCC exact                d / r / p:  8 5 5
LWCC average clustering coefficient:  0.2589582460550202
Assortativity coefficient:            -0.04359402821531297
================================================================================
[ 0, 0, 48, 0 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("testgraph_5.txt", "test", {
    forceExact: true,
    skipEstimates: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         198
Edges number:                         2742
Unique edges number:                  2742
Density:                              0.14059375480695277
WCCs number:                          1
LWCC size:                           198
LWCC relative size:                   1
LWCC exact                d / r / p:  6 4 3
LWCC average clustering coefficient:  0.6174507021536301
Assortativity coefficient:            0.020237399275047283
================================================================================
[ 0, 0, 69, 0 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("testgraph_6.txt", "test", {
    forceExact: true,
    skipEstimates: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         19428
Edges number:                         96662
Unique edges number:                  96662
Density:                              0.000512214581272078
WCCs number:                          23
LWCC size:                           19365
LWCC relative size:                   0.996757257566399
LWCC exact                d / r / p:  11 6 6
LWCC average clustering coefficient:  0
Assortativity coefficient:            -0.19155705078320998
================================================================================
[ 0, 0, 9, 0 ]
```

```js
// prettier-ignore
require("./index.js").nodeGenerateGraphInformation("testgraph_7.txt", "test", {
    oneEstimate: true,
}).calculateStaticFeatures(1, 2);
```

```
================================================================================
Nodes number:                         325729
Edges number:                         1117563
Unique edges number:                  1117563
Density:                              0.000021066408037288526
WCCs number:                          1
LWCC size:                           325729
LWCC relative size:                   1
LWCC estimated (random)   d / r / p:  28 2 10
LWCC estimated (snowball) d / r / p:  30 24 9
LWCC average clustering coefficient:  0.2417871186789608
Assortativity coefficient:            -0.05195813420048538
================================================================================
[ 583, 0.07612953773831288, 4718018, 255.85940916255996 ]
```
