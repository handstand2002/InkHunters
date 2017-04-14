<DOCTYPE html>
<html>
<head>


<style>
tr td
{
	border-bottom: 1px solid black;
}

tr th
{
	border-bottom: 2px solid black;
}
</style>
</head>
<body>
<h3>Recent Requests:</h3>

<table>
	<tr>
		<th>Time</th>
		<th>Action</th>
		<th>Parameters</th>
		<th>Callback</th>
	</tr>
	
	<?php 
	$files = scandir ( __DIR__ );
	foreach($files as $requestFile)
	{
		if (strpos($requestFile, "Request") === 0)
		{
// 			echo "Request: $requestFile<br />";
			$data = file_get_contents(__DIR__."/$requestFile");
			$dateTime = date ("F d Y H:i:s", filemtime(__DIR__."/$requestFile"));
			
			$data = json_decode($data);
			$post = $data->POST;
			$actionData = $post->i;
			$actionData = json_decode($actionData);
			$get = $data->GET;
			
			echo "<tr>";
			echo "<td>$dateTime<br /><a target='_blank' href='../ajaxHelper.php?file=". $requestFile . "'>Run File</a></td>";
			
			echo "<td>";
			foreach($actionData as $singleRequest)
				echo $singleRequest->action . "<br />";
			echo "</td>";
			
			echo "<td>";
			foreach($actionData as $singleRequest)
				echo print_r($singleRequest->parameters, true) . "<br />";
			echo "</td>";
			
			echo "<td>";
			foreach($actionData as $singleRequest)
				echo $singleRequest->callback . "<br />";
			echo "</td>";
		}
	}
?>

</table>



</body>
</html>