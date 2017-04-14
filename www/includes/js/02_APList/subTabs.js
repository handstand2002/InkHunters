function APList_subTabs()
{
	$( ".APSubTabBtn" ).button();
	this.activateTab(document.querySelector(".APSubTabBtn"));
	this.hiddenDivDisplay = "";
}

APList_subTabs.prototype.activateTab = function(btn)
{
	var btnList = document.querySelectorAll(".APSubTabBtn");
	for (x in btnList)
		$( "#" +btnList[x].id ).button( "enable" );

	var toVisibleContent = null;
	var toHideContent = null;
	if (btn.textContent == "Details")
	{
		toVisibleContent = "APList-Details";
		toHideContent = "APList-Map";
	}
	else if (btn.textContent == "Map")
	{
		toVisibleContent = "APList-Map";
		toHideContent = "APList-Details";
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
