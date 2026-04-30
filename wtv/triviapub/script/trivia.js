
var bCheckCS=false;

function SetCookie (name, value)
{
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

function GetCookieVal (offset)
{
  var endstr = document.cookie.indexOf (";", offset);
  if (endstr == -1)
    endstr = document.cookie.length;
  return unescape(document.cookie.substring(offset, endstr));
}

function GetCookie (name)
{
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

function AddToAccum (sCookieName, sPoints) {

  var expdate = new Date ();
  expdate.setTime (expdate.getTime() + (24 * 60 * 60 * 1000));

  var sAccum = GetCookie(sCookieName);

  //alert("b "+sCookieName+" "+sAccum);

  if (sAccum == null) {
    sAccum = eval(sPoints);
  } else {
    sAccum = eval(sAccum) + eval(sPoints);
  }

  //alert("a "+sCookieName+" "+sAccum);

  SetCookie (sCookieName, sAccum, expdate, "/");

  return (sAccum);

}

function SetCookieMacro (sCookieName, sValue) {

  var expdate = new Date ();
  expdate.setTime (expdate.getTime() + (7 * 24 * 60 * 60 * 1000));

  SetCookie (sCookieName, sValue, expdate, "/");

}

function PlayWrong() {
  document.getElementById("buzz.mid").currentTime = 0;
  document.getElementById("buzz.mid").play();
}

function PlayRight() {
  document.getElementById("newbell3.mid").currentTime = 0;
  document.getElementById("newbell3.mid").play()
}

function GetDigit(iScore, iDigit) {

  while (iScore.length < 4) {
    iScore = "0" + iScore;
  }

  //alert("before"+iScore+" "+iScore.length);
  var sDigit = iScore.charAt(iDigit);
  //alert("after"+sDigit);
  return(sDigit);

}

function FormMessageImageURL(sMessage) {

  if (sMessage != "spacer") {
    return("../../images/"+sMessage+".gif");
  } else {
    return("/wtv/ROMCache/spacer.gif");
  }
}

function FormDigitImageURL(iDigit) {
  return("../../images/"+iDigit+".GIF");
}

function SetScoreImages(sUserScore) {

  if (eval(sUserScore) < 0) {
    document.scorem.src  = "../../images/minus.gif";
    sUserScoreMod = sUserScore.substring(1,sUserScore.length);
  } else {
    document.scorem.src  = "/ROMCache/spacer.gif";
    sUserScoreMod = sUserScore;
  }

  document.score0.src = FormDigitImageURL(GetDigit(sUserScoreMod, 0));
  document.score1.src = FormDigitImageURL(GetDigit(sUserScoreMod, 1));
  document.score2.src = FormDigitImageURL(GetDigit(sUserScoreMod, 2));
  document.score3.src = FormDigitImageURL(GetDigit(sUserScoreMod, 3));

}

function loadDigitImage(iDigit) {

  var image = new Image();
  image.src = FormDigitImageURL(iDigit);

}

function loadMessageImage(sMessage) {

  var image = new Image();
  image.src = FormMessageImageURL(sMessage);

}

function LoadImages() {

  loadDigitImage(0);
  loadDigitImage(1);
  loadDigitImage(2);
  loadDigitImage(3);
  loadDigitImage(4);
  loadDigitImage(5);
  loadDigitImage(6);
  loadDigitImage(7);
  loadDigitImage(8);
  loadDigitImage(9);
  loadMessageImage("sorry");

}

function SetMessageImage(sWrongAnswer) {

  if (sWrongAnswer == null)
    sWrongAnswer=GetCookie("WRONGANSWER");

  if (sWrongAnswer == "T") {
    document.message.src = FormMessageImageURL("sorry");
    SetCookieMacro("WRONGANSWER", "B");
  } else if (sWrongAnswer == "F") {
    document.message.src = FormMessageImageURL("right");
    SetCookieMacro("WRONGANSWER", "B");
  } else {
    document.message.src = FormMessageImageURL("spacer");
    SetCookieMacro("WRONGANSWER", "B");
  }

}

function CheckOnRightQuestion(sCategory, sCategoryQuestionNumber) {

  var sQuestionOn = GetCookie(sCategory+"QON");
  if (sQuestionOn == null) {
    sQuestionOn = 1;
    SetCookieMacro(sCategory+"QON", sQuestionOn);
  }

  if (eval(sQuestionOn) != eval(sCategoryQuestionNumber)) {
    RedirectToQuestion(sCategory, sQuestionOn);
  }

}

function ReloadPage() {
  window.location.reload();
}

function Redirect(sURL) {
  window.location=sURL;
}

function RedirectToQuestion (sCategory, sQuestion) {
  Redirect(sCategory+sQuestion+".html");
}

function RedirectToNextQuestion (sCategory, sCurrQuestion) {

  var sNextQuestion = eval(eval(sCurrQuestion) + 1);
  SetCookieMacro(sCategory+"QON", sNextQuestion);
  RedirectToQuestion(sCategory, sNextQuestion);

}

function CheckAndRedirect (sSubmittedAnswer, sCorrectAnswer, sCategory,
                           sPointsPossible,  sCategoryQuestionOn) {

  if (bCheckCS)
    return;
  bCheckCS = true;

  SetMessageImage("B");

  if (eval(sSubmittedAnswer) == eval(sCorrectAnswer)) {
    PlayRight();
    var sUserScore = "" + AddToAccum(sCategory+"POINTS", sPointsPossible);
    SetCookieMacro("WRONGANSWER", "B");
    SetScoreImages(sUserScore);
    window.setTimeout(()=>RedirectToNextQuestion(sCategory, sCategoryQuestionOn),3000);
  } else {
    PlayWrong();
    var sWrongPts = eval(eval(-1)*eval(sPointsPossible));
    var sUserScore = "" + AddToAccum(sCategory+"POINTS", sWrongPts);
    SetCookieMacro("WRONGANSWER", "T");
    SetScoreImages(sUserScore);
    SetMessageImage();
    bCheckCS=false;
  }

  //  alert("after Check UserScore: "+sUserScore);

}

thisQuestion = parseInt( window.location.pathname.substr(window.location.pathname.lastIndexOf("general")).replace('general','').replace('.html',''))

CheckOnRightQuestion('general', thisQuestion);

