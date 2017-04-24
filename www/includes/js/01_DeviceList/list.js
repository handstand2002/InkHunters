function DeviceList_List()
{
	this.fullList = [];
	this.table = document.getElementById("DeviceList-Table");
	
	var request = {};
	request.action = "DeviceGetList";
	request.parameters = {};
	request.callback = "pageElements.DeviceListController.populate(result)";
	this.ajaxGetList = request;
	
	request = {};
	request.action = "DeviceEdit";
	request.parameters = {};
	request.callback = "";
	this.ajaxEditDevice = request;
	
	request = {};
	request.action = "DeviceBuzzerStart";
	request.parameters = {};
	request.parameters.DeviceID = 0;
	request.parameters.Seconds = 10;
	this.ajaxStartBuzzer = request;
}

DeviceList_List.prototype.initList = function()
{
	addAjaxRequest(this.ajaxGetList);
	sendAjax();
}

DeviceList_List.prototype.getPinList = function()
{
	var output = [];
	
	for (x in this.fullList)
	{
		var item = {};
		item.Title = this.fullList[x].Title;
		item.Detail = this.fullList[x].Detail;
		item.Latitude = this.fullList[x].Latitude.INT;
		item.Longitude = this.fullList[x].Longitude.INT;
		item.Altitude = this.fullList[x].Altitude;
		output.push(item);
	}
	
	return output;
}

DeviceList_List.prototype.startBuzzer = function()
{
	var form = document.getElementById("Device_EditForm");
	
	this.ajaxStartBuzzer.parameters.DeviceID = form.DeviceID.value;
	
	addAjaxRequest(this.ajaxStartBuzzer);
	sendAjax();
}

DeviceList_List.prototype.openDiag = function(diagName, link)
{
	diagName = diagName.toUpperCase();
	
	switch (diagName)
	{
	case "EDITDEVICE":
		this.openEditDeviceDialog(link.parentNode.parentNode.data);
		break;
	}
}

DeviceList_List.prototype.openEditDeviceDialog = function(data)
{
	$("#Device_EditDialog").dialog("open");
	
	// Populate the fields
	var form = document.getElementById("Device_EditForm");
	
	form.DeviceID.value = data.DeviceID;
	form.Title.value = data.Title;
	form.MAC.value = data.MAC;
	form.LastTime.value = data.LastSeenTime;
	form.Latitude.value = data.Latitude.STRING;
	form.Longitude.value = data.Longitude.STRING;
	form.Altitude.value = data.Altitude;
	form.Details.value = data.Detail;
}

DeviceList_List.prototype.editDevice = function()
{
	var form = document.getElementById("Device_EditForm");
	
	var pars = {};
	pars.DeviceID = form.DeviceID.value;
	pars.Title = form.Title.value;
	pars.Details = form.Details.value
	this.ajaxEditDevice.parameters = pars;
	
	addAjaxRequest(this.ajaxEditDevice);
	addAjaxRequest(this.ajaxGetList);
	sendAjax();
}

DeviceList_List.prototype.populate = function(result)
{
	while (this.table.rows.length > 1)
		this.table.deleteRow(1);
	
	for (x in result)
	{
		var lat = result[x]["Latitude"]["STRING"];
		var long = result[x]["Longitude"]["STRING"];
		
		this.fullList.push(result[x]);
		var row = this.table.insertRow(-1);
		row.data = result[x];
		
		var cell = row.insertCell(0);
		var link = document.createElement("a");
		cell.appendChild(link);
		link.href = "javascript:;";
		link.setAttribute("onclick", "pageElements.DeviceListController.openDiag('EditDevice', this)")
		var img = document.createElement("img");
		link.appendChild(img);
		img.src = "includes/img/EditBtn.png";
		img.width = 30;
		
		
		cell = row.insertCell(1);
		cell.appendChild(document.createTextNode(result[x]["Title"]));
		
		cell = row.insertCell(2);
		cell.appendChild(document.createTextNode(result[x]["LastSeenTime"]));
		
		cell = row.insertCell(3);
		var location = lat + ", " + long + " at " +result[x]["Altitude"] + "ft";
		cell.appendChild(document.createTextNode(location));
		
	}
}
