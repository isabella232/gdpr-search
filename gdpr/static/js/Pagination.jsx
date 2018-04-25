import * as React from 'react';

import {
	connectPagination
} from 'react-instantsearch/connectors';

class Pagination extends React.Component {

	canGoNext(){
		const { nbPages, currentRefinement } = this.props;
		return nbPages > currentRefinement;
	}

	canGoPrev(){
		const { currentRefinement } = this.props;
		return currentRefinement > 1;
	}

	goNext(){
		const { refine, currentRefinement } = this.props;
		if (this.canGoNext()) {
			refine(currentRefinement + 1)
		}
	}

	goPrev(){
		const { refine, currentRefinement } = this.props;
		if (this.canGoPrev()) {
			refine(currentRefinement - 1)
		}
	}

	render() {
		const { nbPages, currentRefinement, offset } = this.props;
		return (
			<div className="row">
				{(nbPages > 1) &&
					<div className={`col-9 offset-md-${offset}`}>
						<div className="pagination">
							<div className="pagination-pages">
								<a onClick={() => this.goPrev()} className={this.canGoPrev() ? '' : 'disabled'}>
									<i className="fa fa-arrow-left"/>
								</a>
								<a onClick={() => this.goNext()} className={this.canGoNext() ? '' : 'disabled'}>
									<i className="fa fa-arrow-right"/>
								</a>
							</div>
							<div className="pagination-status">
								{currentRefinement} - {nbPages}
							</div>
						</div>
					</div>
				}
			</div>
		)
	}
}

const ConnectedPagination = connectPagination(Pagination);

export default ConnectedPagination;
