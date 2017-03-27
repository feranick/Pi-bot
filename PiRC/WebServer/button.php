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
<body>
<style type=text/css>
h2{
        position: absolute;
        top: 150px;
        left: 100px;
}
</style>
<h2>Going $status</h2>
</body>
</html>
";

include('index.html');
?>
