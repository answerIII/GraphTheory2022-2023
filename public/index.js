// @ts-check

/** A custom element. */
class GraphElement extends HTMLElement {
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
class GraphAlertElement extends GraphElement {
  constructor() {
    super();

    this.attachTemplate(
      /** @type {HTMLTemplateElement} */ (
        document.getElementById("graph-alert-template")
      )
    );
  }
}

customElements.define(
  "graph-error-alert",
  /** A custom error alert element. */
  class GraphErrorAlertElement extends GraphAlertElement {}
);

customElements.define(
  "graph-info-alert",
  /** A custom information alert element. */
  class GraphInfoAlertElement extends GraphAlertElement {}
);

customElements.define(
  "graph-warn-alert",
  /** A custom warning alert element. */
  class GraphWarnAlertElement extends GraphAlertElement {}
);
