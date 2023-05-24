// @ts-check

/**
 * @file The worker for doing graph computations.
 */

/**
 * @typedef GraphEdge
 *   An edge of a graph.
 * @property {number?} weight
 *   An edge weight.
 * @property {Date?}   time
 *   An edge creation time.
 */

/**
 * @typedef {{ [to: number]: GraphEdge[] }}     GraphAdjacent
 *   An adjacency of a graph vertex.
 * @typedef {{ [from: number]: GraphAdjacent }} GraphAdjacency
 *   An adjacency list of a graph.
 * @typedef {number[]}                          GraphComponent
 *   A component of a graph.
 * @typedef {GraphComponent[]}                  GraphComponents
 *   A list of components of a graph.
 */

/**
 * @typedef Graph
 *   A generic graph representation.
 * @property {boolean}         isDirected
 *   Whether a graph is directed or not.
 * @property {GraphAdjacency}  adjacency
 *   An adjacency list of a graph.
 * @property {GraphAdjacency?} reversedAdjacency
 *   A "reversed" adjacency list for a directed graph.
 * @property {number}          edgesNumber
 *   A number of edges in a graph (counting multiple edges as many).
 * @property {number}          uniqueEdgesNumber
 *   A number of edges in a graph (counting multiple edges as one).
 * @property {number}          verticesNumber
 *   A number of vertices in a graph.
 * @property {number}          density
 *   A density charcteristic of a graph.
 * @property {GraphComponents} wcc
 *   A list of weakly connected components of a graph.
 * @property {GraphComponent}  largestWCC
 *   A largest weakly connected component of a graph.
 */

/**
 * @typedef GraphParserState
 *   A state of a graph parser.
 * @property {number?}                currentEdgeFrom
 *   A current edge source.
 * @property {number?}                currentEdgeTo
 *   A current edge destination.
 * @property {number?}                currentEdgeWeight
 *   A current edge weight.
 * @property {GraphParserColumnState} currentColumnState
 *   A column being read currently.
 * @property {boolean}                isLineSkipped
 *   Whether a current line is skipped.
 * @property {boolean}                isDelimiterBefore
 *   Whether a character before was a delimiter.
 * @property {string}                 readBuffer
 *   An already read characters buffer.
 */

/**
 * An error when functionality is not implemented.
 */
class UnimplementedError extends Error {
  /**
   * @param {string} [message]
   *   The additional error message.
   */
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
  }
}

/**
 * The state of a column being read.
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
   * The third column (the edge weight).
   */
  weight: 3,

  /**
   * The fourth column (the edge creation timestamp).
   */
  timestamp: 4,
});

/**
 * The characters that are treated by the graph parser as comments.
 */
const graphParserComments = "%";

/**
 * The characters that are treated by the graph parser as delimiters.
 */
const graphParserDelimiters = " \t";

/**
 * The characters that are treated by the graph parser as newlines.
 */
const graphParserNewlines = "\r\n";

/**
 * The decoder for the text.
 */
const textDecoder = new TextDecoder("utf-8");

/**
 * Adds the edge to `args.graph.adjacency`.
 *
 * This operation modifies the graph, but the following properties are NOT
 * automatically recalculated: `density`, `wcc`, `largestWCC`. Do not forget
 * to recalculate them manually.
 * @param {object}  args
 *   The function arguments as an object.
 * @param {Graph}   args.graph
 *   The graph itself.
 * @param {number}  args.edgeFrom
 *   The edge source.
 * @param {number}  args.edgeTo
 *   The edge destination.
 * @param {number}  args.edgeWeight
 *   The edge weight.
 * @param {Date}    args.edgeTime
 *   The edge creation time.
 * @param {boolean} [args.isReversed]
 *   Whether the edge is "reversed" ("backward" edge for a "forward" one).
 *   If so, it does not add to the edge counters, but still updates the
 *   vertex counter.
 */
const addGraphEdge = ({
  graph,
  edgeFrom,
  edgeTo,
  edgeWeight,
  edgeTime,
  isReversed = false,
}) => {
  // prettier-ignore
  /**
   * The "reversed" adjacency list.
   */
  const reversedAdjacency =
    /** @type {GraphAdjacency} */ (
      graph.reversedAdjacency
    );

  // prettier-ignore
  /**
   * The adjacency list for the edge.
   */
  const adjacency =
    isReversed && graph.isDirected
      ? reversedAdjacency
      : graph.adjacency;

  /**
   * A new edge added to the graph.
   * @type {GraphEdge}
   */
  const edge = {
    weight: edgeWeight,
    time: edgeTime,
  };

  if (!(edgeFrom in adjacency)) {
    adjacency[edgeFrom] = { [edgeTo]: [edge] };

    if (
      !graph.isDirected ||
      (isReversed && !(edgeFrom in graph.adjacency)) ||
      (!isReversed && !(edgeFrom in reversedAdjacency))
    ) {
      ++graph.verticesNumber;
    }

    if (!isReversed) {
      ++graph.uniqueEdgesNumber;
      ++graph.edgesNumber;
    }
  } else if (!(edgeTo in adjacency[edgeFrom])) {
    adjacency[edgeFrom][edgeTo] = [edge];

    if (!isReversed) {
      ++graph.uniqueEdgesNumber;
      ++graph.edgesNumber;
    }
  } else {
    adjacency[edgeFrom][edgeTo].push(edge);

    if (!isReversed) {
      ++graph.edgesNumber;
    }
  }

  if (!isReversed) {
    addGraphEdge({
      graph,
      edgeWeight,
      edgeTime,
      edgeFrom: edgeTo,
      edgeTo: edgeFrom,
      isReversed: true,
    });
  }
};

