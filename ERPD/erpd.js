bare="toolbar=0,location=0,directories=0,status=1,menubar=0,scrollbars=0,resizable=1";
// bare="toolbar=1,location=1,directories=0,status=1,menubar=1,scrollbars=1,resizable=1";

function w(s) {
    document.write(s);
}

function show_net_channel(chnum, sip, sport, dip, dport, idle) {
  w("<tr class=net>"+
      "<td class=num>" +chnum+ "</th>" +
      "<td class=source align=right>" +sip+ "</td>"+
      "<td class=source align=right>" +sport+ "</td>"+
      "<td class=dest align=right>" +dip+ "</td>"+
      "<td class=dest align=right>" +dport+ "</td>"+
      "<td class=misc align=right>" +(idle ? "True" : "False")+ "</td>"+
      "<td class=control>"+
	"<INPUT/ type=button value=Modify onClick=jsModifyNet('" +chnum+ "') >&nbsp;&nbsp;"+
	"<INPUT/ type=button value=Delete onClick=jsDeleteNet('" +chnum+ "') >"+
      "</td>"+
    "</tr>"
  );
}

function jsAddNet() {
    window.open("AddNet.php", "AddNet",
		bare + ",dependent=1,width=630,height=500" ).focus;
}

function jsModifyNet(netchnum) {
    window.open("ModNet.php?netch=" +netchnum, "ModNet",
		bare + ",dependent=1,width=630,height=500" ).focus;
}

function jsDeleteNet(netchnum) {
    if (confirm("Really delete network channel " +netchnum+ "?")) {
	var w=window.open("doDelNet.php?netch=" +netchnum, "DelNet",
		    bare + "width=50,height=50");
	return true;
    }
    return false;
}

function jsModRF(rfinput, rfchnum) {
    window.open("ModRF.php?rfinput=" +rfinput+ "&rfch=" +rfchnum, "ModRF",
		bare + ",dependent=1,width=630,height=500" ).focus;
}


function show(msg) { window.status=msg; return true; }

function soff() { window.status=''; }

function mhz_vert(chnum) {
    khz = ch_to_khz(chnum);
    s = "";
    digit = parseInt(khz/10000);
    khz = khz%10000;
    if (digit != 0) {
	s += digit;
    }

    digit = parseInt(khz/1000);
    khz = khz%1000;
    s += "<br>" + digit;

    s += "<br>.";   // Decimal point

    digit = parseInt(khz/100);
    khz = khz%100;
    s += "<br>" + digit;

    digit = parseInt(khz/10);
    khz = khz%10;
    s += "<br>" + digit;

    digit = parseInt(khz);
    s += "<br>" + digit;

    return s;
}

function ch_to_khz(chnum)
{
    return 8096 + chnum * 192;
}

function setchannel(rfi, chnum, netch, minpwr, nompwr, fecon) {
    netchannel[rfi][chnum] = netch;
    minpower[rfi][chnum] = minpwr;
    nompower[rfi][chnum] = nompwr;
    fec[rfi][chnum] = fecon;
}

function initchannels(maxrfi, nchannels, minpwr, nompwr)
{
    netchannel = new Array(maxrfi);
    minpower = new Array(maxrfi);
    nompower = new Array(maxrfi);
    fec = new Array(maxrfi);

    for (var i = 0; i < maxrfi; i++) {
	netchannel[i] = new Array(nchannels);
	minpower[i] = new Array(nchannels);
	nompower[i] = new Array(nchannels);
	fec[i] = new Array(nchannels);

	for (var j = 0; j < nchannels; j++) {
	    setchannel(i, j, -1, minpwr, nompwr, "Off");
	}
    }
}

// initchannels(maxrfi, nchannels);

// setchannel(0, 0, 1, 6, 7, 0);
// setchannel(0, 5, 0, 3, 30, 1);
// setchannel(1, 3, 0, 8, 30, 0);
// setchannel(1, 10, 1, 12, 100, 1);

function starttable() { w("<table class=channel>"); }
function endtable() { w("</table>"); }
function whdr(s) { w("<th class=channel>" +s+ "</th>");  }
function startrow(s) { w("<tr class=channel>");  whdr(s); }
function endrow() { w("</tr>"); }
function cell(s) { w("<td>" +s+ "</td>"); }

function channel_table(rfi, startch, numch) {
  var i;
  var endch;

  endch = startch + numch;  

  starttable();
  startrow("MHz");
    for (i = startch; i < endch; i++) {
      whdr(mhz_vert(i));
    }
  endrow();
  startrow("Network<br>Channel");
    for (i = startch; i < endch; i++) {
      cell( netchannel[rfi][i] == -1 ? "" : netchannel[rfi][i] );
    }
  endrow();
  startrow("Min<br>Power");
    for (i = startch; i < endch; i++) {
      cell(minpower[rfi][i]);
    }
  endrow();
  startrow("Nominal<br>Power");
    for (i = startch; i < endch; i++) {
      cell(nompower[rfi][i]);
    }
  endrow();
  startrow("Error<br>Correction");
    for (i = startch; i < endch; i++) {
      cell ( fec[rfi][i] == "On" ? "Y" : "" );
    }
  endrow();
  startrow("Change");
    for (i = startch; i < endch; i++) {
      cell("<INPUT/ type=button value=\"\" onClick=jsModRF(" +rfi+ "," +i+ ") >");
      // cell("<a onClick=jsModRF(" +rfi+ "," +i+ ") >*</a>");
    }
  endrow();
  endtable();
}

function channelst(nrfis, nchannels) {
  for (var rfi = 0; rfi < nrfis; rfi++) {
    w("<h4>RF Input " +rfi+ "</h4>");
    channel_table(rfi, 0, nchannels);
  }
}

function jsBackup() {
    window.open("BackupConfigFile.php", "Backup",
		bare + ",dependent=1,width=630,height=500" ).focus;
}

function jsRestore() {
    window.open("RestoreConfigFile.php", "Restore",
		bare + ",dependent=1,width=630,height=500" ).focus;
}

function jsDefault() {
    window.open("DefaultConfigFile.php", "Default",
		bare + ",dependent=1,width=630,height=500" ).focus;
}

function jsShowFile() {
    window.open("ShowConfigFile.php?filename=data.xml", "Show",
		"toolbar=0,location=0,directories=0,status=1,menubar=0,scrollbars=1,resizable=1, width=630"
		).focus;
}
