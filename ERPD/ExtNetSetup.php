<HTML>
<TITLE>ERPD - External Network Setup</TITLE>
<BODY>

<? require 'xml.php' ?>
<?
$netch = $HTTP_GET_VARS['netch'];
echo "<H2>Modifying Network Channel $netch</H2>";
?>

<FORM action=doExtNetworkSetup.php method=POST>
 <TABLE>
  <tr>
<th align=left>NC-1500 IP Address:</th>
   <td><INPUT type=text size=18 name=nc1500ip value="<? echo $srcips[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>DAC IP address:</th>
   <td><INPUT/ type=text size=18 name=dacip value="<? echo $srcports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>SDM IP address (if applicable):</th>
   <td><INPUT/ type=text size=18 name=sdmip value="<? echo $srcports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>ERPD (to NC-1500) IP address:</th>
   <td><INPUT/ type=text size=18 name=erpdnc1500ip value="<? echo $srcports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>ERPD (management) IP address:</th>
   <td><INPUT/ type=text size=18 name=erpdmgmtip value="<? echo $srcports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>Router IP address (if applicable):</th>
   <td><INPUT/ type=text size=18 name=routerip value="<? echo $srcports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>ERPD Hardware address:</th>
   <td><INPUT/ type=text size=18 name=erpdmac value="<? echo $srcports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>Server IP address:</th>
   <td><INPUT/ type=text size=18 name=serverip value="<? echo $srcports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>Subnet Mask:</th>
   <td><INPUT/ type=text size=18 name=subnetmask value="<? echo $dstips[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>Gateway IP address:</th>
   <td><INPUT/ type=text size=18 name=gatewayip value="<? echo $dstports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>Server host name:</th>
   <td><INPUT/ type=text size=30 name=serverhost value="<? echo $dstports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>Boot filename:</th>
   <td><INPUT/ type=text size=30 name=bootfilename value="<? echo $dstports[$netch]; ?>"></td>
  </tr>
  <tr>
   <th align=left>Vendor specific info:</th>
   <td><INPUT/ type=text size=30 name=venderspecificinfo value="<? echo $dstports[$netch]; ?>"></td>
  </tr>

 </TABLE>
<?
echo "<INPUT type=hidden name=netch value=$netch>";
?>
 <INPUT/ type=submit name=action value=Submit>
</FORM>

</BODY>
</HTML>