/**
 * Calculates the density of the graph.
 * @param {Graph} graph
 *   The graph itself.
 */
const calculateGraphDensity = (graph) => {
  if (graph.isDirected) {
    graph.density =
      (1 * graph.uniqueEdgesNumber) /
      (graph.verticesNumber * (graph.verticesNumber - 1));
  } else {
    graph.density =
      (2 * graph.uniqueEdgesNumber) /
      (graph.verticesNumber * (graph.verticesNumber - 1));
  }
};

/**
 * Creates a new state of a graph parser.
 * @returns {GraphParserState}
 *   The result state of the graph parser.
 */
const createGraphParserState = () => {
  return {
    currentEdgeFrom: null,
    currentEdgeTo: null,
    currentEdgeWeight: null,
    currentColumnState: GraphParserColumnState.from,
    isLineSkipped: false,
    isDelimiterBefore: false,
    readBuffer: "",
  };
};

/**
 * Does DFS through the graph as if it is undirected. Also, while doing
 * DFS, finds the weakly connected components of the graph.
 * @param {Graph} graph
 *   The graph itself.
 */
const doGraphUndirectedDFS = (graph) => {
  /**
   * The markers of the visited vertices.
   */
  const visitedVertices = Object.fromEntries(
    Object.keys(graph.adjacency).map((value) => [value, false])
  );

  // Visit every vertex at least once.
  for (const visitedVertexKey in visitedVertices) {
    // No need to visit what is visited.
    if (visitedVertices[visitedVertexKey]) {
      continue;
    }

    /**
     * The current weakly connected component.
     * @type {number[]}
     */
    const currentWCC = [Number(visitedVertexKey)];

    /**
     * The stack for keeping the DFS paths.
     */
    const dfsStack = [visitedVertexKey];
    visitedVertices[visitedVertexKey] = true;

    // Go until all vertices are explored.
    while (dfsStack.length !== 0) {
      /**
       * The vertex being currently explored.
       */
      const currentVertex = /** @type {string} */ (dfsStack.pop());

      // Explore all the adjacent vertices.
      for (const vertexKey in graph.adjacency[currentVertex]) {
        if (!visitedVertices[vertexKey]) {
          dfsStack.push(vertexKey);
          visitedVertices[vertexKey] = true;
          currentWCC.push(Number(vertexKey));
        }
      }

      // Explore all the "reversed" adjacent vertices.
      if (graph.reversedAdjacency !== null) {
        for (const vertexKey in graph.reversedAdjacency[currentVertex]) {
          if (!visitedVertices[vertexKey]) {
            dfsStack.push(vertexKey);
            visitedVertices[vertexKey] = true;
            currentWCC.push(Number(vertexKey));
          }
        }
      }
    }

    // Add the weakly connected component to the list.
    graph.wcc.push(currentWCC);

    // Update the largest weakly connected component.
    if (currentWCC.length >= graph.largestWCC.length) {
      graph.largestWCC = currentWCC;
    }
  }
};

/**
 * Resets `graphParserState` to defaults.
 * @param {GraphParserState} graphParserState
 *   The state of the graph parser.
 */
const resetGraphParserState = (graphParserState) => {
  graphParserState.currentEdgeFrom = null;
  graphParserState.currentEdgeTo = null;
  graphParserState.currentEdgeWeight = null;
  graphParserState.currentColumnState = GraphParserColumnState.from;
  graphParserState.isLineSkipped = false;
  graphParserState.isDelimiterBefore = false;
  graphParserState.readBuffer = "";
};

/**
 * Switches the state of the graph parser over to the next column and also
 * parses and saves the current column. It is assumed that this function is
 * called when the current character is the delimiter.
 * @param {GraphParserState} graphParserState
 *   The state of the graph parser.
 */
