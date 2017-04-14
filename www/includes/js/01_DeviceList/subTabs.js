function DeviceList_subTabs()
{
	$( ".DeviceSubTabBtn" ).button();
	this.activateTab(document.querySelector(".DeviceSubTabBtn"));
	this.hiddenDivDisplay = "";
}

DeviceList_subTabs.prototype.activateTab = function(btn)
{
	var btnList = document.querySelectorAll(".DeviceSubTabBtn");
	for (x in btnList)
		$( "#" +btnList[x].id ).button( "enable" );

	var toVisibleContent = null;
	var toHideContent = null;
	if (btn.textContent == "Details")
	{
		toVisibleContent = "DeviceList-Details";
		toHideContent = "DeviceList-Map";
	}
	else if (btn.textContent == "Map")
	{
		toVisibleContent = "DeviceList-Map";
		toHideContent = "DeviceList-Details";
		pageElements.gMapController.init();
		pageElements.gMapController.setPinSet(pageElements.DeviceListController.getPinList());
	}
	var divToShow = document.getElementById(toVisibleContent)
	divToShow.style.display = this.hiddenDivDisplay;
	
	var divToHide = document.getElementById(toHideContent);
	this.hiddenDivDisplay = divToHide.style.display;
	if (this.hiddenDivDisplay.length = 0)
		this.hiddenDivDisplay = "initial";
	divToHide.style.display = "none";
	
	if (btn.textContent == "Map")
	{
		pageElements.gMapController.init();
	}
	
	$( "#" +btn.id ).button( "disable" );
}
