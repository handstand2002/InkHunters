function ServerInfoPageController()
{
	this.table = document.getElementById("ServerInfo-Table");
	
	var request = {};
	request.action = "ServerGetInfo";
	request.parameters = {};
	request.callback = "pageElements.ServerInfoPageController.populate(result)";
	this.ajaxGetInfo = request;
}

ServerInfoPageController.prototype.initList = function()
{
	addAjaxRequest(this.ajaxGetInfo);
	sendAjax();
}

ServerInfoPageController.prototype.populate = function(result)
{
	while (this.table.rows.length > 0)
		this.table.deleteRow(0);
	
	for (x in result)
	{
		var row = this.table.insertRow(-1);
		
		var cell = row.insertCell(0);
		cell.appendChild(document.createTextNode(x));
		
		cell = row.insertCell(1);
		cell.appendChild(document.createTextNode(result[x]));
		
	}
}
