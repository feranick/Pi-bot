<?php
$file = "buttonStatus.txt";
$handle = fopen($file,'w+');
$status = "ZERO";
fwrite($handle,$status);
fclose($handle);
echo $status
?>
