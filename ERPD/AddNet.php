<HTML>
<TITLE>ERPD - Add New Network Channel</TITLE>
<BODY>
<H2>Add New Network Channel</H2>
<FORM action=doAddNet.php method=POST>
 <TABLE>
  <tr>
   <th align=left>Source IP Address/Bits:</th>
   <td><INPUT/ type=text size=18 name=srcip></td>
  </tr>
  <tr>
   <th align=left>Source Port:</th>
   <td><INPUT/ type=text size=5 name=srcport></td>
  </tr>
  <tr>
   <th align=left>NC-1500 IP Address:</th>
   <td><INPUT/ type=text size=15 name=dstip></td>
  </tr>
  <tr>
   <th align=left>NC-1500 Port:</th>
   <td><INPUT/ type=text size=5 name=dstport></td>
  </tr>
  <tr>
   <th align=left>Idle TX:</th>
   <td><SELECT name=idletx><OPTION SELECTED>False<OPTION>True</SELECT></td>
  </tr>
 </TABLE>
 <INPUT/ type=submit name=action value=Submit>
</FORM>

</BODY>
</HTML>
