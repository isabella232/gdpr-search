import * as React from 'react';

import {
	connectHits
} from 'react-instantsearch/connectors';
import {
  Highlight
} from 'react-instantsearch/dom';

class ChapterHits extends React.Component {
	render() {
		const { hits } = this.props;
		return (
			<div className="chapter-hits">
				{hits.map(hit => {
					return (
						<div className="row chapter-row">
							<div className="col-3">
								<span className="chapter-index">
									Chap {hit.index}
								</span>
							</div>
							<div className="col-9">
								<span className="chapter-name">
									<Highlight attribute="name" hit={hit} />
								</span>
							</div>
						</div>
					)
				})}
				{!hits.length &&
					<div className="chapter-row">
						<p className="chapter-name">
							<i>No results</i>
						</p>
					</div>
				}
			</div>
		)
	}
}

const ConnectedChapters = connectHits(ChapterHits);

export default ConnectedChapters;
