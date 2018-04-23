import * as React from 'react'
import ReactDOM from 'react-dom'

import {
  InstantSearch,
  SearchBox,
  Hits,
  Index
} from 'react-instantsearch/dom';
import key from 'keyboard-shortcut';


class Search extends React.Component {

  componentWillMount(){
    key('escape', this.onEscape)
  }

  onEscape() {
    document.body.classList.toggle('searching', false)
  }

  onSearch() {
    document.body.classList.toggle('searching', true)
  };

  render() {
    const language = window.language_code;
    const chapterIndexName = `dev_GDRPR_chapters_${language}`;
    const articlesIndexName = `dev_GDRPR_articles_${language}`;
    const sectionsIndexName = `dev_GDRPR_sections_${language}`;
    const recitalsIndexName = `dev_GDRPR_recitals_${language}`;

    return (
      <InstantSearch
        appId="OA3O0E2RHO"
        apiKey="9c1dd06a40440adc4e7a50d485bd46d5"
        indexName={chapterIndexName}
      >
        <SearchBox
          onFocus={this.onSearch.bind(this)}
          translations={{
            'placeholder': 'Search in chapters, articles, recitals, …'
          }}
        />
        <div className="search-results">
          <Hits />
          <Index indexName={articlesIndexName}>
            <Hits />
          </Index>
          <Index indexName={sectionsIndexName}>
            <Hits />
          </Index>
          <Index indexName={recitalsIndexName}>
            <Hits />
          </Index>
        </div>
				<a onClick={this.onEscape.bind(this)} className="search-escape">
          <i className="fa fa-times" /><br/>esc
        </a>
      </InstantSearch>
    )
  }
}

const element = <Search name="test" />;
ReactDOM.render(
  element,
  document.getElementById('search')
);
