'use strict';

var filterableListControl = require( '../shared_objects/filterable-list-control' );

function SublandingFilterablePage() {

  Object.assign( this, filterableListControl );

  this.gotoURL = function(url='/sfp') {
    browser.get(url);
  };

  this.results = element.all(by.css('.o-post-preview_content'));
  this.first_result = this.results.first();
  this.last_result = this.results.last();
}

module.exports = SublandingFilterablePage;
