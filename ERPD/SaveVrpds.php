<HTML>
<TITLE>ERPD - vRPDs Updated</TITLE>
<BODY>
<? require 'xml.php';
   require 'JSON.php' 
?>
<?

$gridInput = $HTTP_POST_VARS['gridMods'];
$json = new Services_JSON(SERVICES_JSON_LOOSE_TYPE);

$gridInputClean = str_replace("\\","",$gridInput);
$datalist = $json->decode($gridInputClean);

$updated =0;
foreach ($datalist as $vrpd) {
  $index = $vrpd['vrpd']-1;
  $srcips[$index] = $vrpd['ipddr'];
  $netnames[$index] = $vrpd['name'];
  $srcports[$index] = $vrpd['sport'];
  $dstips[$index] = $vrpd['nc1500'];
  $dstports[$index] = $vrpd['dport'];
  $idletxs[$index] = (($vrpd['idle_tx'] == 1) ? 1: 0);
  $netdemods[$index] = 0;
  $netspresent[$index] = 1;
  $updated +=1;
}

// reset this as we have modfied and/or added channels.  may want to just update the whole thing 
// from the client to prevent sync errors...

$nVRPDs = 0;
while (each($srcips)) {
   $nVRPDs += 1;
}

write_config();
echo "<H2>$updated of $nVRPDs Network Channels Updated</H2>";
?>

</BODY>
</HTML>
