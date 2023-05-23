// @ts-check

/**
 * @file The worker for doing graph computations.
 */

/**
 * @typedef TemporalGraphEdge
 *   An edge of a temporal graph.
 * @property {number} weight
 *   An edge weight.
 * @property {Date} time
 *   An edge creation time.
 */

/**
 * @typedef {{ [to: number]: TemporalGraphEdge[] }}
 *   TemporalGraphAdjacency
 *   An adjacency of a temporal graph vertex.
 */

/**
 * @typedef {{ [from: number]: TemporalGraphAdjacency }}
 *   TemporalGraphAdjacencyList
 *   An adjacency list of a temporal graph.
 */

/**
 * @typedef UndirectedTemporalGraph
 *   An undirected temporal graph.
 * @property {TemporalGraphAdjacencyList} adjacency
 *   An adjacency list of a graph.
 * @property {number} edgesNumber
 *   A number of edges in a graph (counting multiple edges as one).
 * @property {number} edgesNumberMultiples
 *   A number of edges in a graph (counting multiple edges as many).
 * @property {number} verticesNumber
 *   A number of vertices in a graph.
 */

/**
 * What column is being read currently.
 * @enum {number}
 */
const currentlyReadingState = Object.freeze({
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
 * The decoder for the text.
 */
const textDecoder = new TextDecoder();

/**
 * Adds the edge to `adjacency`.
 * @param {object} args
 *   The function alrguments as an object.
 * @param {TemporalGraphAdjacencyList} args.adjacency
 *   The adjacency list of a temporal graph.
 * @param {number} args.from
 *   The edge source.
 * @param {number} args.to
 *   The edge destination.
 * @param {number} args.weight
 *   The edge weight.
 * @param {Date} args.time
 *   The edge creation time.
 */
const addTemporalGraphEdge = ({ adjacency, from, to, weight, time }) => {
  if (from in adjacency) {
    if (to in adjacency[from]) {
      adjacency[from][to].push({ weight, time });
    } else {
      adjacency[from][to] = [{ weight, time }];
    }
  } else {
    adjacency[from] = { [to]: [{ weight, time }] };
  }
};

/**
 * Creates the undirected temporal graph by parsing `file`.
 * @param {File} file
 *   The file to get the dataset from.
 * @returns {Promise<UndirectedTemporalGraph>}
 *   The created undirected temporal graph.
 */
const createUndirectedTemporalGraph = async (file) => {
  console.info("Started creating undirected temporal graph");

  /**
   * The freshly created graph.
   * @type {UndirectedTemporalGraph}
   */
  const graph = {
    adjacency: {},
    edgesNumber: 0,
    edgesNumberMultiples: 0,
    verticesNumber: 0,
  };

  /**
   * The stream from the file.
   */
  const stream = file.stream();

  /**
   * The default stream reader.
   */
  const reader = stream.getReader();

  /**
   * The current edge source.
   * @type {number?}
   */
  let currentEdgeFrom = null;

  /**
   * The current edge destination.
   * @type {number?}
   */
  let currentEdgeTo = null;

  /**
   * The current edge weight.
   * @type {number?}
   */
  let currentEdgeWeight = null;

  /**
   * The column being read currently.
   * @type {number}
   */
  let currentlyReading = currentlyReadingState.from;

  /**
   * Whether the current line is skipped.
   */
  let isLineSkipped = false;

  /**
   * Whether the character before was tab or space.
   */
  let isSpaceBefore = false;

  /**
   * The already read characters buffer.
   */
  let readBuffer = "";

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
     * The decoded as a string value of the result.
     */
    const data = textDecoder.decode(result.value);

    for (const character of data) {
      // Skip the comment line.
      if (character === "%") {
        isLineSkipped = true;
        continue;
      }

      // Switch over to the new line.
      if (character === "\r" || character === "\n") {
        if (
          currentEdgeFrom !== null &&
          currentEdgeTo !== null &&
          currentEdgeWeight !== null &&
          readBuffer !== ""
        ) {
          // Parse the last timestamp column.

          /**
           * The current edge creation timestamp.
           */
          const currentEdgeTimestamp = 1000 * Number(readBuffer);

          /**
           * The current edge creation time.
           */
          const currentEdgeTime = new Date(currentEdgeTimestamp);

          // Add the undirected edge to the list.
          addTemporalGraphEdge({
            adjacency: graph.adjacency,
            from: currentEdgeFrom,
            to: currentEdgeTo,
            weight: currentEdgeWeight,
            time: currentEdgeTime,
          });

          addTemporalGraphEdge({
            adjacency: graph.adjacency,
            from: currentEdgeTo,
            to: currentEdgeFrom,
            weight: currentEdgeWeight,
            time: currentEdgeTime,
          });
        }

        // Reset the values to defaults.
        currentEdgeFrom = null;
        currentEdgeTo = null;
        currentEdgeWeight = null;
        currentlyReading = currentlyReadingState.from;
        isLineSkipped = false;
        isSpaceBefore = false;
        readBuffer = "";

        continue;
      }

      // Skip if in the skipped line.
      if (isLineSkipped) {
        continue;
      }

      // Add the character to the buffer.
      if (character !== " " && character !== "\t") {
        isSpaceBefore = false;
        readBuffer += character;
        continue;
      }

      // Skip the extra tabs and spaces.
      if (isSpaceBefore) {
        continue;
      }

      // Switch over to the next column and parse the current one.
      switch (currentlyReading) {
        case currentlyReadingState.from:
          currentEdgeFrom = Number(readBuffer);
          currentlyReading = currentlyReadingState.to;
          break;
        case currentlyReadingState.to:
          currentEdgeTo = Number(readBuffer);
          currentlyReading = currentlyReadingState.weight;
          break;
        case currentlyReadingState.weight:
          currentEdgeWeight = Number(readBuffer);
          currentlyReading = currentlyReadingState.timestamp;
      }

      // The current character is either tab or space, so mark that.
      isSpaceBefore = true;

      // Do not forget to empty the buffer after switching columns.
      readBuffer = "";
    }
  }

  // Clean up the reader and the stream.
  reader.releaseLock();
  stream.cancel();

  console.info("Finished creating undirected temporal graph");
  console.info("The result graph is:", graph);

  return graph;
};

/**
 * The undirected temporal graph for this worker.
 * @type {UndirectedTemporalGraph?}
 */
let undirectedTemporalGraph = null;

/**
 * The functions that the worker implements.
 */
const functions = Object.freeze({});

self.addEventListener("message", async (event) => {
  /**
   * The name of the executed function.
   * @type {string}
   */
  const name = event.data.shift();

  console.info(`Called ${name} with:`, event.data);

  if (name === "createUndirectedTemporalGraph") {
    undirectedTemporalGraph = await createUndirectedTemporalGraph(
      event.data[0]
    );

    console.info(
      `${name} was called, so saving the result and sending nothing`
    );

    return postMessage([name, null]);
  }

  /**
   * The result of the executed function.
   */
  const result = await functions[name](...event.data);

  console.info(`Sending the result of ${name} back`);
  console.info("The function result is:", result);

  // Send the name and the result back.
  return postMessage([name, result]);
});
