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

$dbConvert = new dbInterface();
$apDetail = new APDetail();

$details = (object) array(
		"MAC" => $dbConvert->convertValueToDB("MAC", $parameters->MAC),
		"Detail" => $parameters->Detail,
		"Location" => $parameters->Location,
		"Latitude" => $dbConvert->convertValueToDB("LATITUDE", $parameters->Latitude),
		"Longitude" => $dbConvert->convertValueToDB("LONGITUDE", $parameters->Longitude),
		"Altitude" => $parameters->Altitude,
		"APID" => $parameters->APID
);
	
if (empty($details->APID))
{
	$apDetail->addAP($details);
}
else 
{
	$apDetail->updateAP($details);
}
	
/* END OF ACTION */

/* $returnValue is set as object */	
?>