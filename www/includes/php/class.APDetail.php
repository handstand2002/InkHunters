<?php 
include_once __DIR__."/class.mysqlDBConnection.php";
include_once __DIR__."/class.dbInterface.php";

class APDetail
{
	private $dbLink;
	
	function __construct()
	{
		$this->dbLink = $GLOBALS["DBLINK"];
		$this->dbConvert = new dbInterface();
	}
	
	function getList()
	{
		$query = "select 
					APID, HEX(MAC) as MAC, Detail, LocationDescription, 
					Latitude, Longitude, Altitude 
				FROM 
					APDETAIL";
		
		$result = $this->dbLink->queryDB($query);
		
		foreach($result as $key=>$value)
		{
			$result[$key]["MAC"] = $this->dbConvert->convertValueFromDB("MAC", $value["MAC"]);
			
			$result[$key]["Latitude"] = (object) array(
					"STRING" => $this->dbConvert->convertValueFromDB("LATITUDE", $value["Latitude"]),
					"INT" => $value["Latitude"]
			);
			
			$result[$key]["Longitude"] = (object) array(
					"STRING" => $this->dbConvert->convertValueFromDB("LONGITUDE", $value["Longitude"]),
					"INT" => $value["Longitude"]
			);
		}
		
		return $result;
	}
			
	/**
	 * @param Object $details
 	 * 					MAC,
	 * 					Detail,
	 * 					Location,
	 * 					Latitude,
	 * 					Longitude,
	 * 					Altitude
	 */
	public function addAP($details)
	{
		$query = "INSERT INTO 
	APDETAIL 
		(MAC, Detail, LocationDescription, 
		Latitude, Longitude, Altitude) 
values 
		(CONV(? , 16 , 10 ), ?, ?, ?, ?, ?);";
		$values = array($details->MAC, $details->Detail, $details->Location,
				$details->Latitude, $details->Longitude, $details->Altitude
		);
		
		$result = $this->dbLink->queryDB($query, $values);
	}
	
	public function updateAP($details)
	{
		echo "<pre>".print_r($details, true)."</pre>";
		$query = "UPDATE APDETAIL SET MAC=CONV(? , 16 , 10 ), Detail=?, LocationDescription=?, Latitude=?, Longitude=?, Altitude=? where APID=?";
		$values = array($details->MAC, $details->Detail, $details->Location, 
				$details->Latitude, $details->Longitude, $details->Altitude, $details->APID);
		$this->dbLink->queryDB($query, $values);
	}
	
	public function deleteAP($APID)
	{
		$query = "DELETE FROM APDETAIL where APID=?";
		$values = array($APID);
		$this->dbLink->queryDB($query, $values);
	}
}
?>