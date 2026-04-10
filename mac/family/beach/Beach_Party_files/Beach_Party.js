// Created by iWeb 3.0.1 local-build-20100307

function createMediaStream_id3()
{return IWCreatePhotocast("http://www.woofie.com/mac/family/beach/Beach_Party_files/rss.xml",true);}
function initializeMediaStream_id3()
{createMediaStream_id3().load('http://www.woofie.com/mac/family/beach',function(imageStream)
{var entryCount=imageStream.length;var headerView=widgets['widget1'];headerView.setPreferenceForKey(imageStream.length,'entryCount');NotificationCenter.postNotification(new IWNotification('SetPage','id3',{pageIndex:0}));});}
function layoutMediaGrid_id3(range)
{createMediaStream_id3().load('http://www.woofie.com/mac/family/beach',function(imageStream)
{if(range==null)
{range=new IWRange(0,imageStream.length);}
IWLayoutPhotoGrid('id3',new IWPhotoGridLayout(3,new IWSize(186,186),new IWSize(186,26),new IWSize(222,227),27,27,0,new IWSize(2,35)),new IWPhotoFrame([IWCreateImage('Beach_Party_files/Playtime_blue_hills_01.png'),IWCreateImage('Beach_Party_files/Playtime_blue_hills_02.png'),IWCreateImage('Beach_Party_files/Playtime_blue_hills_03.png'),IWCreateImage('Beach_Party_files/Playtime_blue_hills_06.jpg'),IWCreateImage('Beach_Party_files/Playtime_blue_hills_09.png'),IWCreateImage('Beach_Party_files/Playtime_blue_hills_08.png'),IWCreateImage('Beach_Party_files/Playtime_blue_hills_07.png'),IWCreateImage('Beach_Party_files/Playtime_blue_hills_04.png')],null,2,1.000000,0.000000,0.000000,0.000000,0.000000,1.000000,25.000000,1.000000,10.000000,355.000000,229.000000,355.000000,229.000000,null,null,null,0.500000),imageStream,range,new IWShadow({blurRadius:10,offset:new IWPoint(-0.0000,2.0000),color:'#000000',opacity:0.600000}),null,1.000000,{backgroundColor:'rgb(0, 0, 0)',reflectionHeight:100,reflectionOffset:2,captionHeight:100,fullScreen:0,transitionIndex:2},'Media/slideshow.html','widget1','widget2','widget3')});}
function relayoutMediaGrid_id3(notification)
{var userInfo=notification.userInfo();var range=userInfo['range'];layoutMediaGrid_id3(range);}
function onStubPage()
{var args=window.location.href.toQueryParams();parent.IWMediaStreamPhotoPageSetMediaStream(createMediaStream_id3(),args.id);}
if(window.stubPage)
{onStubPage();}
setTransparentGifURL('Media/transparent.gif');function applyEffects()
{var registry=IWCreateEffectRegistry();registry.registerEffects({stroke_0:new IWPhotoFrame([IWCreateImage('Beach_Party_files/Playtime_waves_01.png'),IWCreateImage('Beach_Party_files/Playtime_waves_02.png'),IWCreateImage('Beach_Party_files/Playtime_waves_03.png'),IWCreateImage('Beach_Party_files/Playtime_waves_06.jpg'),IWCreateImage('Beach_Party_files/Playtime_waves_09.jpg'),IWCreateImage('Beach_Party_files/Playtime_waves_08.jpg'),IWCreateImage('Beach_Party_files/Playtime_waves_07.jpg'),IWCreateImage('Beach_Party_files/Playtime_waves_04.jpg')],null,0,1.000000,0.000000,0.000000,0.000000,0.000000,1.000000,18.000000,1.000000,1.000000,43.000000,554.000000,43.000000,554.000000,null,null,null,0.500000),shadow_0:new IWShadow({blurRadius:10,offset:new IWPoint(-0.0000,2.0000),color:'#000000',opacity:0.600000})});registry.applyEffects();}
function hostedOnDM()
{return false;}
function onPageLoad()
{IWRegisterNamedImage('comment overlay','Media/Photo-Overlay-Comment.png')
IWRegisterNamedImage('movie overlay','Media/Photo-Overlay-Movie.png')
loadMozillaCSS('Beach_Party_files/Beach_PartyMoz.css')
adjustLineHeightIfTooBig('id1');adjustFontSizeIfTooBig('id1');adjustLineHeightIfTooBig('id2');adjustFontSizeIfTooBig('id2');NotificationCenter.addObserver(null,relayoutMediaGrid_id3,'RangeChanged','id3')
adjustLineHeightIfTooBig('id4');adjustFontSizeIfTooBig('id4');fixupAllIEPNGBGs();fixAllIEPNGs('Media/transparent.gif');Widget.onload();fixupIECSS3Opacity('id5');applyEffects()
initializeMediaStream_id3()}
function onPageUnload()
{Widget.onunload();}
