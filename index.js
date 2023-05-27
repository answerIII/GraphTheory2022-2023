#!/usr/bin/env node
// @ts-check

/**
 * @file The main graph computation library.
 */

/**
 * The state of the column being read.
 * @enum {number}
 */
const GraphParserColumnState = Object.freeze({
    /**
     * The first column (the edge source).
     */
    from: 1,

    /**
     * The second column (the edge destination).
     */
    to: 2,

    /**
     * The third column (the edge weight, skipped).
     */
    weight: 3,

    /**
     * The fourth column (the edge creation timestamp).
     */
    timestamp: 4,
});

/**
 * The more efficient queue implementation.
 * @template T
 */
class Queue {
    /**
     * @typedef QueueValue
     *     An interal queue value for implementation.
     * @property {T}                      value
     *     A value that is held itself.
     * @property {QueueValue | undefined} next
     *     A queue value right "behind" this one.
     */

    /**
     * The first queue value in the queue.
     * @type {QueueValue | undefined}
     */
    #first;

    /**
     * The last queue value in the queue.
     * @type {QueueValue | undefined}
     */
    #last;

    /**
     * Peeks at the first value from the queue.
     * @returns {T | undefined}
     */
    peek() {
        return this.#first?.value;
    }

    /**
     * Gets the first value from the queue.
     * @returns {T | undefined}
     */
    pop() {
        if (this.#first) {
            // Get the value and move to the next one.
            const value = this.#first.value;
            this.#first = this.#first.next;
            return value;
        }
    }

    /**
     * Adds `value` to the queue.
     * @param {T} value The last value in the queue.
     */
    push(value) {
        if (this.#first && this.#last) {
            // We are behind the last value now.
            this.#last.next = { value, next: undefined };

            // Finally, we ourselves are last now.
            this.#last = this.#last.next;
        } else {
            // If no one is here, we are first.
            this.#first = { value, next: undefined };

            // If no one is here, we are last too.
            this.#last = this.#first;
        }
    }
}

/**
 * The undirected temporal (and static) graph.
 */
class Graph {
    /**
     * @typedef GraphParserState
     *     A state of a graph parser.
     * @property {number?}                currentEdgeFrom
     *     A current edge source.
     * @property {number?}                currentEdgeTo
     *     A current edge destination.
     * @property {GraphParserColumnState} currentColumnState
     *     A column being read currently.
     * @property {boolean}                isLineSkipped
     *     Whether a current line is skipped.
     * @property {boolean}                isDelimiterBefore
     *     Whether a character before was a delimiter.
     * @property {string}                 readBuffer
     *     An already read characters buffer.
     */

    /**
     * @typedef GraphTemporalWeights
     *    Temporal weights for a pair of the graph nodes.
     * @property {number} lin
     *    A linear temporal weight.
     * @property {number} sqrt
     *    A square root temporal weight.
     * @property {number} exp
     *    An exponential temporal weight.
     */

    /**
     * @typedef GraphWCCFeatures
     *     Features associated with a weakly connected component
     *     of a graph.
     * @property {number} percentile
     *     A 90-percentile of distances of a weakly connected
     *     component of a graph.
     * @property {number} diameter
     *     A diameter of a weakly connected component of a graph.
     * @property {number} radius
     *     A radius of a weakly connected component of a graph.
     */

    /**
     * The limit on the attempts during the feature selection generation.
     */
    #featureSelectionAttemptsNumber = 10_000_000;

    /**
     * The size of the positive or negative answers in the generated
     * feature selection.
     */
    #featureSelectionEachSize = 10_000;

    /**
     * The number of experiments to do for the estimation of features
     * of the largest weakly connected component.
     * @readonly
     */
    #largestWCCFeaturesExperimentsNumber = 5;

    /**
     * The size of the subgraph to use for the estimation of features
     * of the largest weakly connected component.
     * @readonly
     */
    #largestWCCFeaturesSubgraphSize = 500;

    /**
     * The threshold for doing the exact calculation of features of the
     * largest weakly connected component.
     * @readonly
     */
    #largestWCCFeaturesThreshold = 500;

    /**
     * The characters that are treated by the graph parser as comments.
     * @readonly
     */
    #parserComments = "%";

    /**
     * The characters that are treated by the graph parser as delimiters.
     * @readonly
     */
    #parserDelimiters = " \t";

    /**
     * The characters that are treated by the graph parser as newlines.
     * @readonly
     */
    #parserNewlines = "\r\n";

    /**
     * The point from the interval at which the temporal network is split.
     * @readonly
     */
    #split = 2 / 3;

    /**
     * The decoder for the text.
     * @readonly
     */
    #text = new TextDecoder("utf-8");

    /**
     * The adjacency list of the graph. The value(s) held is (are) the
     * edge creation time(s).
     * @type {Map<number, Map<number, Date[]>>}
     */
    #adjacency = new Map();

    /**
     * The number of loops each node has.
     * @type {Map<number, number>}
     */
    #loops = new Map();

    /**
     * The distances list of the graph.
     * @type {Map<number, Map<number, number>>}
     */
    #distances = new Map();

