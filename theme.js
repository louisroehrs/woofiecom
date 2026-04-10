var mytheme;


// Create a cookie with the specified name and value.

// The cookie expires at the end of the 20th century.

function setCookie(sName, sValue)

{

  date = new Date("12/31/2029"
);

  document.cookie = sName + "=" + escape(sValue) + "; expires=" + date.toGMTString();

}




// Retrieve the value of the cookie with the specified name.

function getCookie(sName)

{

  // cookies are separated by semicolons

  var aCookie = document.cookie.split("; ");

  for (var i=0; i < aCookie.length; i++)

  {

    // a name/value pair (a crumb) is separated by an equal sign

    var aCrumb = aCookie[i].split("=");

    if (sName == aCrumb[0]) 

      return unescape(aCrumb[1]);

  }



  // a cookie with the requested name does not exist

  return null;


}

function setTheme(theme) {


   setCookie("Theme",theme);
// alert(theme+   document.styleSheets[0].href +    document.styleSheets[0].disabled);
   document.styleSheets[0].href="http://www.woofie.com/"+theme +".css";


   
   

}

function getAndDrawTheme() {

   mytheme= getCookie("Theme");

alert(mytheme);
   if (mytheme=="") mytheme="style";

   document.styleSheets(0).href="http://www.woofie.com/"+mytheme +".css";


}

