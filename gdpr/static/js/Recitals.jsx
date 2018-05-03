import React, { Component } from "react";

import { Snippet } from "react-instantsearch/dom";
import { connectHits } from "react-instantsearch/connectors";

class RecitalsHits extends Component {
  render() {
    const { hits } = this.props;
    return (
      <div className="recital-hits">
        {hits.map(hit => {
          return (
            <div className="row chapter-row">
              <div className="col-1">
                <p className="recital-index">{hit.index}</p>
              </div>
              <div className="col-11">
                <p className="recital-content">
                  <a
                    href="#"
                    data-toggle="modal"
                    data-target={`#recital-${hit.index}`}
                  >
                    <Snippet hit={hit} attribute="text" />
                  </a>
                </p>
                <div
                  className="modal fade"
                  tabIndex="-1"
                  role="dialog"
                  aria-labelledby={`recital-${hit.index}-title`}
                  aria-hidden="true"
                  id={`recital-${hit.index}`}
                >
                  <div className="modal-dialog modal-lg">
                    <div className="modal-content">
                      <div className="modal-header">
                        <h5
                          className="modal-title"
                          id={`recital-${hit.index}-title`}
                        >
                          Recital #{hit.index}
                        </h5>
                        <button
                          type="button"
                          className="close"
                          data-dismiss="modal"
                          aria-label="Close"
                        >
                          <span aria-hidden="true">&times;</span>
                        </button>
                      </div>
                      <div className="modal-body">
                        <p>{hit.text}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
        {!hits.length && (
          <div className="chapter-row">
            <p className="recital-index">
              <i>No results</i>
            </p>
          </div>
        )}
      </div>
    );
  }
}

const ConnectedRecitals = connectHits(RecitalsHits);

export default ConnectedRecitals;
