function APList_List()
{
	this.apDetails = {};
	this.table = document.getElementById("APList-Table");
	
	var request = {};
	request.action = "APGetList";
	request.parameters = {};
	request.callback = "pageElements.APListController.populate(result)";
	this.ajaxGetList = request;
	
	request = {};
	request.action = "APAdd";
	request.parameters = {};
	request.parameters.MAC = null;
	request.parameters.Detail = null;
	request.parameters.Location = null;
	request.parameters.Latitude = null;
	request.parameters.Longitude = null;
	request.parameters.Altitude = null;
	request.callback = "";
	this.ajaxAddAP = request;
	
	request = {};
	request.action = "APDelete";
	request.parameters = {};
	request.parameters.APID = null;
	request.callback = "";
	this.ajaxDeleteAP = request;
}

APList_List.prototype.initList = function()
{
	addAjaxRequest(this.ajaxGetList);
	sendAjax();
}

APList_List.prototype.getPinList = function()
{
	var output = [];
	
	for (x in this.apDetails)
	{
		var item = {};
		item.Title = this.apDetails[x].LocationDescription;
		item.Detail = this.apDetails[x].Detail;
		item.Latitude = this.apDetails[x].Latitude.INT;
		item.Longitude = this.apDetails[x].Longitude.INT;
		item.Altitude = this.apDetails[x].Altitude;
		
		output.push(item);
	}
	
//	console.log(this.apDetails);
	return output;
}


APList_List.prototype.populate = function(result)
{
	while (this.table.rows.length > 1)
		this.table.deleteRow(1);
	
	this.apDetails = {};
	
	for (x in result)
	{
		this.apDetails[result[x]["APID"]] = result[x];
//		console.log(result[x]);
		var row = this.table.insertRow(-1);
		
		var cell = row.insertCell(0);
		var delLink = document.createElement("a");
		delLink.href = "javascript:;";
		delLink.APID = result[x]["APID"];
		delLink.setAttribute("onclick", "pageElements.APListController.deleteAP(this)");
		var delImg = document.createElement("img");
		delImg.src = "includes/img/DelBtn.png";
		delImg.width = "30";
		
		delLink.appendChild(delImg);
		cell.appendChild(delLink);
		
		var editLink = document.createElement("a");
		editLink.href = "javascript:;";
		editLink.APID = result[x]["APID"];
		editLink.setAttribute("onclick", "pageElements.APListController.editAP(this)" );
		var editImg = document.createElement("img");
		editImg.src = "includes/img/EditBtn.png";
		editImg.width = "30";
		
		editLink.appendChild(editImg);
		cell.appendChild(editLink);
		
		cell = row.insertCell(1);
		cell.appendChild(document.createTextNode(result[x]["LocationDescription"]));
		
		cell = row.insertCell(2);
		cell.appendChild(document.createTextNode(result[x]["MAC"]));
		
		cell = row.insertCell(3);
		cell.appendChild(document.createTextNode(result[x]["Detail"]));
	}
	
	var row = this.table.insertRow(-1);
	
	var cell = row.insertCell(0);
	cell.colSpan = "4";
	cell.style.textAlign = "center";
	
	var img = document.createElement("img");
	img.src = "includes/img/AddBtn.png";
	img.height = "38";
	
	var link = document.createElement("a");
	link.href = "javascript:;";
	link.setAttribute("onclick", "pageElements.APListController.OpenAddAPDialog()");
	link.appendChild(img);
	
	cell.appendChild(link);
}

APList_List.prototype.OpenAddAPDialog = function()
{
	var form = document.getElementById("APAddForm");
	form.APID.value = "";
	form.MAC.value = "";
	form.Details.value = "";
	form.Location.value = "";
	form.Latitude.value = "";
	form.Longitude.value = "";
	form.Altitude.value = "";
	
	$("#APAddDialog").dialog("open");
}

APList_List.prototype.addAP = function()
{
	var form = document.getElementById("APAddForm");
	var request = this.ajaxAddAP;
	
	request.parameters.APID = form.APID.value;
	request.parameters.MAC = form.MAC.value;
	request.parameters.Detail = form.Details.value;
	request.parameters.Location = form.Location.value;
	request.parameters.Latitude = form.Latitude.value;
	request.parameters.Longitude = form.Longitude.value;
	request.parameters.Altitude = form.Altitude.value;
	
	addAjaxRequest(request);
	addAjaxRequest(this.ajaxGetList);
	sendAjax();
	
}

APList_List.prototype.deleteAP = function(link)
{
	this.ajaxDeleteAP.parameters.APID = link.APID;
	
	addAjaxRequest(this.ajaxDeleteAP);
	addAjaxRequest(this.ajaxGetList);
	sendAjax();
}

APList_List.prototype.editAP = function(link)
{
	$("#APAddDialog").dialog("open");
	
	var details = this.apDetails[link.APID];
	
	var form = document.getElementById("APAddForm");
	form.APID.value = details.APID;
	form.MAC.value = details.MAC;
	form.Details.value = details.Detail;
	form.Location.value = details.LocationDescription;
	form.Latitude.value = details.Latitude.STRING;
	form.Longitude.value = details.Longitude.STRING;
	form.Altitude.value = details.Altitude;
}
