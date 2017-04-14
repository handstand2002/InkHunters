<script src="includes/js/02_APList/list.js"></script>
<script src="includes/js/02_APList/subTabs.js"></script>
<script>

</script>

<h2>Access Points</h2>

<button class="bubbleBtn APSubTabBtn" id="APList-btnDetails" onclick="pageElements.APSubTabController.activateTab(this)">Details</button>
<button class="bubbleBtn APSubTabBtn" id="APList-btnMap" onclick="pageElements.APSubTabController.activateTab(this)">Map</button>

<div id="APList-Details">
	<p>
		<table id="APList-Table">
			<tr>
				<th style="width: 85px"></th>
				<th>Location</th>
				<th>MAC Address</th>
				<th>Details</th>
			</tr>
		</table>
	</p>
</div>

<div id="APList-Map">
<!-- 	testing map under AP -->
</div>

<script>
pageElements.APListController = new APList_List();
pageElements.APListController.initList();

pageElements.APSubTabController = new APList_subTabs();
// window.setInterval("pageElements.APListController.initList()", 5000);

</script>

<style>
#APList-Table { border-collapse:collapse; }
#APList-Table tr:nth-child(even) { background-color: #ccc; }
#APList-Table tr:first-child th { border-bottom: 2px solid black; }
#APList-Table tr th, #APList-Table tr td { padding: 10px; }
</style>
		    