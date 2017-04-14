<?php 
include_once __DIR__."/class.mysqlDBConnection.php";
include_once __DIR__."/class.dbInterface.php";

class Device
{
	private $dbLink;
	
	function __construct()
	{
		$this->dbLink = $GLOBALS["DBLINK"];
		$this->dbConvert = new dbInterface();
	}
	
	public function getList()
	{
		$query = "select DeviceID, HEX(MAC) as MAC, Title, Detail, LastSeenTime, LastSeenLatitude, LastSeenLongitude, LastSeenAltitude from DEVICE";
		$result = $this->dbLink->queryDB($query);
		
		foreach($result as $key=>$value)
		{
			$result[$key]["MAC"] = $this->dbConvert->convertValueFromDB("MAC", $value["MAC"]);
			
			$result[$key]["Latitude"] = (object) array(
					"STRING" => $this->dbConvert->convertValueFromDB("LATITUDE", $value["LastSeenLatitude"]),
					"INT" => $value["LastSeenLatitude"]
			);
			
			$result[$key]["Longitude"] = (object) array(
					"STRING" => $this->dbConvert->convertValueFromDB("LONGITUDE", $value["LastSeenLongitude"]),
					"INT" => $value["LastSeenLongitude"]
			);
			
			$result[$key]["Altitude"] = $value["LastSeenAltitude"];
			
			unset($result[$key]["LastSeenLatitude"]);
			unset($result[$key]["LastSeenLongitude"]);
			unset($result[$key]["LastSeenAltitude"]);
			
		}
		
		return $result;
	}
	
	public function editDevice($id, $title, $details)
	{
		$query = "update DEVICE set Title=?, Detail=? where DeviceID=?";
		$values = array($title, $details, $id);
		$this->dbLink->queryDB($query, $values);
	}
	
}
?>