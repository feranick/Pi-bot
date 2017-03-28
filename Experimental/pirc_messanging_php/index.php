<?php

$status = $_POST['status'];

#$command = escapeshellcmd("/var/www/html/pirc_manual/piRC.py " .$status);
$command = "/var/www/html/pirc_manual/piRC.py $status 2>&1";
$output = shell_exec($command);
echo $output;

print "
<script>
console.log('PHP:" .$status. "');
</script>

<html>
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
