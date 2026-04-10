<? require 'xml.php';
   require 'JSON.php' 
?>
<?
$rfinput = $HTTP_POST_VARS['rfinput'];
$channels = array();
for ($i=0; $i<$nchannels; $i++) {
  $channels[$i]['channel'] = $i+1;
  $channels[$i]['vrpd'] = $netchs[$rfinput][$i];

  $channels[$i]['performance'] = $minpower[$rfinput][$i];
  $channels[$1]['errorcorrection'] = $fecs[$rfinput][$1];
}

$channelsList = array();
$channelsList['results']=$i;
$channelsList['channelList']=$channels;

$json = new Services_JSON();
$value = $json->encode($channelList);
echo $value;
?>
