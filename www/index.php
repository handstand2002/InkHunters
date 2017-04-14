<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<link rel="stylesheet" href="includes/jquery-ui-1.12.1/jquery-ui.css">
<script src="includes/jquery-ui-1.12.1/external/jquery/jquery.js"></script>
<script src="includes/jquery-ui-1.12.1/jquery-ui.js"></script>

<link rel="stylesheet" href="includes/css/verticalTabs.css">
<link rel="stylesheet" href="includes/css/error.css">
<link rel="stylesheet" href="includes/css/gMap.css">

<script src="includes/js/debugFunctionModifier.js"></script>
<script>
var pageElements = {};
pageElements.debugController = new debugFunctionModifier();
</script>

<script src="includes/js/main.js"></script>
<script src="includes/js/error.js"></script>
<script src="includes/js/gMap.js" ></script>

<script>
	pageElements.debugController.postLoadRun();

	$( function() {
		$( "#tabs" ).tabs({ activate: function( event, ui ) { onMainTabChange(event, ui); } }).addClass( "ui-tabs-vertical ui-helper-clearfix" );
		$( "#tabs li" ).removeClass( "ui-corner-top" ).addClass( "ui-corner-left" );
	} );

	pageElements.gMapController = new gMap();
</script>

</head>
<body>
	<div id="bottomError">
	</div>
	<script>
	// Move the errorDiv to get rid of the margin
	var errorDiv = document.getElementById("bottomError");
	errorDiv.style.marginLeft = ((errorDiv.offsetLeft+1)*-1) + "px";
	</script>


	<div style="width: 800px">
		<div id="tabs" style="height: 700px;">
		  <ul>
		    <li><a href="#tabs-1">Devices</a></li>
		    <li><a href="#tabs-2">Access Points</a></li>
		    <li><a href="#tabs-3">Server Info</a></li>
		  </ul>
		  <div id="tabs-1">
		    <?php include __DIR__."/includes/tab/01_DeviceList.php";?>
		  </div>
		  <div id="tabs-2">
		    <?php include __DIR__."/includes/tab/02_APList.php";?>
		  </div>
		  <div id="tabs-3">
		    <?php include __DIR__."/includes/tab/03_ServerInfo.php";?>
		  </div>
		</div>

	</div>
<?php include __DIR__."/includes/dialog/APAdd.php";?>
<?php include __DIR__."/includes/dialog/DeviceEdit.php";?>

<script>
pageElements.errorController = new errorDialog();
$( ".bubbleBtn" ).button();
</script>

<script 
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAV7dVwQ3cFxgDcXuFkuE7AGiO97eUPiZc&callback=pageElements.gMapController.init">
    </script>
<script>
pageElements.gMapController.setPinSet(pageElements.DeviceListController.getPinList() );
</script>

</body>
</html>
