<HTML>
<TITLE>ERPD - Modify RF Channel</TITLE>
<BODY>

<? require 'xml.php' ?>
<?
$rfinput = $HTTP_GET_VARS['rfinput'];
$rfch = $HTTP_GET_VARS['rfch'];
$mhz = $rfch * 0.192 + 8.096;
printf("<H2>Modifying RF Channel at input %d, %2.3f MHz</H2>", $rfinput, $mhz);
// XXX power values should be drop-down lists
?>


<FORM action=doModRF.php method=POST>
 <TABLE>
  <tr>
   <th align=left>Network Channel</th>
   <td> <SELECT name=netch> <? netch_selections($rfinput, $rfch); ?> </SELECT> </td>
  </tr>
  <tr>
   <th align=left>Min Power</th>
   <td><INPUT/ type=text size=3 name=minpower value="<?
     if (isset($minpowers[$rfinput][$rfch])) {
       echo $minpowers[$rfinput][$rfch];
     } else {
       echo $defminpower;
     }
   ?>" align=right></td>
  </tr>
  <tr>
   <th align=left>Nominal Power</th>
   <td><INPUT/ type=text size=3 name=nompower value="<?
     if (isset($nompowers[$rfinput][$rfch])) {
        echo $nompowers[$rfinput][$rfch];
     } else {
        echo $defnompower;
     }
   ?>" align=right></td>
  </tr>
  <tr>
   <th align=left>Error Correction</th>
   <td><SELECT name=fec> <? fec_selections($rfinput, $rfch); ?> </SELECT></td>
  </tr>
 </TABLE>
<?
echo "<INPUT type=hidden name=rfch value=$rfch>";
echo "<INPUT type=hidden name=rfinput value=$rfinput>";
?>
 <INPUT/ type=submit name=action value=Submit>
 <INPUT/ type=button onClick="window.close()" value=Cancel>
</FORM>

</BODY>
</HTML>
