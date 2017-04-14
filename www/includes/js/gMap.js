function gMap()
{
	this.currentPins = [];
	this.currentPinData = [];
}

gMap.prototype.init = function()
{
	this.mapDiv = document.getElementById("gMapDiv");
	
	var center = {lat: 0, lng: 0};
    map = new google.maps.Map(this.mapDiv, {
      zoom: 2,
      center: center
    });
    
//    console.log("Done with init, about to set pins");
    
    if (this.currentPins.length > 0)
    	this.setPinSet(this.currentPinData);
}


gMap.prototype.setPinSet = function(array)
{
	// Remove markers from map
//	console.log("removing all markers");
	for (x in this.currentPins)
	{
//		console.log(this.currentPins[x]);
		this.currentPins[x].setMap(null);
	}
		
	this.currentPins = [];
	
	this.currentPinData = [];
	
	for (x in array)
	{
		this.currentPinData.push(array[x]);
		this.addPin(array[x].Latitude, array[x].Longitude);
	}
}

gMap.prototype.addPin = function(latitude, longitude)
{
	if (latitude == null || longitude == null)
		return;
	
	var newPin = {lat: latitude, lng: longitude};
	var marker = new google.maps.Marker({
        position: newPin,
        map: map
      });
	marker.addListener('click', function() {
//        map.setZoom(8);
//        map.setCenter(marker.getPosition());
		console.log("Clicked on marker... at " + latitude + ", " + longitude);
      });
	this.currentPins.push(marker);
}

gMap.prototype.moveMapToDiv = function(div)
{
	this.mapDiv.parentNode.removeChild(this.mapDiv);
	div.appendChild(this.mapDiv);
	this.init();
}