<?php 
$dialogID = "Device_EditDialog";
$title = "Edit Device Name";
?>

<div id="<?php echo $dialogID;?>" title="<?php echo $title;?>" style="display:none">
  <p>
  <form id="Device_EditForm">
  	<table>
  		<tr>
  			<td>Device ID</td>
  			<td><input name="DeviceID" maxlength="5" type="number" disabled></td>
		</tr>
  		<tr>
  			<td>Location</td>
  			<td><input name="Title" maxlength="30" type="text" placeholder="EDU441 Laser5si"></td>
		</tr>
  		<tr>
  			<td>MAC Address</td>
  			<td><input name="MAC" maxlength="17" type="text" disabled></td>
		</tr>
		<tr>
  			<td>Last Seen Time</td>
  			<td><input name="LastTime" type="text" disabled></td>
		</tr>
		<tr>
  			<td>Latitude</td>
  			<td><input name="Latitude" type="text" disabled></td>
		</tr>
		<tr>
  			<td>Longitude</td>
  			<td><input name="Longitude" type="text" disabled></td>
		</tr>
		<tr>
  			<td>Altitude (ft)</td>
  			<td><input name="Altitude" type="text" disabled ></td>
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
							pageElements.DeviceListController.editDevice();
							$( this ).dialog( "close" );
						}
					}
				]
		  }
		  );
} );
</script>
