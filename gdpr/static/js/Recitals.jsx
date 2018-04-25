import * as React from 'react';

import {
  Snippet
} from 'react-instantsearch/dom';
import {
	connectHits
} from 'react-instantsearch/connectors';

class RecitalsHits extends React.Component {
	render() {
		const { hits } = this.props;
		return (
			<div className="recital-hits">
				{hits.map(hit => {
					return (
						<div className="row chapter-row">
							<div className="col-1">
								<p className="recital-index">
									{hit.index}
								</p>
							</div>
							<div className="col-11">
								<p className="recital-content">
									<Snippet hit={hit} attribute="text" />
								</p>
							</div>
						</div>
					)
				})}
				{!hits.length &&
					<div className="chapter-row">
						<p className="recital-index">
							<i>No results</i>
						</p>
					</div>
				}
			</div>
		)
	}
}

const ConnectedRecitals = connectHits(RecitalsHits);

export default ConnectedRecitals;
