<? require 'xml.php';
   require 'JSON.php' 
?>
<?

$vrpds = array();
for ($i=0; $i<$nVRPDs; $i++) {
  $vrpds[$i]['vrpd'] = $i+1;
  $vrpds[$i]['name'] = $netnames[$i];
  $vrpds[$i]['ipaddr'] = $srcips[$i];
  $vrpds[$i]['sport'] = $srcports[$i];
  $vrpds[$i]['nc1500'] = $dstips[$i];
  $vrpds[$i]['dport'] = $dstports[$i];
  $vrpds[$i]['idle_tx'] = $idletxs[$i];
}

$vrpdsList = array();
$vrpdsList['results']=$i;
$vrpdsList['vrpdList']=$vrpds;

$json = new Services_JSON();
$value = $json->encode($vrpdsList);
echo $value;
?>