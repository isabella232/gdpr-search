import * as React from 'react';

import {
  Highlight
} from 'react-instantsearch/dom';
import {
	connectHits
} from 'react-instantsearch/connectors';


class SectionHits extends React.Component {
	render() {
		const { hits, onLinkClick } = this.props;
		const language = window.language_code;
		return (
			<div className="section-hits">
				{hits.map(hit => {
					return (
						<div className="section-row">
							<p className="chapter-info">
								<Highlight hit={hit} attribute="chapter__label" />. <Highlight hit={hit} attribute="chapter__name" />
							</p>
							<p className="article-info">
								<a href={`${language === 'en' ? '' : '/' + language}/gdpr-article-${hit.article__index}`}>
									<Highlight hit={hit} attribute="article__label" />. <Highlight hit={hit} attribute="article__name" />
								</a>
							</p>
							<div className="section-content">
								<div className="section-index">{hit.index}.</div>
								<div>
									<a href={`${language === 'en' ? '' : '/' + language}/gdpr-article-${hit.article__index}#section-${hit.index}`} onClick={onLinkClick}>
										<Highlight hit={hit} attribute="content" />
									</a>
								</div>
							</div>
						</div>
					)
				})}
				{!hits.length &&
					<div className="section-row">
						<p className="section-index">
							<i>No results</i>
						</p>
					</div>
				}
			</div>
		)
	}
}

const ConnectedSections = connectHits(SectionHits);

export default ConnectedSections;