    /**
     * The state of the graph parser.
     * @type {GraphParserState}
     */
    #parserState = {
        currentEdgeFrom: null,
        currentEdgeTo: null,
        currentColumnState: GraphParserColumnState.from,
        isLineSkipped: false,
        isDelimiterBefore: false,
        readBuffer: "",
    };

    /**
     * The latest date observed in the graph.
     */
    #maxTime = new Date(NaN);

    /**
     * The earliest date observed in the graph.
     */
    #minTime = new Date(NaN);

    /**
     * The time at which the temporal network is split.
     */
    #splitTime = new Date(NaN);

    /**
     * The numbers of distances that were encountered.
     * @type {Map<number, number>}
     */
    #distanceNumbers = new Map();

    /**
     * The maximum distances from a source node.
     * @type {Map<number, number>}
     */
    #maxDistances = new Map();

    /**
     * The assortativity coefficient of the graph.
     */
    assortativityCoefficient = 0;

    /**
     * The average clustering coefficient of the graph.
     */
    clusteringCoefficient = 0;

    /**
     * The density charcteristic of the graph.
     */
    density = 0;

    /**
     * The number of edges in the graph (counting multiple edges as many).
     */
    edgesNumber = 0;

    /**
     * The number of nodes in the graph.
     */
    nodesNumber = 0;

    /**
     * The number of edges in the graph (counting multiple edges as one).
     */
    uniqueEdgesNumber = 0;

    /**
     * The list of weakly connected components of the graph.
     * @type {number[][]}
     */
    wccs = [];

    /**
     * The largest weakly connected component of the graph.
     * @type {number[]}
     */
    largestWCC = [];

    /**
     * The relative size of the largest weakly connected component.
     */
    largestWCCRelativeSize = 0;

    /**
     * Features associated with a largest weakly connected component
     * of a graph.
     * @type {GraphWCCFeatures?}
     */
    largestWCCFeatures = null;

    /**
     * Features associated with a largest weakly connected component
     * of a graph, estimated using the "random sample" method with
     * 1000 nodes.
     * @type {GraphWCCFeatures[]}
     */
    largestWCCFeatures1000Random = [];

    /**
     * Features associated with a largest weakly connected component
     * of a graph, estimated using the "snowball sample" method with
     * 1000 nodes.
     * @type {GraphWCCFeatures[]}
     */
    largestWCCFeatures1000Snowball = [];

    /**
     * Calculates the features (or estimates their values) of the largest
     * weakly connected component of the graph.
     * @param {object}  args
     * @param {boolean} [args.forceExact]
     * @param {boolean} [args.skipEstimates]
     * @param {boolean} [args.oneEstimate]
     */
    calculateLargestWCCFeatures({
        forceExact = false,
        skipEstimates = false,
        oneEstimate = false,
    }) {
        // Use the threshold for the exact calculation.
        if (
            forceExact ||
            this.largestWCC.length <= this.#largestWCCFeaturesThreshold
        ) {
            const now = performance.now();
            console.info("Started the exact calculation");

            this.largestWCCFeatures = this.#calculateSubWCCFeatures(
                this.largestWCC
            );

            console.info("Finished the exact calculation");

            console.info(
                `Time taken: (${Math.floor(performance.now() - now)}ms)`
            );
        }

        if (skipEstimates) {
            return;
        }

        for (let i = 0; i < this.#largestWCCFeaturesExperimentsNumber; ++i) {
            const nowR = performance.now();
            console.info(`Started the experiment (random) #${i + 1}`);

            this.#distanceNumbers.clear();
            this.#maxDistances.clear();

            for (let j = 0; j < this.#largestWCCFeaturesSubgraphSize; ++j) {
                // Get the two random node indexes for the component.
                const fromIndex = Math.floor(
                    Math.random() * this.largestWCC.length
                );

                const toIndex = Math.floor(
                    Math.random() * this.largestWCC.length
                );

                // Get the corresponding nodes for the node indexes.
                const fromNode = this.largestWCC[fromIndex];
                const toNode = this.largestWCC[toIndex];

                this.doBFSFrom({ fromNode, toNode });

                // Get the result distance between the two nodes.
                const result = /** @type {number} */ (
                    /** @type {Map<number, number>} */ (
                        this.#distances.get(fromNode)
                    ).get(toNode)
                );

                this.#updateMaxDistances({ fromNode, result });
                this.#updateDistanceNumbers({ result });
            }

            // Add the result to the "random" experiments vector.
            this.largestWCCFeatures1000Random.push(
                this.#calculateWCCFeatures()
            );

            console.info(`Finished the experiment (random) #${i + 1}`);

            console.info(
                `Time taken: (${Math.floor(performance.now() - nowR)}ms)`
            );

            const nowS = performance.now();
            console.info(`Started the experiment (snowball) #${i + 1}`);

            this.#distanceNumbers.clear();
            this.#maxDistances.clear();

            // Get the node index that will start the snowball.
            const initialIndex = Math.floor(
                Math.random() * this.largestWCC.length
            );

            // Get the corresponding node for the node index.
            const initialNode = this.largestWCC[initialIndex];

            // Create the snowball sample by utilizing BFS.
            const nodeSample = Array.from(
                this.doBFSFrom({
                    fromNode: initialNode,
                    threshold: this.#largestWCCFeaturesSubgraphSize,
                })
            );

            // Add the result to the "snowball" experiments vector.
            this.largestWCCFeatures1000Snowball.push(
                this.#calculateSubWCCFeatures(nodeSample)
            );

            console.info(`Finished the experiment (snowball) #${i + 1}`);

            console.info(
                `Time taken: (${Math.floor(performance.now() - nowS)}ms)`
            );

            if (oneEstimate) {
                break;
            }
        }
    }

    /**
     * Calculate the local clustering coefficient for `node`.
     * @param {number} node
     *     The node to calculate the coefficient for.
     * @returns {number}
     *     The result local clustering coefficient.
     */
    calculateLocalClusteringCoefficient(node) {
        // Get the neighbors of this node.
        const neighbors = Array.from(
            /** @type {Map<number, Date[]>} */ (
                this.#adjacency.get(node)
            ).keys()
        ).filter((value) => value !== node);

        // Less than two neighbors will not do anything.
        if (neighbors.length < 2) {
            return 0;
        }

        // Count the number of the edges between the neighbors.
        let neighborEdgesNumber = 0;

        // Check every possible edge on whether it exist, and
        // increase the count if it does.
        for (let i = 0; i < neighbors.length; ++i) {
            for (let j = i + 1; j < neighbors.length; ++j) {
                if (
                    /** @type {Map<number, Date[]>} */ (
                        this.#adjacency.get(neighbors[i])
                    ).has(neighbors[j])
                ) {
                    ++neighborEdgesNumber;
                }
            }
        }

        return (
            (2 * neighborEdgesNumber) /
            (neighbors.length * (neighbors.length - 1))
        );
    }

    /**
     * Calculates the static features for `firstNode` and `secondNode`.
     * @param {number} firstNode
     *     The first node.
     * @param {number} secondNode
     *     The second node.
     * @returns {number[]}
     *     The result static features.
     */
    calculateStaticFeatures(firstNode, secondNode) {
        // Get the neighbors of the both nodes.
        const firstNeighbors = Array.from(
            /** @type {Map<number, Date[]>} */ (
                this.#adjacency.get(firstNode)
            ).keys()
        ).filter((value) => value !== firstNode);

        const secondNeighbors = Array.from(
            /** @type {Map<number, Date[]>} */ (
                this.#adjacency.get(secondNode)
            ).keys()
        ).filter((value) => value !== secondNode);

        // Get the intersection and the union.
        const intersection = firstNeighbors.filter((value) => {
            return secondNeighbors.includes(value);
        });

        const union = Array.from(
            new Set([...firstNeighbors, ...secondNeighbors])
        );

        // Calculate the features as defined in the formulas.
        return [
            // CN
            intersection.length,

            // JC
            intersection.length / union.length,

            // PA
            firstNeighbors.length * secondNeighbors.length,

            // AA
            intersection.reduce((sum, node) => {
                // Get the neighbors of the node, as in formula.
                const nodeNeighbors = Array.from(
                    /** @type {Map<number, Date[]>} */ (
                        this.#adjacency.get(node)
                    ).keys()
                ).filter((value) => value !== node);

                // Do the calculation according to the formula.
                return sum + 1 / Math.log(nodeNeighbors.length);
            }, 0),
        ];
    }

    /**
     * Calculates the temporal weights for `firstNode` and `secondNode`.
     * @param {number} firstNode
     *     The first node.
     * @param {number} secondNode
     *     The second node.
     * @returns {GraphTemporalWeights}
     *     The result temporal weights.
     */
    calculateTemporalWeights(firstNode, secondNode) {
        // The limit parameter (`l` in the formula).
        const limit = 0.2;

        // Get the nodes adjacent to the first node.
        const adjacent = /** @type {Map<number, Date[]>} */ (
            this.#adjacency.get(firstNode)
        );

        if (!adjacent.has(secondNode)) {
            return {
                lin: NaN,
                sqrt: NaN,
                exp: NaN,
            };
        }

        // Get the times associated with the pair of nodes.
        const times = /** @type {Date[]} */ (adjacent.get(secondNode));

        // Skip the event aggregation, get the last time.
        // Also only consider the first interval to prevent any leakage.
        // (See the paper, section 3.3, paragraph 2).
        const lastTime = times.reduce((a, b) => {
            return a > b && a <= this.#splitTime ? a : b;
        });

        // Calculate and return the result temporal weights.
        const timeFraction =
            (lastTime.getTime() - this.#minTime.getTime()) /
            (this.#maxTime.getTime() - this.#minTime.getTime());

        const exponential =
            (Math.exp(3 * timeFraction) - 1) / (Math.E ** 3 - 1);

        const multiplier = 1 - limit;

        return {
            lin: limit + multiplier * timeFraction,
            sqrt: limit + multiplier * Math.sqrt(timeFraction),
            exp: limit + multiplier * exponential,
        };
    }

    /**
     * Calculates the temporal features for `firstNode` and `secondNode`.
     * @param {number} firstNode
     *     The first node.
     * @param {number} secondNode
     *     The second node.
     * @returns {number[]}
     *     The result temporal features.
     */
    calculateTemporalFeatures(firstNode, secondNode) {
        // Get the neighbors of the both nodes.
        const firstNeighbors = Array.from(
            /** @type {Map<number, Date[]>} */ (
                this.#adjacency.get(firstNode)
            ).keys()
        ).filter((value) => value !== firstNode);

        const secondNeighbors = Array.from(
            /** @type {Map<number, Date[]>} */ (
                this.#adjacency.get(secondNode)
            ).keys()
        ).filter((value) => value !== secondNode);

        // Get the intersection of the neighbors.
        const intersection = firstNeighbors.filter((value) => {
            return secondNeighbors.includes(value);
        });

        // Calculate the weighted sum of the first
        // node with its neighbors.
        const sumFirstNeighbors = firstNeighbors.reduce(
            (sum, neighbor) => {
                const weights = this.calculateTemporalWeights(
                    firstNode,
                    neighbor
                );

                return {
                    lin: sum.lin + weights.lin,
                    sqrt: sum.sqrt + weights.sqrt,
                    exp: sum.exp + weights.exp,
                };
            },
            { lin: 0, sqrt: 0, exp: 0 }
        );

        // Calculate the weighted sum of the second
        // node with its neighbors.
        const sumSecondNeighbors = secondNeighbors.reduce(
            (sum, neighbor) => {
                const weights = this.calculateTemporalWeights(
                    secondNode,
                    neighbor
                );

                return {
                    lin: sum.lin + weights.lin,
                    sqrt: sum.sqrt + weights.sqrt,
                    exp: sum.exp + weights.exp,
                };
            },
            { lin: 0, sqrt: 0, exp: 0 }
        );

        // Calculate the `PA` features following the formula.
        const sumPALin = sumFirstNeighbors.lin * sumSecondNeighbors.lin;
        const sumPASqrt = sumFirstNeighbors.sqrt * sumSecondNeighbors.sqrt;
        const sumPAExp = sumFirstNeighbors.exp * sumSecondNeighbors.exp;

        // Calculate the `CN` features following the formula.
        const sumCN = intersection.reduce(
            (sum, neighbor) => {
                const firstWeights = this.calculateTemporalWeights(
                    firstNode,
                    neighbor
                );

                const secondWeights = this.calculateTemporalWeights(
                    secondNode,
                    neighbor
                );

                return {
                    lin: sum.lin + firstWeights.lin + secondWeights.lin,
                    sqrt: sum.sqrt + firstWeights.sqrt + secondWeights.sqrt,
                    exp: sum.exp + firstWeights.exp + secondWeights.exp,
                };
            },
            { lin: 0, sqrt: 0, exp: 0 }
        );

        // Calculate the `JC` features following the formula.
        const sumJC = intersection.reduce(
            (sum, neighbor) => {
                const firstWeights = this.calculateTemporalWeights(
                    firstNode,
                    neighbor
                );

                const secondWeights = this.calculateTemporalWeights(
                    secondNode,
                    neighbor
                );

                return {
                    lin:
                        sum.lin +
                        (firstWeights.lin + secondWeights.lin) /
                            (sumFirstNeighbors.lin + sumSecondNeighbors.lin),
                    sqrt:
                        sum.sqrt +
                        (firstWeights.sqrt + secondWeights.sqrt) /
                            (sumFirstNeighbors.sqrt + sumSecondNeighbors.sqrt),
                    exp:
                        sum.exp +
                        (firstWeights.exp + secondWeights.exp) /
                            (sumFirstNeighbors.exp + sumSecondNeighbors.exp),
                };
            },
            { lin: 0, sqrt: 0, exp: 0 }
        );

        // Calculate the `AA` features following the formula.
        const sumAA = intersection.reduce(
            (sum, neighbor) => {
                const firstWeights = this.calculateTemporalWeights(
                    firstNode,
                    neighbor
                );

                const secondWeights = this.calculateTemporalWeights(
                    secondNode,
                    neighbor
                );

                // Get the neighbors of the neighbor.
                const neighborNeighbors = Array.from(
                    /** @type {Map<number, Date[]>} */ (
                        this.#adjacency.get(neighbor)
                    ).keys()
                ).filter((value) => value !== neighbor);

                // Calculate the weighted sum of the
                // neighbor with its neighbors.
                const sumNeighborNeighbors = neighborNeighbors.reduce(
                    (sum, squaredNeighbor) => {
                        const weights = this.calculateTemporalWeights(
                            neighbor,
                            squaredNeighbor
                        );

                        return {
                            lin: sum.lin + weights.lin,
                            sqrt: sum.sqrt + weights.sqrt,
                            exp: sum.exp + weights.exp,
                        };
                    },
                    { lin: 0, sqrt: 0, exp: 0 }
                );

                return {
                    lin:
                        sum.lin +
                        (firstWeights.lin + secondWeights.lin) /
                            Math.log(1 + sumNeighborNeighbors.lin),
                    sqrt:
                        sum.sqrt +
                        (firstWeights.sqrt + secondWeights.sqrt) /
                            Math.log(1 + sumNeighborNeighbors.sqrt),
                    exp:
                        sum.exp +
                        (firstWeights.exp + secondWeights.exp) /
                            Math.log(1 + sumNeighborNeighbors.exp),
                };
            },
            { lin: 0, sqrt: 0, exp: 0 }
        );

        return [
            sumCN.lin,
            sumJC.lin,
            sumAA.lin,
            sumPALin,
            sumCN.sqrt,
            sumJC.sqrt,
            sumAA.sqrt,
            sumPASqrt,
            sumCN.exp,
            sumJC.exp,
            sumAA.exp,
            sumPAExp,
        ];
    }

    // * @param {File} file
    // *     The file with the table-like graph data.
    /**
     * Creates a new graph by parsing `file`.
     * @param {string} content
     *     The dataset file table-like content.
     */
    createFromFile(content) {
        const now = performance.now();
        console.info("Started creating a new graph");

        this.#parseDataChunk(content);

        // // Get the stream from the file.
        // const stream = file.stream();

        // // Get the default stream reader.
        // const reader = stream.getReader();

        // // Go through every character of the stream.
        // while (true) {
        //     // Get the result of reading the stream.
        //     const result = await reader.read();

        //     // Stop if there is nothing more to parse.
        //     if (result.done) {
        //         break;
        //     }

        //     // Get the decoded chunk of the graph data.
        //     const chunk = this.#text.decode(result.value);

        //     this.#parseDataChunk(chunk);
        // }

        // Calculate certain graph features.
        this.#calculateDensity();
        this.#doFullDFS();
        this.#calculateAssortativityCoefficient();
        this.#calculateClusteringCoefficient();
        this.#calculateSplitTime();

        // // Clean up the stream and the reader.
        // reader.cancel();

        console.info("Finished creating a new graph");

        // prettier-ignore
        console.info(
            `Time taken: (${Math.floor(performance.now() - now)}ms)`
        );
    }

    /**
     * Does a BFS from `fromNode` and goes until `toNode`, if it is provided.
     * Used to calculate
     * @param {object}  args
     *     The function arguments as an object.
     * @param {number}  args.fromNode
     *     The source node.
     * @param {number?} [args.toNode]
     *     The destination node.
     * @param {number?} [args.threshold]
     *     The number of visited nodes threshold.
     * @returns {Set<number>}
     *     The list of the visited nodes.
     */
    doBFSFrom({ fromNode, toNode = null, threshold = null }) {
        this.#distances.clear();

        // Create the markers of the visited nodes.

        /**
         * @type {Set<number>}
         */
        const visitedNodes = new Set();

        // Create the distances list for the source node.
        if (!this.#distances.has(fromNode)) {
            this.#distances.set(fromNode, new Map());
        }

        // Create the reference to the distances list
        // for the source node for easier access to it.
        const distances = /** @type {Map<number, number>} */ (
            this.#distances.get(fromNode)
        );

        // Create the queue for keeping the BFS paths.

        /**
         * @type {Queue<number>}
         */
        const bfsQueue = new Queue();
        bfsQueue.push(fromNode);
        visitedNodes.add(fromNode);
        distances.set(fromNode, 0);

        // Go until all nodes are explored.
        while (bfsQueue.peek() !== undefined) {
            // Get the node being currently explored.
            const currentNode = /** @type {number} */ (bfsQueue.pop());

            // Get the distance to the current node.
            const currentNodeDistance = /** @type {number} */ (
                distances.get(currentNode)
            );

            // Explore all the adjacent not-visited nodes.
            for (const [node] of /** @type {Map<number, Date[]>} */ (
                this.#adjacency.get(currentNode)
            )) {
                if (!visitedNodes.has(node)) {
                    bfsQueue.push(node);
                    visitedNodes.add(node);
                    distances.set(node, currentNodeDistance + 1);

                    // Exit if we have reached the destination node.
                    if (node === toNode) {
                        return visitedNodes;
                    }

                    // Exit if we have reached the threshold count.
                    if (threshold !== null) {
                        if (visitedNodes.size >= threshold) {
                            return visitedNodes;
                        }
                    }
                }
            }
        }

        return visitedNodes;
    }

    getResultDistance(fromNode, toNode) {
        return this.#distances.get(fromNode)?.get(toNode);
    }

    /**
     * Generates the vector of the features with the answers.
     * @returns {[number, number[], number[]][]}
     *     The vector of the features with the answers --- the first value
     *     is the answer, the second are the statical features and the third
     *     are the temporal features. The vector has 20,000 elements.
     */
    getFeaturesAnswers() {
        const now = performance.now();
        console.info("Started generating features / answers");

        /**
         * The result list that will accumulate our successful
         * positive attempts to generate.
         * @type {[number, number[], number[]][]}
         */
        const positiveResult = [];

        /**
         * The result list that will accumulate our successful
         * negative attempts to generate.
         * @type {[number, number[], number[]][]}
         */
        const negativeResult = [];

        // Get the nodes as an array, so we can get the random
        // node from it.
        const nodes = Array.from(this.#adjacency.keys());

        // Limit the amount of attempts to 25000, so we can
        // get the features and the answers as described in
        // the paper.
        for (let i = 0; i < this.#featureSelectionAttemptsNumber; ++i) {
            console.log(i, positiveResult.length, negativeResult.length);

            // If we have filled both lists, then everything
            // went successfully.
            if (
                negativeResult.length >= this.#featureSelectionEachSize &&
                positiveResult.length >= this.#featureSelectionEachSize
            ) {
                console.info("Finished generating features / answers");

                console.info(
                    `Time taken: (${Math.floor(performance.now() - now)}ms)`
                );

                return [...negativeResult, ...positiveResult];
            }

            // Get the random "root" node, which will create a
            // path between the two observed vector nodes.
            const rootNode =
                nodes[Math.floor(Math.random() * this.nodesNumber)];

            const rootNeighbors = Array.from(
                /** @type {Map<number, Date[]>} */ (
                    this.#adjacency.get(rootNode)
                ).keys()
            ).filter((value) => value !== rootNode);

            // Get the neighbors, that will be our nodes with
            // a distance of two between them.
            const firstNeighbor =
                rootNeighbors[Math.floor(Math.random() * rootNeighbors.length)];

            const secondNeighbor =
                rootNeighbors[Math.floor(Math.random() * rootNeighbors.length)];

            // If they are the same node, then the attempt
            // counts as a failed one.
            if (firstNeighbor === secondNeighbor) {
                continue;
            }

            const adjacent = /** @type {Map<number, Date[]>} */ (
                this.#adjacency.get(firstNeighbor)
            );

            // Check whether the nodes will not eventually
            // connect.
            if (!adjacent.has(secondNeighbor)) {
                // If we have already filled the negative
                // result list, go to the next attempt.
                if (negativeResult.length >= this.#featureSelectionEachSize) {
                    continue;
                }

                // Add the value to the negative result list.
                const staticFeatures = this.calculateStaticFeatures(
                    firstNeighbor,
                    secondNeighbor
                );

                const temporalFeatures = this.calculateTemporalFeatures(
                    firstNeighbor,
                    secondNeighbor
                );

                negativeResult.push([0, staticFeatures, temporalFeatures]);
                continue;
            }

            // Get whether the nodes are currently connected.
            const times = /** @type {Date[]} */ (adjacent.get(secondNeighbor));

            let areConnectedCurrently = false;

            for (let j = 0; j < times.length; ++j) {
                if (times[j] <= this.#splitTime) {
                    areConnectedCurrently = true;
                    break;
                }
            }

            // If they are currently connected, then the attempt
            // counts as a failed one, as we only need the ones
            // currently disconnected.
            if (areConnectedCurrently) {
                continue;
            }

            // If we already have filled the positive result list,
            // go to the next attempt.
            if (positiveResult.length >= this.#featureSelectionEachSize) {
                continue;
            }

            // Currenly, the only values left are the ones that
            // are not currently connected, but will eventually
            // connect.

            // Add the value to the positive result list.
            const staticFeatures = this.calculateStaticFeatures(
                firstNeighbor,
                secondNeighbor
            );

            const temporalFeatures = this.calculateTemporalFeatures(
                firstNeighbor,
                secondNeighbor
            );

            positiveResult.push([1, staticFeatures, temporalFeatures]);
        }

        console.error("Maximum number of attempts reached");
        console.error(`Generated positive outcomes: ${positiveResult.length}`);
        console.error(`Generated negative outcomes: ${negativeResult.length}`);
        return [];
    }

    /**
     * Adds the edge to `this.adjacency`.
     *
     * This operation modifies the graph, but a lot of graph properties are not
     * automatically recalculated. Do not forget to recalculate them manually.
     * @param {object}  args
     *     The function arguments as an object.
     * @param {number}  args.edgeFrom
     *     The edge source.
     * @param {number}  args.edgeTo
     *     The edge destination.
     * @param {Date}    args.edgeTime
     *     The edge creation time.
     * @param {boolean} [args.isReversed]
     *     Whether the edge is "reversed" ("backward" edge for a "forward" one).
     *     If so, it does not add to the edge counters, but still updates the
     *     node counter.
     */
    #addEdge({ edgeFrom, edgeTo, edgeTime, isReversed = false }) {
        // Update the earliest and the latest dates.
        if (!isReversed) {
            if (isNaN(this.#maxTime.getTime()) || edgeTime > this.#maxTime) {
                this.#maxTime = edgeTime;
            }

            if (isNaN(this.#minTime.getTime()) || edgeTime < this.#minTime) {
                this.#minTime = edgeTime;
            }
        }

        // Check for and consider the existense of loops.
        if (edgeFrom === edgeTo) {
            if (this.#loops.has(edgeFrom)) {
                const current = /** @type {number} */ (
                    this.#loops.get(edgeFrom)
                );

                this.#loops.set(edgeFrom, current + 1);
            } else {
                this.#loops.set(edgeFrom, 1);
            }
        }

        if (!this.#adjacency.has(edgeFrom)) {
            // Case: the adjacency list does not have such source
            // node yet.

            const nodeMap = new Map([[edgeTo, [edgeTime]]]);
            this.#adjacency.set(edgeFrom, nodeMap);
            ++this.nodesNumber;

            if (!isReversed) {
                ++this.uniqueEdgesNumber;
                ++this.edgesNumber;
            }
        } else if (
            !(
                /** @type {Map<number, Date[]>} */ (
                    this.#adjacency.get(edgeFrom)
                ).has(edgeTo)
            )
        ) {
            // Case: the adjacency list already has the source node,
            // but there is no destination node yet.

            /** @type {Map<number, Date[]>} */ (
                this.#adjacency.get(edgeFrom)
            ).set(edgeTo, [edgeTime]);

            if (!isReversed) {
                ++this.uniqueEdgesNumber;
                ++this.edgesNumber;
            }
        } else {
            // Case: the adjacency list already has such an edge, so
            // the edge currently added is a multiple one.

            /** @type {Date[]} */ (
                /** @type {Map<number, Date[]>} */ (
                    this.#adjacency.get(edgeFrom)
                ).get(edgeTo)
            ).push(edgeTime);

            if (!isReversed) {
                ++this.edgesNumber;
            }
        }

        if (!isReversed && edgeFrom !== edgeTo) {
            this.#addEdge({
                edgeTime,
                edgeFrom: edgeTo,
                edgeTo: edgeFrom,
                isReversed: true,
            });
        }
    }

    /**
     * Calculates `this.assortativityCoefficient` of this graph.
     */
    #calculateAssortativityCoefficient() {
        // Initialize with zeros.
        let r1 = 0n;
        let r2 = 0n;
        let r3 = 0n;
        let re = 0n;

        // Go through every node.
        for (const [node, adjacent] of this.#adjacency) {
            if (this.#loops.has(node)) {
                r1 += BigInt((adjacent.size + 1) ** 1);
                r2 += BigInt((adjacent.size + 1) ** 2);
                r3 += BigInt((adjacent.size + 1) ** 3);
            } else {
                r1 += BigInt(adjacent.size ** 1);
                r2 += BigInt(adjacent.size ** 2);
                r3 += BigInt(adjacent.size ** 3);
            }

            // Go through every node adjacent to it.
            for (const [adjacentNode] of adjacent) {
                const adjacentNodeSize = /** @type {Map<number, Date[]>} */ (
                    this.#adjacency.get(adjacentNode)
                ).size;

                if (this.#loops.has(node) && this.#loops.has(adjacentNode)) {
                    re += BigInt((adjacent.size + 1) * (adjacentNodeSize + 1));
                } else if (this.#loops.has(node)) {
                    re += BigInt((adjacent.size + 1) * adjacentNodeSize);
                } else if (this.#loops.has(adjacentNode)) {
                    re += BigInt(adjacent.size * (adjacentNodeSize + 1));
                } else {
                    re += BigInt(adjacent.size * adjacentNodeSize);
                }
            }
        }

        // Calculate the final value.
        this.assortativityCoefficient =
            Number(re * r1 - r2 ** 2n) / Number(r3 * r1 - r2 ** 2n);
    }

    /**
     * Calculates `this.clusteringCoefficient` of this graph.
     */
    #calculateClusteringCoefficient() {
        // Go through every node in the largest component.
        this.largestWCC.forEach((node) => {
            // For now, just count the sum of the local clustering
            // coefficients.
            this.clusteringCoefficient +=
                this.calculateLocalClusteringCoefficient(node);
        });

        // "Mean" the sum of the local clustering coefficients.
        if (this.largestWCC.length !== 0) {
            this.clusteringCoefficient /= this.largestWCC.length;
        }
    }

    /**
     * Calculates `this.density` of the graph.
     */
    #calculateDensity() {
        // Calculate the max value as if the graph is directed.
        const maxDirected = this.nodesNumber * (this.nodesNumber - 1);

        // Use the fraction formula to calculate the density.
        this.density = (2 * this.uniqueEdgesNumber) / maxDirected;
    }

    /**
     * Calculates the time at which the temporal network is split.
     */
    #calculateSplitTime() {
        const elapsedTime = this.#maxTime.getTime() - this.#minTime.getTime();

        this.#splitTime = new Date(
            this.#minTime.getTime() + this.#split * elapsedTime
        );
    }

    /**
     * Calculates the features of `lsubWCC`.
     * @param {number[]} subWCC
     *     The subgraph of the weakly connected component of the graph.
     * @return {GraphWCCFeatures}
     *     The result diameter, radius and 90-percentile.
     */
    #calculateSubWCCFeatures(subWCC) {
        this.#distanceNumbers.clear();
        this.#maxDistances.clear();

        // Go through each of the nodes.
        subWCC.forEach((fromNode) => {
            this.doBFSFrom({ fromNode });

            // Get the result distances from the source node.
            const results = /** @type {Map<number, number>} */ (
                this.#distances.get(fromNode)
            );

            // Update the maximum distance from the source node.
            for (const [_, result] of results) {
                this.#updateMaxDistances({ fromNode, result });
                this.#updateDistanceNumbers({ result });
            }
        });

        return this.#calculateWCCFeatures();
    }

    /**
     * Calculates the features associated with a weakly connected component
     * of a graph using `args.maxDistances` and `args.distanceNumbers`.
     * @returns {GraphWCCFeatures}
     *     The result diameter, radius and 90-percentile.
     */
    #calculateWCCFeatures() {
        // Create the variable for the diameter.
        let diameter = 0;

        // Create the variable for the radius.
        let radius = Infinity;

        // Find the diameter and the radius.
        for (const [_, distance] of this.#maxDistances) {
            if (diameter < distance) {
                diameter = distance;
            }

            if (radius > distance) {
                radius = distance;
            }
        }

        // Sort the final distance numbers for counting percentile.
        const sortedDistanceNumbers = Array.from(this.#distanceNumbers).sort(
            (a, b) => a[0] - b[0]
        );

        // Calculate the total number of distances in the distance numbers.
        const distancesNumber = sortedDistanceNumbers.reduce(
            (sum, [_, number]) => sum + number,
            0
        );

        // Set the index of the 90th percentile in the sorted distances
        // list.
        const percentileIndex = 0.9 * (distancesNumber - 1) + 1;

        // Set the index of the 90th percentile in the sorted distances
        // list (whole part).
        let percentileIndexWhole = Math.floor(percentileIndex);

        // Set the index of the 90th percentile in the sorted distances
        // list (fractional part).
        const percentileIndexFractional = percentileIndex % 1;

        // Calculate the 90th percentile based on its position in the list.
        for (let i = 0; ; ++i) {
            percentileIndexWhole -= sortedDistanceNumbers[i][1];

            if (percentileIndexWhole < 0) {
                return {
                    diameter,
                    radius,
                    percentile: sortedDistanceNumbers[i][0],
                };
            }

            if (percentileIndexWhole == 0) {
                return {
                    diameter,
                    radius,
                    percentile:
                        sortedDistanceNumbers[i][0] +
                        percentileIndexFractional *
                            (sortedDistanceNumbers[i + 1][0] -
                                sortedDistanceNumbers[i][0]),
                };
            }
        }
    }

    /**
     * Does a full DFS through the graph. Also, while doing DFS, finds the
     * weakly connected components of the graph, the largest one and its
     * relative size.
     */
    #doFullDFS() {
        // Create the markers of the visited nodes.

        /**
         * @type {Set<number>}
         */
        const visitedNodes = new Set();

        // Visit every node at least once.
        for (const [nodeToVisit] of this.#adjacency) {
            // No need to visit what is visited.
            if (visitedNodes.has(nodeToVisit)) {
                continue;
            }

            // Create the current weakly connected component.
            const currentWCC = [nodeToVisit];

            // Create the stack for keeping the DFS paths.
            const dfsStack = [nodeToVisit];
            visitedNodes.add(nodeToVisit);

            // Go until all nodes are explored.
            while (dfsStack.length !== 0) {
                // Get the node being currently explored.
                const currentNode = /** @type {number} */ (dfsStack.pop());

                // Explore all the adjacent not-visited nodes.
                for (const [node] of /** @type {Map<number, Date[]>} */ (
                    this.#adjacency.get(currentNode)
                )) {
                    if (!visitedNodes.has(node)) {
                        dfsStack.push(node);
                        visitedNodes.add(node);
                        currentWCC.push(node);
                    }
                }
            }

            // Add the weakly connected component to the list.
            this.wccs.push(currentWCC.sort((a, b) => a - b));

            // Update the largest weakly connected component.
            if (currentWCC.length >= this.largestWCC.length) {
                this.largestWCC = currentWCC;
            }
        }

        // Calculate the relative size of the largest weakly
        // connected component.
        const largestWCCLength = this.largestWCC.length;
        this.largestWCCRelativeSize = largestWCCLength / this.nodesNumber;
    }

    /**
     * Parses `chunk` of the table-like graph data.
     * @param {string} chunk
     *     The chunk of the table-like graph data.
     */
    #parseDataChunk(chunk) {
        for (const character of chunk) {
            // Skip the comment lines.
            if (this.#parserComments.includes(character)) {
                this.#parserState.isLineSkipped = true;
                continue;
            }

            // Switch to the new line.
            if (this.#parserNewlines.includes(character)) {
                if (
                    this.#parserState.currentEdgeFrom !== null &&
                    this.#parserState.currentEdgeTo !== null &&
                    this.#parserState.readBuffer !== ""
                ) {
                    // Parse the current edge creation timestamp.
                    const currentEdgeTimestamp =
                        1000 * Number(this.#parserState.readBuffer);

                    this.#addEdge({
                        edgeFrom: this.#parserState.currentEdgeFrom,
                        edgeTo: this.#parserState.currentEdgeTo,
                        edgeTime: new Date(currentEdgeTimestamp),
                    });
                }

                this.#resetParserState();
                continue;
            }

            // Skip if in the skipped line.
            if (this.#parserState.isLineSkipped) {
                continue;
            }

            // Add the character to the buffer.
            if (!this.#parserDelimiters.includes(character)) {
                this.#parserState.isDelimiterBefore = false;
                this.#parserState.readBuffer += character;
                continue;
            }

            // Skip the extra delimiters.
            if (!this.#parserState.isDelimiterBefore) {
                this.#switchParserStateToNextColumn();
            }
        }
    }

    /**
     * Resets `this.parserState` to defaults.
     */
    #resetParserState() {
        this.#parserState.currentEdgeFrom = null;
        this.#parserState.currentEdgeTo = null;
        this.#parserState.currentColumnState = GraphParserColumnState.from;
        this.#parserState.isLineSkipped = false;
        this.#parserState.isDelimiterBefore = false;
        this.#parserState.readBuffer = "";
    }

    /**
     * Switches `this.parserState` over to the next column and also parses
     * and saves the current column. It is assumed that this function is
     * called when the current character is the delimiter.
     */
    #switchParserStateToNextColumn() {
        switch (this.#parserState.currentColumnState) {
            case GraphParserColumnState.from:
                this.#parserState.currentEdgeFrom = Number(
                    this.#parserState.readBuffer
                );

                this.#parserState.currentColumnState =
                    GraphParserColumnState.to;
                break;
            case GraphParserColumnState.to:
                this.#parserState.currentEdgeTo = Number(
                    this.#parserState.readBuffer
                );

                this.#parserState.currentColumnState =
                    GraphParserColumnState.weight;
                break;
            case GraphParserColumnState.weight:
                this.#parserState.currentColumnState =
                    GraphParserColumnState.timestamp;
        }

        // Do assume that the current character is the delimiter.
        this.#parserState.isDelimiterBefore = true;

        // Do not forget to empty the buffer for the next column.
        this.#parserState.readBuffer = "";
    }

    /**
     * Updates the maximum distance from `fromNode`.
     * @param {object} args
     *     The function arguments as an object.
     * @param {number} args.fromNode
     *     The source node.
     * @param {number} args.result
     *     The result distance.
     */
    #updateMaxDistances({ fromNode, result }) {
        if (
            !this.#maxDistances.has(fromNode) ||
            /** @type {number} */ (this.#maxDistances.get(fromNode)) < result
        ) {
            this.#maxDistances.set(fromNode, result);
        }
    }

    /**
     * Updates the number of distance that was encountered.
     * @param {object} args
     *     The function arguments as an object.
     * @param {number} args.result
     *     The result distance.
     */
    #updateDistanceNumbers({ result }) {
        if (this.#distanceNumbers.has(result)) {
            this.#distanceNumbers.set(
                result,
                /** @type {number} */ (this.#distanceNumbers.get(result)) + 1
            );
        } else {
            this.#distanceNumbers.set(result, 1);
        }
    }
}

