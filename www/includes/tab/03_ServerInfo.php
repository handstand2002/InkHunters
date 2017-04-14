<script src="includes/js/03_ServerInfo/pageController.js"></script>

<h2>Server Info</h2>
<p>
<table id="ServerInfo-Table">
</table>
</p>

<script>
pageElements.ServerInfoPageController = new ServerInfoPageController();
pageElements.ServerInfoPageController.initList();

// window.setInterval("pageElements.ServerInfoPageController.initList()", 5000);
</script>

<style>

#ServerInfo-Table { border-collapse:collapse; }
#ServerInfo-Table tr:nth-child(odd) { background-color: #ccc; }
#ServerInfo-Table tr:first-child th { border-bottom: 2px solid black; }
#ServerInfo-Table tr th, #ServerInfo-Table tr td { padding: 15px; }
</style>
		    