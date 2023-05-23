// @ts-check

/**
 * @file The non-heavy core and UI functions.
 */

/**
 * A custom root element.
 */
class RootElement extends HTMLElement {
  /**
   * Attaches `template` as a shadow DOM tree to self.
   * @param {HTMLTemplateElement} template
   *   The template element to attach.
   */
  attachTemplate(template) {
    this.attachShadow({ mode: "open" }).appendChild(
      template.content.cloneNode(true)
    );
  }
}

/**
 * A custom alert element.
 */
class AlertElement extends RootElement {
  constructor() {
    super();

    this.attachTemplate(
      /** @type {HTMLTemplateElement} */ (
        document.getElementById("alert-template")
      )
    );
  }
}

/**
 * Shows the alert of `type` with `text`.
 * @param {object} args
 *   The function alrguments as an object.
 * @param {string} args.type
 *   The alert type (error, info or warn).
 * @param {string?} args.text
 *   The text to display on the alert.
 */
const showAlert = ({ type = "info", text = null }) => {
  /**
   * The text element to "replace" the slot.
   */
  const textElement = document.createElement("span");

  // Set the passed alert properties.
  textElement.slot = "text";
  textElement.textContent = text;

  /**
   * The root element for the shadow DOM.
   */
  const rootElement = document.createElement(`stlp-${type}-alert`);

  // Add the created elements to the DOM.
  rootElement.appendChild(textElement);
  document.body.appendChild(rootElement);

  // Remove the alert after some time.
  setTimeout(HTMLElement.prototype.remove.bind(rootElement), 3000);
};

/**
 * The names of the graph worker functions.
 * @enum {string}
 * @type {Readonly<{ [key: string]: string }>}
 */
const workerNames = Object.freeze(
  ["createUndirectedTemporalGraph"].reduce(
    (obj, value) => ({ ...obj, [value]: value }),
    {}
  )
);

/**
 * The form used to send datasets.
 */
const datasetForm = /** @type {HTMLFormElement} */ (
  document.getElementById("dataset-form")
);

customElements.define(
  "stlp-error-alert",
  /**
   * A custom error alert element.
   */
  class ErrorAlertElement extends AlertElement {}
);

customElements.define(
  "stlp-info-alert",
  /**
   * A custom information alert element.
   */
  class InfoAlertElement extends AlertElement {}
);

customElements.define(
  "stlp-warn-alert",
  /**
   * A custom warning alert element.
   */
  class WarnAlertElement extends AlertElement {}
);

datasetForm.addEventListener("submit", (event) => {
  console.info("The dataset is submitted");
  event.preventDefault();

  /**
   * The worker for doing graph computations.
   */
  const worker = new Worker("/worker.js");

  /**
   * The submitted via the form dataset file.
   */
  const datasetFile = /** @type {File} */ (
    new FormData(datasetForm).get("dataset")
  );

  if (datasetFile.size === 0) {
    console.info("The dataset is empty");
    showAlert({ type: "error", text: "The dataset is empty" });
  } else {
    // Send the name and arguments to the worker.
    worker.postMessage([
      workerNames.createUndirectedTemporalGraph,
      datasetFile,
    ]);
  }

  // Recieve the function results from the worker.
  worker.addEventListener("message", (event) => {
    /**
     * The name of the executed function.
     * @type {string}
     */
    const name = event.data[0];

    /**
     * The result of the executed function.
     */
    const result = event.data[1];

    switch (name) {
      case workerNames.createUndirectedTemporalGraph:
      // TODO: add the next computation step
    }
  });
});
