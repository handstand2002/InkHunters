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

$returnValue = (object) array();

// Get Host Name
$returnValue->HostName = gethostname();

// Get listening port for process
// netstat -tulpn

// Get IP Address
$ipAddressProp = "IP Address";
$returnValue->$ipAddressProp = $_SERVER['SERVER_ADDR'];

// Get CPU load
$cpuProp = "CPU Usage";
$returnValue->$cpuProp = sys_getloadavg()[0]*100 . "%";

// Get Memory usage
$info = shell_exec("cat /proc/meminfo");
$info = explode("\n", $info);
foreach($info as $prop=>$value)
{
	$info[$prop] = explode(" ", $value);
	$i = 0;
	foreach($info[$prop] as $subProp=>$subValue)
	{
		if (strlen(trim($subValue)) > 0)
			$info[$prop][$i++] = $subValue;
		
		if ($i-1 != $subProp)
			unset($info[$prop][$subProp]);
	}
}
$returnValue->Memory = round($info[1][1]/$info[0][1] * 100) . "% Free (" . $info[0][1] . " " . $info[0][2] . " Total)";;

/* END OF ACTION */

/* $returnValue is set as object */	
?>