<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

session_start();

$debug = false;

$showOutput = !empty($_GET["debug"]);

if ($debug && empty($_GET["file"]))
{
	$debugFolderInfoFile = __DIR__."/debugRequests/.folderInfo.json";
	if (!file_exists($debugFolderInfoFile))
	{
		$initObject = (object) array("LastRequestID" => 0);
		file_put_contents($debugFolderInfoFile, json_encode($initObject));
	}
	// Get the info about the last request ID
	$folderInfo = json_decode(file_get_contents($debugFolderInfoFile));
	
	// Construct the request parameters into an object, to put in the file
	$requestInfo = json_encode((object) array("POST" => $_POST, "GET" => $_GET));
	
	// Write the request into the file
	$newDebugFile = __DIR__."/debugRequests/Request" . $folderInfo->LastRequestID;
	file_put_contents($newDebugFile, $requestInfo);
	
	// Write the data back to the folder info file, with incremented RequestID
	$folderInfo->LastRequestID++;
	file_put_contents($debugFolderInfoFile, json_encode($folderInfo));
}
else if (!empty($_GET["file"]))
{
	$data = file_get_contents(__DIR__."/debugRequests/" . $_GET["file"]);
		
	$showOutput = true;
	$data = json_decode($data, true);
	$_POST = $data["POST"];
// 	$actionData = $post->i;
// 	$actionData = json_decode($actionData);
	$_GET = $data["GET"];
}


include_once __DIR__."/php/class.mysqlDBConnection.php";
include_once __DIR__."/php/class.Device.php";
include_once __DIR__."/php/class.APDetail.php";

$stubText = '<?php 
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

/* END OF ACTION */

/* $returnValue is set as object */	
?>';

// print_r($_POST);
$requestArray = json_decode($_POST["i"]);
foreach ($requestArray as $key=>$request)
{
	if (!empty($request->action))
	{
		// test if the ajaxAction file is defined
		if (file_exists(__DIR__."/ajaxAction/" . $request->action . ".php"))
		{
			$parameters = $request->parameters;
			
			ob_start();
			// Run action file
			include __DIR__."/ajaxAction/" . $request->action . ".php";
			$rawOutput = ob_get_contents();
			ob_end_clean();
			if ($showOutput)
			{
				echo $rawOutput;
			}
			
			
			if (!isset($returnValue))
				$returnValue = "";
			$requestArray[$key]->result = $returnValue; 
		}
		else
		{
			$stubFilename = __DIR__."/ajaxAction/stub." . $request->action . ".php";
			// Create the stub
			if (!file_exists($stubFilename))
			{
				file_put_contents($stubFilename, $stubText);
				chmod($stubFilename, 0766);
			}
			$requestArray[$key]->error = "action '" . $request->action . "' not properly defined";
			$requestArray[$key]->result = "";
		}
	}
// 	echo "Request: " . print_r($request, true);
}

echo json_encode($requestArray);

// $query = "select * from APDETAIL";
// $res = $dbLink->queryDB($query);
// print_r($res);
?>
