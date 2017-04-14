<?php 
/* Auto Generated Action File. Actions done in here will be called when the corresponding action is requested.
 * $parameters are provided in $parameters - object format
 * Return value is passed back through $returnValue - object format
 */
/* DO NOT MODIFY */
$pageName = strtolower(basename($_SERVER["SCRIPT_NAME"]));
if ($pageName != "ajaxhelper.php")
	Exit;
/* END PRE-FUNCTION */
/* CONTENTS OF ACTION */

	$apDetail = new APDetail();
	$apDetail->deleteAP($parameters->APID);
	
/* END OF ACTION */

/* $returnValue is set as object */	
?>