// Created by iWeb 3.0.1 local-build-20100110

setTransparentGifURL('Media/transparent.gif');function hostedOnDM()
{return false;}
function onPageLoad()
{loadMozillaCSS('Goodnight_files/GoodnightMoz.css')
adjustLineHeightIfTooBig('id1');adjustFontSizeIfTooBig('id1');adjustLineHeightIfTooBig('id2');adjustFontSizeIfTooBig('id2');fixupAllIEPNGBGs();fixAllIEPNGs('Media/transparent.gif');Widget.onload();fixupIECSS3Opacity('id3');performPostEffectsFixups()}
function onPageUnload()
{Widget.onunload();}
