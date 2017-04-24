<?php
$powerFile = "powerStatus.txt";
$steerFile = "steerStatus.txt";

if (isset($_POST['steer']))
{	$file = $steerFile;
	$status = $_POST['steer'];}
else
{	$file = $powerFile;
	$status = $_POST['power'];}

$handle = fopen($file,'w');
fwrite($handle,$status);
fclose($handle);

print "
<script>
console.log('PHP:" .$status. "');
</script>

<html>
<title> PiRC - file exchange version</title>    
<body>
<style type=text/css>
h2{
        position: absolute;
        top: 220px;
        left: 140px;
}
</style>
<h2>Going $status</h2>
</body>
</html>
";

include('buttons.html');
?>
