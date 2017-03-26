<?php
$file = "buttonStatus.txt";
$handle = fopen($file,'w+');
if (isset($_POST['up']))
  { $status = "UP"; }
else if(isset($_POST['down']))
  { $status = "DOWN";}
else if(isset($_POST['left']))
  { $status = "LEFT";}
else if(isset($_POST['right']))
  { $status = "RIGHT";}

fwrite($handle,$status);
fclose($handle);

print "
<html>
<body>
<style type=text/css>
h2{
        position: absolute;
        top: 75px;
        left: 225px;
}
</style>
<h2>Going $status</h2>
</body>
</html>
";

include('index.html');
?>
