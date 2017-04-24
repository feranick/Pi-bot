<?php
$status = $_POST['status'];

//$command = "sudo python3 piRC_manual.cpython-34.pyc $status 2>&1";y
$command = "sudo ./piRC_manual.py $status 2>&1";
$output = shell_exec($command);
echo $output;

print "
<script>
console.log('PHP:" .$status. "');
</script>

<html>
<title> PiRC - no file version</title>
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
