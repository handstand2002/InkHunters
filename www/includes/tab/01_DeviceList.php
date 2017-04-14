<script src="includes/js/01_DeviceList/list.js"></script>
<script src="includes/js/01_DeviceList/subTabs.js"></script>

<h2>Devices</h2>
<button class="bubbleBtn DeviceSubTabBtn" id="DeviceList-btnDetails" onclick="pageElements.DeviceSubTabController.activateTab(this)">Details</button>
<button class="bubbleBtn DeviceSubTabBtn" id="DeviceList-btnMap" onclick="pageElements.DeviceSubTabController.activateTab(this)">Map</button>

<div id="DeviceList-Details">
	<p>
		<table id="DeviceList-Table">
			<tr>
				<th></th>
				<th>Title</th>
				<th>Last-Seen Time</th>
				<th>Last Location</th>
			</tr>
		</table>
	</p>
</div>

<div id="DeviceList-Map">
	<div id="gMapDiv"></div>
</div>

<script>
pageElements.DeviceListController = new DeviceList_List();
pageElements.DeviceListController.initList();
//window.setInterval("pageElements.DeviceListController.initList()", 5000);

pageElements.DeviceSubTabController = new DeviceList_subTabs();

</script>

<style>
#DeviceList-Table { border-collapse:collapse; }
#DeviceList-Table tr:nth-child(even) { background-color: #ccc; }
#DeviceList-Table tr:first-child th { border-bottom: 2px solid black; }
#DeviceList-Table tr th, #DeviceList-Table tr td { padding: 10px; }
</style>
