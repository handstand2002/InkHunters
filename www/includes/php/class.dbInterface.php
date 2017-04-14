<?php 
class dbInterface
{
	/**
	 * @param string $type - "MAC", "LATITUDE", "LONGITUDE"
	 * @param string $value - <MAC>: BigInt, <LATITUDE> [-90,90], <LONGITUDE> [-180,180]
	 * @return string - MAC: "00:AA:11:BB:22:CC", LATITUDE: S 49, LONGITUDE: W 117
	 */
	public function convertValueFromDB($type, $value)
	{
		$type = strtoupper($type);
		$returnValue = "";
		switch ($type)
		{
			case "MAC":
				while (strlen($value) < 12)
					$value = "0" . $value;
				$returnValue = $this->convertMACFromDB($value);
				break;
			case "LATITUDE":
				$returnValue = $this->convertLatitudeFromDB($value);
				break;
			case "LONGITUDE":
				$returnValue = $this->convertLongitudeFromDB($value);
				break;
		}
		return $returnValue;
	}
	
	/**
	 * @param string $type - "MAC", "LATITUDE", "LONGITUDE"
	 * @param string $value - MAC: "00:AA:11:BB:22:CC", LATITUDE: S 49, LONGITUDE: W 117
	 * @return number - <MAC>: BigInt, <LATITUDE> [-90,90], <LONGITUDE> [-180,180]
	 */
	public function convertValueToDB($type, $value)
	{
		$type = strtoupper($type);
		$returnValue = "";
		switch ($type)
		{
			case "MAC":
				$returnValue = $this->convertMACToDB($value);
				break;
			case "LATITUDE":
				$returnValue = $this->convertLatitudeToDB($value);
				break;
			case "LONGITUDE":
				$returnValue = $this->convertLongitudeToDB($value);
				break;
		}
		return $returnValue;
	}
	
	private function convertMACToDB($string)
	{
		$rawHex = str_replace(array('-',':',';'), '',$string);
		return $rawHex;
	}
	
	private function convertMACFromDB($string)
	{
		$output = "";
		$first = true;
		for ($i = 0; $i < 6; $i++)
		{
			if (!$first)
				$output .= ":";
				$first = false;
				$output .= substr($string, $i*2, 2);
		}
		return $output;
	}
	
	private function convertLatitudeToDB($string)
	{
		$direction = substr($string, 0, 1);
		$numbers = floatVal(trim(substr($string, 1)));
		if (strtoupper($direction) == "S")
			$numbers *= -1;
			
		return $numbers;
	}
	
	private function convertLatitudeFromDB($number)
	{
		if (floatval($number) < 0)
		{
			$number *= -1;
			$output = "S " . $number;
		}
		else
			$output = "N " . $number;
			return $output;
	}
	
	private function convertLongitudeToDB($string)
	{
		$direction = substr($string, 0, 1);
		$numbers = floatVal(trim(substr($string, 1)));
		if (strtoupper($direction) == "W")
			$numbers *= -1;
			
			return $numbers;
	}
	
	private function convertLongitudeFromDB($number)
	{
		$output = "";
		if (floatval($number) < 0)
		{
			$number *= -1;
			$output = "W " . $number;
		}
		else
			$output = "E " . $number;
			return $output;
	}
}
?>