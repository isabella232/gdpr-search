import * as React from 'react'
import {
  InstantSearch,
  SearchBox,
  Hits
} from 'react-instantsearch/dom';
import key from 'keyboard-shortcut';
import ReactDOM from 'react-dom'


class Search extends React.Component {

  componentWillMount(){
    key('escape', this.onEscape)
  }

  onEscape() {
    document.body.classList.toggle('searching', false)
  }

  onSearch(element) {
    document.body.classList.toggle('searching', true)
  };

  render() {
    return (
      <InstantSearch
        appId="OA3O0E2RHO"
        apiKey="9c1dd06a40440adc4e7a50d485bd46d5"
        indexName="dev_GDRPR_chapters_FR"
      >
        <SearchBox
          onKeyDown={this.onSearch.bind(this)}
          translations={{
            'placeholder': 'Search in chapters, articles, recitals, …'
          }}
        />
        <div className="search-results">
          <Hits />
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
