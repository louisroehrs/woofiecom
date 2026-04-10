<HTML>
<TITLE>ERPD - Network Channel Deleted</TITLE>
<BODY>
<? require 'xml.php' ?>
<?
$netch = $HTTP_GET_VARS['netch'];

$netspresent[$netch] = 0;

write_config();
echo "<H2>Network Channel $netch Deleted</H2>";

?>
<SCRIPT>
setTimeout("opener.window.location.reload(); window.close()", 1000);
</SCRIPT>

</BODY>
</HTML>
