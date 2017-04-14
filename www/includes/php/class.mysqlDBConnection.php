<?php 
/* file: class.mysqlPosDBConnection.php
 * 
 * Brief: class file for the connection to the DB
 * 			contains the functions for connecting to, and querying the DB.
 */
include_once __DIR__."/class.mysqliExt.php";

class dbConnection
{
	/********************* Variable Declarations *******************/
	private $link;
	
	private $dbServername = "localhost";
	private $dbUsername = "root";
	private $dbPassword = "capstone";
	private $dbName = "INKHUNTERS";
	
	/****************** End Variable Declarations *******************/
	
	
	/********************** Private Functions ************************/
	/* db_connection
	 * 
	 * Brief: constructor: creates the $link resource in order to query the DB.
	 */
	function __construct()
	{
		$this->link = $this->connectDB();
	}
	
	/* private connectDB
	 * 
	 * Brief: connects to DB and returns resource ID for the link
	 * 
	 * Input: none
	 * 
	 * output: none
	 * 
	 * return: resource ID for doing queries
	 */
	private function connectDB()
	{
		$link = new db($this->dbServername, $this->dbUsername, $this->dbPassword, $this->dbName);
			
		return $link;
	}
	
	/******************** End Private Functions *********************/
	
	/******************** Start Public Functions ********************/
	
	/* public getQueryResults
	 * 
	 * Brief: retrieves the query specified and puts into an array
	 * 			with all the items in the array
	 * 
	 * Input:	$query - text for the query. arguments to be replaced with ?
	 * 						e.g. select * from items where id=?;
	 * 			$args - array of arguments to replace ? in query statement
	 * 
	 * Output: none
	 * 
	 * Return: array of results
	 */
	public function queryDB($query, $args = null)
	{
		$resource = $this->getResource($query, $args);
		// Change the formatting from MSSQL to MySql
		
		$output = array();
		if (!empty($resource))
		{
			$numRows = $resource->num_rows;
			for ($i = 0; $i < $numRows; $i++)
				$output[] = $this->getNextRow($resource);
		}
		return $output;
	}
	
	public function getLink()
	{
		return $this->link;
	}
	
	public function getNextRow($resource)
	{
		return $resource->fetch_array(MYSQLI_ASSOC);
	}
	
	public function getResource($query, $args = array())
	{
		$resource = null;
		
		// Change the formatting from MSSQL to MySql
		$pattern = '@top [0-9]+@i';
		$matches = array();
		preg_match($pattern, $query, $matches);
		
		if (!empty($matches))
		{
			$query = str_replace($matches[0], "", $query);	// kill the 'top x' part of the query
			$pattern = '@[0-9]+@i';
			$numMatches = array();
			preg_match($pattern, $matches[0], $numMatches);	// find the number part
			$query = trim($query);
			if (substr($query, -1) == ';')
				$query = substr($query, 0, strlen($query)-1);
			$query .= " limit ".$numMatches[0];				// add back in 'limit x' at the end of the statement
		}
		
		$output = array();
		if ($this->link != null)
		{
		
			$stmt = $this->link->prepare($query);
			
			
			
			if (!empty($args))
			{
				foreach($args as $argKey=>$argVal)
				{
					$type = 'b';	// blob
					if (gettype($argVal) == "boolean" || gettype($argVal) == "integer")
						$type = 'i';
					else if (gettype($argVal) == "double" || gettype($argVal) == "float")
						$type = 'd';
					else if (gettype($argVal) == "string")
						$type = 's';
					$stmt->mbind_param($type, $args[$argKey]);
					
				}
			}
			
			$stmt->execute();
// 			echo "<pre>".print_r($stmt) . "</pre>";
			$resource = $stmt->get_result();
		}
		return $resource;
	}
	
	public function getTime()
	{
		$query = "SELECT CURRENT_TIMESTAMP;";
		$result = $this->queryDB($query);
		
		
		if (!empty($result))
			$returnArray = array("Time" => $result[0]["CURRENT_TIMESTAMP"]);
		else
			$returnArray = array("Time" => "");
		
		return $returnArray;
	}
	
} /// End Class


if (empty($GLOBALS["DBLINK"]))
{
	$GLOBALS["DBLINK"] = new dbConnection();
}
$dbLink = $GLOBALS["DBLINK"];

?>