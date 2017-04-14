<?php 
$dialogID = "template";
$title = "Dialog Template";
?>

<div id="<?php echo $dialogID;?>" title="<?php echo $title;?>" style="display:none">
  <p>This is the default dialog which is useful for displaying information. The dialog window can be moved, resized and closed with the 'x' icon.</p>
</div>


<script>
$( function() {
  $( "#<?php echo $dialogID;?>" ).dialog(
		  {
			  autoOpen: false
		  }
		  );
} );
</script>
