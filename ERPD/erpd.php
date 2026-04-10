<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <link REL=stylesheet TYPE=text/css HREF=erpd.css>
  <head>
    <title>ERPD Configuration</title>
  </head>
  <SCRIPT SRC="erpd.js"></SCRIPT>

  <body>
<?php require 'xml.php' ?>
    <h1>ERPD Configuration</h1>
    <FORM>
      <INPUT type=button value="Save Copy of Config File" onClick=jsBackup() ></INPUT>
      <INPUT type=button value="Restore from Saved Copy" onClick=jsRestore() ></INPUT>
      <INPUT type=button value="Set to Default Values" onClick=jsDefault() ></INPUT>
      <INPUT type=button value="Show Config File" onClick=jsShowFile() ></INPUT>
    </FORM>
    <FORM>
      <h2>Network Channels</h2>
      Each network channel lets the ERPD talk to a specific NC-1500.  You can create
      as many network channels as you wish.
      <p>
      <table>
	  <tr>
	    <th class=num rowspan=2>Network<br>Channel</th>
	    <th class=source colspan=2>Source</th>
	    <th class=dest colspan=2>NC-1500</th>
	    <th class=misc>Misc</th>
	    <th rowspan=2>Controls</th>
	  </tr>
	  <tr>
	    <th class=source>IP/Bits</th>
	    <th class=source>Port</th>
	    <th class=dest>IP</th>
	    <th class=dest>Port</th>
	    <th class=misc>Idle TX</th>
	  </tr>
          <SCRIPT LANGUAGE="Javascript">  <? vars_to_js(); ?>  </SCRIPT>
	  <tr>
	    <td class=num>New</td>
	    <td class=control colspan=5 align=center>Click button to add new channel</td>
	    <td><INPUT type=BUTTON value="Add Network Channel"
		 onClick=jsAddNet()
	         onMouseOver="show('Define a new network channel')"
	         onMouseOut="soff()">
		</INPUT></td>
	  </tr>
      </table>

    <h2>Return Path Channels</h2>
    Click on a change button to configure that channel.
<?php
    echo "<SCRIPT>channelst($nRFis, $nchannels);</SCRIPT>";
    // xml_out("save.xml");
?>
    </FORM>
  </body>
</html>