////////////////////////////////////////////////////////////////////////////////
//// The technical / Node.js part                                           ////
////////////////////////////////////////////////////////////////////////////////

/**
 * @param {string} [setName]
 */
const nodeGenerateFeaturesAnswers = (setName = "null") => {
    const fs = require("fs");
    const graph = new Graph();

    graph.createFromFile(fs.readFileSync(`sets/${setName}`).toString());

    fs.writeFileSync(
        `data/${setName}.json`,
        JSON.stringify({ features: graph.getFeaturesAnswers() })
    );
};

/**
 * @param {string} [setName]
 * @returns {Graph}
 */
const nodeCreateGraphInstance = (setName = "null", dirName = "sets") => {
    const fs = require("fs");
    const graph = new Graph();

    graph.createFromFile(fs.readFileSync(`${dirName}/${setName}`).toString());
    return graph;
};

/**
 * @param {string} [setName]
 * @returns {Graph}
 */
const nodeGenerateGraphInformation = (
    setName = "null",
    dirName = "sets",
    wccFeatures = {}
) => {
    const fs = require("fs");
    const graph = new Graph();

    graph.createFromFile(fs.readFileSync(`${dirName}/${setName}`).toString());
    graph.calculateLargestWCCFeatures(wccFeatures);

    {
        const { largestWCCRelativeSize } = graph;

        // prettier-ignore
        console.info(
            "========================================" +
            "========================================"
        );

        // prettier-ignore
        console.info(
            `Nodes number:                         ${graph.nodesNumber}`
        );

        // prettier-ignore
        console.info(
            `Edges number:                         ${graph.edgesNumber}`
        );

        // prettier-ignore
        console.info(
            `Unique edges number:                  ${graph.uniqueEdgesNumber}`
        );

        // prettier-ignore
        console.info(
            `Density:                              ${graph.density}`
        );

        // prettier-ignore
        console.info(
            `WCCs number:                          ${graph.wccs.length}`
        );

        // prettier-ignore
        console.info(
            `LWCC size:                            ${graph.largestWCC.length}`
        );

        // prettier-ignore
        console.info(
            `LWCC relative size:                   ${largestWCCRelativeSize}`
        );
    }

    if (graph.largestWCCFeatures) {
        const { diameter, radius, percentile } = graph.largestWCCFeatures;

        // prettier-ignore
        console.info(
            `LWCC exact                d / r / p:  ${diameter} ` +
                `${radius} ${percentile}`
        );
    }

    graph.largestWCCFeatures1000Random.forEach((feature) => {
        // prettier-ignore
        console.info(
            `LWCC estimated (random)   d / r / p:  ${feature.diameter} ` +
                `${feature.radius} ${feature.percentile}`
        );
    });

    graph.largestWCCFeatures1000Snowball.forEach((feature) => {
        // prettier-ignore
        console.info(
            `LWCC estimated (snowball) d / r / p:  ${feature.diameter} ` +
                `${feature.radius} ${feature.percentile}`
        );
    });

    {
        const { clusteringCoefficient, assortativityCoefficient } = graph;

        // prettier-ignore
        console.info(
            `LWCC average clustering coefficient:  ${clusteringCoefficient}`
        );

        // prettier-ignore
        console.info(
            `Assortativity coefficient:            ${assortativityCoefficient}`
        );

        // prettier-ignore
        console.info(
            "========================================" +
            "========================================"
        );
    }

    return graph;
};

if (module) {
    module.exports = {
        Graph,
        nodeCreateGraphInstance,
        nodeGenerateFeaturesAnswers,
        nodeGenerateGraphInformation,
    };
}
