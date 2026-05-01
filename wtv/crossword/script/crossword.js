lastAudio = null;


function FindAcrossClue(x,y) {

  var cWordOn = -1;
  var cx;

  // Check for no clue.
  var xm1  = eval(eval(x)-1);
  var xp1  = eval(eval(x)+1);

  var pxm1;
  if (xm1 >= 0) {
    pxm1 = GetCell(xm1, y);
  } else {
    pxm1 = "+";
  }

  var pxp1;
  if (xp1 < kWidth) {
    pxp1 = GetCell(xp1, y);
  } else {
    pxp1 = "+";
  }

  var px = GetCell(x,y);
  if (pxm1 == "+" && px != "+" && pxp1 == "+" ) {
    // No clue, return " "
    return(" ");
  }

  for (cx=0; cx <= x; cx++) {

    var xm1  = eval(eval(cx)-1);
    var xp1  = eval(eval(cx)+1);

    var pxm1;
    if (xm1 >= 0) {
      pxm1 = GetCell(xm1, y);
    } else {
      pxm1 = "+";
    }

    var pxp1;
    if (xp1 < kWidth) {
      pxp1 = GetCell(xp1, y);
    } else {
      pxp1 = "+";
    }

    var px = GetCell(cx,y);

    if (pxm1 == "+" && px != "+" && pxp1 != "+") {
      cWordOn++;
    }

  }

  if (aasAcross[y][cWordOn] != null) {
    return(aasAcross[y][cWordOn]);
  } else {
    return(" ");
  }

}

function FindDownClue(x,y) {

  var cWordOn = -1;
  var cy;

  // Check for no clue.
  var ym1  = eval(eval(y)-1);
  var yp1  = eval(eval(y)+1);

  var pym1;
  if (ym1 >= 0) {
    pym1 = GetCell(x, ym1);
  } else {
    pym1 = "+";
  }

  var pyp1;
  if (yp1 < kWidth) {
    pyp1 = GetCell(x, yp1);
  } else {
    pyp1 = "+";
  }

  var py = GetCell(x,y);
  if (pym1 == "+" && py != "+" && pyp1 == "+" ) {
    // No clue, return " "
    return(" ");
  }

  for (cy=0; cy <= y; cy++) {

    var ym1  = eval(eval(cy)-1);
    var yp1  = eval(eval(cy)+1);

    var pym1;
    if (ym1 >= 0) {
      pym1 = GetCell(x, ym1);
    } else {
      pym1 = "+";
    }

    var pyp1;
    if (yp1 < kHeight) {
      pyp1 = GetCell(x, yp1);
    } else {
      pyp1 = "+";
    }

    var py = GetCell(x,cy);
    if (pym1 == "+" && py != "+" && pyp1 != "+" ) {
      cWordOn++;
    }

  }

  if (aasDown[x][cWordOn] != null) {
    return(aasDown[x][cWordOn]);
  } else {
    return(" ");
  }

}

function ClearHighlights() {
  var cy, cx;
  for (cy = 0; cy < kHeight; cy++) {
    for (cx = 0; cx < kWidth; cx++) {
      if (GetCell(cx, cy) != '+') {
        document.crossword.elements[cx + cy * kWidth + kOtherFormElements].style.backgroundColor = '';
      }
    }
  }
}

function HighlightWord(x, y) {
  var cx, cy;

  // Find across word bounds and highlight
  var acrossLeft = x;
  while (acrossLeft > 0 && GetCell(acrossLeft - 1, y) != '+') acrossLeft--;
  var acrossRight = x;
  while (acrossRight < kWidth - 1 && GetCell(acrossRight + 1, y) != '+') acrossRight++;

  if (acrossRight > acrossLeft) {
    for (cx = acrossLeft; cx <= acrossRight; cx++) {
      document.crossword.elements[cx + y * kWidth + kOtherFormElements].style.backgroundColor = '#8888ff';
    }
  }

  // Find down word bounds and highlight
  var downTop = y;
  while (downTop > 0 && GetCell(x, downTop - 1) != '+') downTop--;
  var downBottom = y;
  while (downBottom < kHeight - 1 && GetCell(x, downBottom + 1) != '+') downBottom++;

  if (downBottom > downTop) {
    for (cy = downTop; cy <= downBottom; cy++) {
      document.crossword.elements[x + cy * kWidth + kOtherFormElements].style.backgroundColor = '#88ff88';
    }
  }

  // The focused cell gets a distinct highlight
  document.crossword.elements[x + y * kWidth + kOtherFormElements].style.backgroundColor = '#ffff00';
}

function show_clue(x, y, click) {
  document.crossword.across.value =  FindAcrossClue(x,y);
  document.crossword.down.value = FindDownClue(x,y);
  ClearHighlights();
  HighlightWord(x, y);
  if (click) {
    PlaySound("jollygooba1.mp3");
  }
}

function GetCell(x,y) {
  return (asPuzzle.charAt(y*kWidth+x));
}

