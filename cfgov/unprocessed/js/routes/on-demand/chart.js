/* ==========================================================================
   Scripts for Line Chart molecule.
   ========================================================================== */

'use strict';

var atomicHelpers = require( '../../modules/util/atomic-helpers' );
var Chart = require( '../../molecules/Chart' );

atomicHelpers.instantiateAll( '.m-chart_graphics', Chart );
