/*
 Template Name: Zoter - Bootstrap 4 Admin Dashboard
 Author: Mannatthemes
 File: Google Maps Integration with Django Incident Data
*/

(function ($) {
  "use strict";

  var GoogleMap = function () {};

  /**
   * Create map with dynamic incident markers
   * @param {string} $container - ID or selector for the map div
   */
  GoogleMap.prototype.createMarkers = function ($container) {
    // Initialize map centered on Bangladesh
    var map = new GMaps({
      div: $container,
      lat: 23.6943117,
      lng: 90.344352,
      zoom: 6
    });

    // Check if INCIDENT_DATA is defined and add markers
    if (typeof INCIDENT_DATA !== 'undefined' && INCIDENT_DATA.length > 0) {
      INCIDENT_DATA.forEach(function (incident) {
        // Add marker
        map.addMarker({
          lat: incident.lat,
          lng: incident.lng,
          title: incident.title,
          infoWindow: {
            content: `
              <div style="max-width: 250px;">
                <h6>${incident.title}</h6>
                <p>${incident.description || ''}</p>
                <p><strong>Date:</strong> ${incident.date}</p>
              </div>
            `
          }
        });
      });

      // Center and fit bounds if multiple markers
      if (INCIDENT_DATA.length > 1) {
        var bounds = [];
        INCIDENT_DATA.forEach(function (incident) {
          bounds.push([incident.lat, incident.lng]);
        });
        map.fitLatLngBounds(bounds);
      }
      // Single marker? Center on it
      else if (INCIDENT_DATA.length === 1) {
        map.setCenter(INCIDENT_DATA[0].lat, INCIDENT_DATA[0].lng);
        map.setZoom(10);
      }
    } else {
      console.log("No incident data found for map.");
    }

    return map;
  };

  // Main initializer
  GoogleMap.prototype.init = function () {
    var $this = this;

    $(document).ready(function () {
      // Initialize the map with dynamic markers
      $this.createMarkers('#gmaps-markers');
    });
  };

  // Initialize
  $.GoogleMap = new GoogleMap();
  $.GoogleMap.Constructor = GoogleMap;
})(window.jQuery);

// Automatically start
(function ($) {
  "use strict";
  $.GoogleMap.init();
})(window.jQuery);