function SolvePuzzle() {

  var sy=0;
  var sx=0;

  for (sy=0; sy < kHeight; sy++) {
    for (sx=0; sx < kWidth; sx++) {
      document.crossword.elements[eval(sx+sy*kHeight+kOtherFormElements)].value = GetCell(sx,sy);
    }
  }

}


function PlaySound(sound) {
  if (lastAudio) lastAudio.pause();
  lastAudio = document.getElementById(sound);
  lastAudio.currentTime = 0;
  lastAudio.play()
}

function CorrectPuzzle() {

  var cy=0;
  var cx=0;
  var bCorrect="t";

  for (cy=0; cy < kHeight; cy++) {
    for (cx=0; cx < kWidth; cx++) {
      if (document.crossword.elements[eval(cx+cy*kHeight+kOtherFormElements)].value != GetCell(cx,cy)) {
        document.crossword.elements[eval(cx+cy*kHeight+kOtherFormElements)].value = "";
        bCorrect="f";
      }
    }
  }

  if (bCorrect == "t") {
    PlaySound("applause.mp2");
  }

}

function RenderCell(x, y) {

  if (GetCell(x,y) == '+') {
    document.write("<td width=20 bgcolor=000000 align=left valign=top>");
    document.write("  <img src=/wtv/ROMCache/spacer.gif width=20 height=20>");
    document.write("  <input type=hidden name=sel"+eval(x+y*kWidth)+" value=\"+\">");
    document.write("</td>");
  } else {
    document.write("<td width=20 height=20 bgcolor=666666 align=center valign=bottom>");
    document.write("  <input type=text name=sel"+eval(x+y*kWidth)+" bgcolor=666666 maxlength=1 autocaps size=1 width=20 border=0 onChange=\"CaseSet(this)\" onFocus=\"show_clue("+x+","+y+",true)\">");
    document.write("</td>");
  }

}

function RenderRow(y) {

  document.write("<tr>");

  var x=0;

  for (x=0; x < kWidth; x++) {
    RenderCell(x,y);
  }

  document.write("</tr>");

}

function RenderPuzzle() {

  document.write("<table border=0 cellspacing=3 cellpadding=0 bgcolor=222222>");

  var y=0;

  for (y=0; y < kHeight; y++) {
    RenderRow(y);
  }

  document.write("</table>");

}

function CaseSet(j) {
  for (var i = 0; i < j.value.length;  i++) {
    var c = j.value.charAt(i);
    if (c >= 'a' && c <= 'z') {
      j.value = j.value.toUpperCase();
    }
  }
}

function SetCookie (name, value) {

  var argv = SetCookie.arguments;
  var argc = SetCookie.arguments.length;
  var expires = (argc > 2) ? argv[2] : null;
  var path = (argc > 3) ? argv[3] : null;
  var domain = (argc > 4) ? argv[4] : null;
  var secure = (argc > 5) ? argv[5] : false;
  document.cookie = name + "=" + escape (value) +
    ((expires == null) ? "" : ("; expires=" + expires.toGMTString())) +
    ((path == null) ? "" : ("; path=" + path)) +
    ((domain == null) ? "" : ("; domain=" + domain)) +
    ((secure == true) ? "; secure" : "");

}

function GetCookieVal (offset) {

  var endstr = document.cookie.indexOf (";", offset);
  if (endstr == -1)
    endstr = document.cookie.length;
  return unescape(document.cookie.substring(offset, endstr));

}

function GetCookie (name) {

  var arg = name + "=";
  var alen = arg.length;
  var clen = document.cookie.length;
  var i = 0;

  while (i < clen) {
    var j = i + alen;
    if (document.cookie.substring(i, j) == arg)
      return GetCookieVal (j);

    i = document.cookie.indexOf(" ", i) + 1;
    if (i == 0)
      break;
  }

  return null;

}

function SetCookieMacro (sCookieName, sValue) {

  var expdate = new Date ();
  // Save Cookie for 56 days (8 weeks).
  expdate.setTime (expdate.getTime() + (56 * 24 * 60 * 60 * 1000));

  SetCookie (sCookieName, sValue, expdate, "/");

}

function SaveGame() {

  sGameCookie = "";

  for (gy=0; gy < kHeight; gy++) {
    for (gx=0; gx < kWidth; gx++) {
      if (document.crossword.elements[eval(gx+gy*kHeight+kOtherFormElements)].value != "") {
        sGameCookie += document.crossword.elements[eval(gx+gy*kHeight+kOtherFormElements)].value;
      } else {
        sGameCookie += "+";
      }
    }
  }

  SetCookieMacro("sgcw"+sPuzzleName, sGameCookie);
  //alert("sGameCookie: "+sGameCookie);
}

function LoadGame() {

  sGameCookie = GetCookie("sgcw"+sPuzzleName);

  if (sGameCookie == null)
    return;

  for (ly=0; ly < kHeight; ly++) {
    for (lx=0; lx < kWidth; lx++) {
      if (sGameCookie.charAt(lx+ly*kHeight) != "+") {
        document.crossword.elements[eval(lx+ly*kHeight+kOtherFormElements)].value = sGameCookie.charAt(lx+ly*kHeight);
      }
    }
  }

}

function Quit() {


}