const switchGraphParserStateToNextColumn = (graphParserState) => {
  switch (graphParserState.currentColumnState) {
    case GraphParserColumnState.from:
      graphParserState.currentEdgeFrom = Number(graphParserState.readBuffer);
      graphParserState.currentColumnState = GraphParserColumnState.to;
      break;
    case GraphParserColumnState.to:
      graphParserState.currentEdgeTo = Number(graphParserState.readBuffer);
      graphParserState.currentColumnState = GraphParserColumnState.weight;
      break;
    case GraphParserColumnState.weight:
      graphParserState.currentEdgeWeight = Number(graphParserState.readBuffer);
      graphParserState.currentColumnState = GraphParserColumnState.timestamp;
  }

  // Assume that the current character is the delimiter.
  graphParserState.isDelimiterBefore = true;

  // Do not forget to empty the buffer for the next column.
  graphParserState.readBuffer = "";
};

/**
 * Parses `args.chunk` of the graph data.
 * @param {object}           args
 *   The function arguments as an object.
 * @param {string}           args.chunk
 *   The chunk of the table-like graph data.
 * @param {Graph}            args.graph
 *   The graph that is being populated.
 * @param {GraphParserState} args.graphParserState
 *   The state of the graph parser.
 */
const parseGraphDataChunk = ({ chunk, graph, graphParserState }) => {
  for (const character of chunk) {
    // Skip the comment lines.
    if (graphParserComments.includes(character)) {
      graphParserState.isLineSkipped = true;
      continue;
    }

    // Switch to the new line.
    if (graphParserNewlines.includes(character)) {
      if (
        graphParserState.currentEdgeFrom !== null &&
        graphParserState.currentEdgeTo !== null &&
        graphParserState.currentEdgeWeight !== null &&
        graphParserState.readBuffer !== ""
      ) {
        // Parse the last timestamp column.

        // prettier-ignore
        /**
         * The current edge creation timestamp.
         */
        const currentEdgeTimestamp =
          1000 * Number(graphParserState.readBuffer);

        addGraphEdge({
          graph,
          edgeFrom: graphParserState.currentEdgeFrom,
          edgeTo: graphParserState.currentEdgeTo,
          edgeWeight: graphParserState.currentEdgeWeight,
          edgeTime: new Date(currentEdgeTimestamp),
        });
      }

      resetGraphParserState(graphParserState);
      continue;
    }

    // Skip if in the skipped line.
    if (graphParserState.isLineSkipped) {
      continue;
    }

    // Add the character to the buffer.
    if (!graphParserDelimiters.includes(character)) {
      graphParserState.isDelimiterBefore = false;
      graphParserState.readBuffer += character;
      continue;
    }

    // Skip the extra delimiters.
    if (!graphParserState.isDelimiterBefore) {
      switchGraphParserStateToNextColumn(graphParserState);
    }
  }
};

/**
 * Creates a new graph by parsing `args.file`.
 * @param {object}  args
 *   The function arguments as an object.
 * @param {File}    args.file
 *   The file with the table-like graph data.
 * @param {boolean} [args.isDirected]
 *   Whether the graph is directed or not.
 * @returns {Promise<Graph>}
 *   The result graph.
 */
const createGraphFromFile = async ({ file, isDirected = false }) => {
  console.info("Started creating a new graph");

  /**
   * The freshly created graph.
   * @type {Graph}
   */
  const graph = {
    isDirected,
    adjacency: {},
    reversedAdjacency: null,
    edgesNumber: 0,
    uniqueEdgesNumber: 0,
    verticesNumber: 0,
    density: 0,
    wcc: [],
    largestWCC: [],
  };

  if (isDirected) {
    graph.reversedAdjacency = {};
  }

  /**
   * The stream from the file.
   */
  const stream = file.stream();

  /**
   * The default stream reader.
   */
  const reader = stream.getReader();

  /**
   * The state of the graph parser.
   */
  const graphParserState = createGraphParserState();

  // Go through every character of the stream.
  while (true) {
    /**
     * The result of reading the stream.
     */
    const result = await reader.read();

    // Stop if there is nothing more to parse.
    if (result.done) {
      break;
    }

    /**
     * The decoded chunk of the graph data.
     */
    const chunk = textDecoder.decode(result.value);

    parseGraphDataChunk({
      chunk,
      graph,
      graphParserState,
    });
  }

  // Calculate the graph characteristics.
  calculateGraphDensity(graph);
  doGraphUndirectedDFS(graph);

  // Clean up the stream and the reader.
  reader.cancel();

  console.info("Finished creating a new graph");
  console.info("The result graph is:", graph);

  return graph;
};

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
      graph = await createGraphFromFile(args);

      console.info(`${name} was called, sending nothing`);
      return postMessage({ name, result: null });
    default:
      /**
       * The result of the executed function.
       */
      const result = await funcs[name](...args);

      console.info(`Sending the result of ${name} back`);
      console.info("The function result is:", result);
      return postMessage({ name, result });
  }
});
