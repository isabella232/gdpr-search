import * as React from 'react';

import {
	connectHits
} from 'react-instantsearch/connectors';
import {
  Highlight
} from 'react-instantsearch/dom';

class ChapterHits extends React.Component {
	render() {
		const { hits, onLinkClick } = this.props;
		const language = window.language_code;
		return (
			<div className="chapter-hits">
				{hits.map(hit => {
					return (
						<div className="row chapter-row">
							<div className="col-3">
								<span className="chapter-index">
									<a href={`${language === 'en' ? '' : '/' + language}/gdpr-article-${hit.first_article_id}`} onClick={onLinkClick}>
										Chap {hit.index}
									</a>
								</span>
							</div>
							<div className="col-9">
								<span className="chapter-name">
									<a href={`${language === 'en' ? '' : '/' + language}/gdpr-article-${hit.first_article_id}`} onClick={onLinkClick}>
										<Highlight attribute="name" hit={hit} />
									</a>
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
