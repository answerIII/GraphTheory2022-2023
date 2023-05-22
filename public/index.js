// @ts-check

/**
 * @typedef STLPGraphEdge An edge of a graph, with additional attached data.
 * @property {number} to An edge destination.
 * @property {number} weight An edge weight.
 * @property {number} time An edge creation time.
 */

/** @typedef {Set<STLPGraphEdge>[]} STLPGraph A graph as an edge list. */

/** A custom element. */
class STLPElement extends HTMLElement {
  /**
   * Attaches `template` as a shadow DOM tree to this element.
   * @param {HTMLTemplateElement} template The template element to attach.
   */
  attachTemplate(template) {
    this.attachShadow({ mode: "open" }).appendChild(
      template.content.cloneNode(true)
    );
  }
}

/** A custom alert element. */
class STLPAlertElement extends STLPElement {
  constructor() {
    super();

    this.attachTemplate(
      /** @type {HTMLTemplateElement} */ (
        document.getElementById("stlp-alert-template")
      )
    );
  }
}

customElements.define(
  "stlp-error-alert",
  /** A custom error alert element. */
  class STLPErrorAlertElement extends STLPAlertElement {}
);

customElements.define(
  "stlp-info-alert",
  /** A custom information alert element. */
  class STLPInfoAlertElement extends STLPAlertElement {}
);

customElements.define(
  "stlp-warn-alert",
  /** A custom warning alert element. */
  class STLPWarnAlertElement extends STLPAlertElement {}
);

/**
 * Parses `datasetFile` and returns the graph from it.
 * @param {File} datasetFile The uploaded file with the data.
 * @returns {Promise<STLPGraph>} The graph as the edge list.
 */
const stlpParseDataset = async (datasetFile) => {
  const graph = [];
  const textDecoder = new TextDecoder();
  let line = "";

  // @ts-ignore 2504 It has the async iterator.
  for await (const chunk of datasetFile.stream()) {
    const data = textDecoder.decode(chunk);

    for (const character of data) {
      if (character !== "\r" && character !== "\n") {
        line += character;
        continue;
      }

      if (line !== "" && !line.startsWith("%")) {
        // TODO: Parse the line (maybe no line accumulator?)
      }

      line = "";
    }
  }

  return graph;
};

/**
 * Shows the alert of `type` with `text`.
 * @param type {string} The alert type (error, info or warn).
 * @param text {string} The text to display on the alert.
 */
const stlpShowAlert = (type, text) => {
  const textElement = document.createElement("span");
  textElement.slot = "text";
  textElement.textContent = text;

  const hostElement = document.createElement(`stlp-${type}-alert`);
  hostElement.appendChild(textElement);
  document.body.appendChild(hostElement);

  setTimeout(HTMLElement.prototype.remove.bind(hostElement), 2500);
};

const datasetForm = /** @type {HTMLFormElement} */ (
  document.getElementById("dataset-form")
);

datasetForm.addEventListener("submit", (event) => {
  console.info("The dataset is submitted");
  event.preventDefault();

  const datasetForm = /** @type {HTMLFormElement} */ (event.target);

  const datasetFile = /** @type {File} */ (
    new FormData(datasetForm).get("dataset")
  );

  if (datasetFile.size === 0) {
    stlpShowAlert("error", "The dataset is empty");
  } else {
    stlpParseDataset(datasetFile);
  }
});
