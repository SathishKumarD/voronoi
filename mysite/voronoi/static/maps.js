var map;
var infowindow;
var marker;
var markers = []

var UB_south_location = {
    lat: 42.954511,
    lng: -78.820139
}
var global_houses;
var selected_houseId;


$('.dropdownfilter').on('hide.bs.dropdown', function () {
    refreshResults();
})

var populatePageFunc = function populatePage(results){
        houseMarkSuccess(results.map_data);
        populateResults(results.search_data);
    }

function refreshResults(){
    clearMarkers();
    getHouses(populatePageFunc);
}


function getResultsUrl(){
    var results_url = "/voronoi/get_search_json/";
    var rent = $("input[name='rent']").val();
    var bus_stop_time = $("input[name='bus_stop_time']").val();
    var address = $("#search2").val();
    url = results_url+"?address="+address+"&rent="+rent+"&bus_stop_time="+bus_stop_time;
    return url;
}


function initmap2() {
    map = new google.maps.Map(document.getElementById('map'), {
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: new google.maps.LatLng(UB_south_location.lat, UB_south_location.lng),
        zoom: 15
    });
    infowindow = new google.maps.InfoWindow();
    getHouses(populatePageFunc);
}

function getMarkerContent(house) {
    var markerhtml = '';
    markerhtml += "<a href=" + house.id + ">" + house.address.split(",")[0] + "</a>";
    markerhtml += '</br> Rating: 4';
    markerhtml += '</br> Bus stop: ' +  Math.round(house.bus_stop_distance *10)/10 + ' miles';
    markerhtml += '</br>' + house.bus_stop_time.toString().concat(' minutes walk');
    markerhtml += '</br>';
    return markerhtml;
}

function populateResults(houses){
    $('#results').html(houses);
}

function houseMarkSuccess(houses) {
    // console.log(houses);
    var allbounds = new google.maps.LatLngBounds();
    var circle = {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: 'red',
        fillOpacity: .4,
        scale: 7,
        strokeColor: 'white',
        strokeWeight: 1
    };

    var circle_house = {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: 'green',
        fillOpacity: .4,
        scale: 7,
        strokeColor: 'white',
        strokeWeight: 1
    };

    var i;
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(UB_south_location.lat, UB_south_location.lng),
        icon: circle,
        map: map
    });

    for (i = 0; i < houses.length; i++) {
        // console.log(houses[i]);
        allbounds.extend(new google.maps.LatLng(houses[i].latitude, houses[i].longitude))
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(houses[i].latitude, houses[i].longitude),
            icon: circle_house,
            map: map
        });

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {

                houses[i].markerContent = getMarkerContent(houses[i]);
                infowindow.setContent(houses[i].markerContent);
                infowindow.open(map, marker);
                houses[i].marker = marker;
                // setHouseDetails(houses[i]);
                //selected_houseId = houses[i].houseId;
            }
        })(marker, i));
        markers.push(marker);
    }
    map.fitBounds(allbounds);
}

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}


// get the search filter object
function getFilterObject(){
  var filterObj = {};
  filterObj.address = $('#search2').val();
  if (!filterObj.address){
    filterObj.address='e';
  }
  filterObj.rent= $("input[name='rent']").val();
  filterObj.bus_stop_time= $("input[name='bus_stop_time']").val();
  var name = $('#searchType').attr('name');
  if(name) {
    filterObj['name'] = $('#searchType').val();
  }
  return filterObj;
}


function getHouses(populatePageFunc) {

    var dataObj = getFilterObject();
    console.log(dataObj);
    dataObj['csrfmiddlewaretoken'] = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: "GET",
        url: getResultsUrl(),
        data: dataObj,
        success: populatePageFunc,
        error: function(XMLHttpRequest, textStatus, errorThrown) {
        },
        dataType: 'json'
    });
}


