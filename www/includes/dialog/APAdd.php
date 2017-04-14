<?php 
$dialogID = "APAddDialog";
$title = "Add Access Point";
?>

<div id="<?php echo $dialogID;?>" title="<?php echo $title;?>" style="display:none">
  <p>
  <form id="APAddForm">
  	<table>
  		<tr>
  			<td>AP ID</td>
  			<td><input name="APID" maxlength="5" type="number" disabled placeholder="System Populated"></td>
		</tr>
  		<tr>
  			<td>Location</td>
  			<td><input name="Location" maxlength="30" type="text" placeholder="EDU Bldg 441"></td>
		</tr>
  		<tr>
  			<td>MAC Address</td>
  			<td><input name="MAC" maxlength="17" type="text" placeholder="00:00:00:00:00:00"></td>
		</tr>
		<tr>
  			<td>Latitude</td>
  			<td><input name="Latitude" type="text" placeholder="S 48.98345"></td>
		</tr>
		<tr>
  			<td>Longitude</td>
  			<td><input name="Longitude" type="text" placeholder="W 117.03948"></td>
		</tr>
		<tr>
  			<td>Altitude (ft)</td>
  			<td><input name="Altitude" type="text" placeholder="2426"></td>
		</tr>
		<tr>
  			<td>Details</td>
  			<td><textarea name="Details" placeholder="Add Additional Details"></textarea></td>
		</tr>
  	</table>
  </form>
  </p>
</div>


<script>
$( function() {
  $( "#<?php echo $dialogID;?>" ).dialog(
		  {
			  autoOpen: false,
			  width: 400,
			  modal: true,
			  buttons: [
					{
						text: "Cancel",
						click: function() {
							$( this ).dialog( "close" );
						}
					},
					{
						text: "Save",
						click: function() {
							pageElements.APListController.addAP();
							$( this ).dialog( "close" );
						}
					}
				]
		  }
		  );
} );
</script>
