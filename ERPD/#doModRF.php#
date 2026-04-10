<HTML>
<TITLE>ERPD - RF Channel Modified</TITLE>
<BODY>
<? require 'xml.php' ?>
<?
$rfinput = $HTTP_POST_VARS['rfinput'];
$rfch    = $HTTP_POST_VARS['rfch'];
$netch   = $HTTP_POST_VARS['netch'];
$minpower= $HTTP_POST_VARS['minpower'];
$nompower= $HTTP_POST_VARS['nompower'];
$fec     = $HTTP_POST_VARS['fec'];

if ($netch == "-") {
  $netch = -1;
}

$netchs[$rfinput][$rfch] = $netch;
$minpowers[$rfinput][$rfch] = $minpower;
$nompowers[$rfinput][$rfch] = $nompower;
$demodthreads[$rfinput][$rfch] = 0;
$fecs[$rfinput][$rfch] = $fec;

echo "$netch,$minpower,$nompower,$fec<br>";

write_config();

echo "<H2>RF Channel Modified</H2>";
?>
<SCRIPT>
setTimeout("opener.window.location.reload(); window.close()", 1000);
</SCRIPT>

</BODY>
</HTML>
