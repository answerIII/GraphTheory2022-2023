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
     * The number of experiments to do for the estimation of features
     * of the largest weakly connected component.
     * @readonly
     */
    #largestWCCFeaturesExperimentsNumber = 1;

    /**
     * The size of the subgraph to use for the estimation of features
     * of the largest weakly connected component.
     * @readonly
     */
    #largestWCCFeaturesSubgraphSize = 500;

    /**
     * The threshold for doing the exact calculation of features of the
     * largest weakly connected component.
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
     * Creates a new graph by parsing `file`.
     * @param {File} file
     *     The file with the table-like graph data.
     */
    async createFromFile(file) {
        console.info("Started creating a new graph");

        // Get the stream from the file.
        const stream = file.stream();

        // Get the default stream reader.
        const reader = stream.getReader();

        // Go through every character of the stream.
        while (true) {
            // Get the result of reading the stream.
            const result = await reader.read();

            // Stop if there is nothing more to parse.
            if (result.done) {
                break;
            }

            // Get the decoded chunk of the graph data.
            const chunk = this.#text.decode(result.value);

            this.#parseDataChunk(chunk);
        }

        // Calculate certain graph features.
        this.#calculateDensity();
        this.#doFullDFS();
        this.#calculateLargestWCCFeatures();
        this.#calculateClusteringCoefficient();

        // Clean up the stream and the reader.
        reader.cancel();

        console.info("Finished creating a new graph");
        console.info("The result graph is:", this);

        return graph;
    }

    /**
     * Adds the edge to `this.adjacency`.
     *
     * This operation modifies the graph, but a lot of graph properties are not
     * automatically recalculated. Do not forget to recalculate them manually.
     * @param {object} args
     *     The function arguments as an object.
     * @param {number} args.edgeFrom
     *     The edge source.
     * @param {number} args.edgeTo
     *     The edge destination.
     * @param {Date}   args.edgeTime
     *     The edge creation time.
     * @param {boolean} [args.isReversed]
     *     Whether the edge is "reversed" ("backward" edge for a "forward" one).
     *     If so, it does not add to the edge counters, but still updates the
     *     node counter.
     */
    #addEdge({ edgeFrom, edgeTo, edgeTime, isReversed = false }) {
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

        if (!isReversed) {
            this.#addEdge({
                edgeTime,
                edgeFrom: edgeTo,
                edgeTo: edgeFrom,
                isReversed: true,
            });
        }
    }

    /**
     * Calculates `this.clusteringCoefficient` of this graph.
     */
    #calculateClusteringCoefficient() {
        // Go through every node in the largest component.
        this.largestWCC.forEach((node) => {
            // Get the neighbors of this node.
            const neighbors = Array.from(
                /** @type {Map<number, Date[]>} */ (
                    this.#adjacency.get(node)
                ).keys()
            );

            // Less than two neighbors will not do anything.
            if (neighbors.length < 2) {
                return;
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

            // For now, just count the sum of the node clustering
            // coefficients.
            this.clusteringCoefficient +=
                (2 * neighborEdgesNumber) /
                (neighbors.length * (neighbors.length - 1));
        });

        // "Mean" the sum of the node clustering coefficients.
        if (this.nodesNumber !== 0) {
            this.clusteringCoefficient /= this.nodesNumber;
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
     * Calculates the features (or estimates their values) of the largest
     * weakly connected component of the graph.
     */
    #calculateLargestWCCFeatures() {
        // Use the threshold for the exact calculation.
        if (this.largestWCC.length <= this.#largestWCCFeaturesThreshold) {
            console.info("Started the exact calculation");

            this.largestWCCFeatures = this.#calculateSubWCCFeatures(
                this.largestWCC
            );

            console.info("Finished the exact calculation");
        }

        for (let i = 0; i < this.#largestWCCFeaturesExperimentsNumber; ++i) {
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

                this.#doBFSFrom({ fromNode, toNode });

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
                this.#doBFSFrom({
                    fromNode: initialNode,
                    threshold: this.#largestWCCFeaturesSubgraphSize,
                })
            );

            // Add the result to the "snowball" experiments vector.
            this.largestWCCFeatures1000Snowball.push(
                this.#calculateSubWCCFeatures(nodeSample)
            );

            console.info(`Finished the experiment (snowball) #${i + 1}`);
        }
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
            this.#doBFSFrom({ fromNode });

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
    #doBFSFrom({ fromNode, toNode = null, threshold = null }) {
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

/////////////////////
//// WORKER PART ////
/////////////////////

/**
 * The graph associated with this worker.
 * @type {Graph?}
 */
let graph = null;

/**
 * The functions that the worker implements.
 */
const funcs = Object.freeze({});

self.addEventListener("message", async ({ data: { name, args } }) => {
    console.info(`Called ${name} with:`, args);

    switch (name) {
        case "createGraphFromFile":
            // When creating a graph, it might have huge size,
            // so do not send it back and save it internally.
            graph = new Graph();
            await graph.createFromFile(args);

            console.info(`${name} was called, sending nothing`);
            return postMessage({ name, result: null });
        default:
            // Get the result of the executed function.
            const result = await funcs[name](...args);

            console.info(`Sending the result of ${name} back`);
            console.info("The function result is:", result);
            return postMessage({ name, result });
    }
});
