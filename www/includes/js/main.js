pageElements.DeviceListController = null;
pageElements.APListController = null;
pageElements.errorController = null;

var queuedAjaxRequests = [];

function addAjaxRequest(request)
{
	queuedAjaxRequests.push(request);
}

function sendAjax()
{
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function()
	{
		if (this.readyState == 4 && this.status == 200)
		{
			onAjaxResponse(this.responseText);
		}
	}
	
	var parameters = "i=" + JSON.stringify(queuedAjaxRequests);
	xhttp.open("POST", "includes/ajaxHelper.php", true)
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(parameters)

	// Clear the ajax queue;
	queuedAjaxRequests = [];	
}

function onAjaxResponse(results)
{
	var responseObj = JSON.parse(results);
	
//	console.log(responseObj);
	for (x in responseObj)
	{
		var obj = responseObj[x];
		
		if (typeof(obj.error) != 'undefined' && obj.error.length > 0)
			pageElements.errorController.setError(obj.error);
		
		var result = obj.result;
		eval(obj.callback);
		
	}
}

function onMainTabChange(event, ui)
{
	var btnText = ui["newTab"]["context"]["textContent"]; 
//	console.log(btnText);
	
	if (btnText == "Devices")
	{
		pageElements.gMapController.moveMapToDiv(document.getElementById("DeviceList-Map"));
		pageElements.gMapController.setPinSet(pageElements.DeviceListController.getPinList() );
	}
	else if (btnText == "Access Points")
	{
		pageElements.gMapController.moveMapToDiv(document.getElementById("APList-Map"));
		pageElements.gMapController.setPinSet(pageElements.APListController.getPinList() );
	}
}
