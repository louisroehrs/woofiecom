
var size_unit="em";var cnbc_defaultSize=1;var cnbc_maxSize=1.25;var cnbc_minSize=.75;var cnbc_fontSize=cnbc_defaultSize;var element;function incrFontContent(id)
{var incrFont=getFontSize();incrFont+=.25;if(incrFont>=cnbc_maxSize)
{incrFont=cnbc_maxSize;}
setFontSize(incrFont);if(id==null){id="cnbc_textbody";}
document.getElementById(id).style.fontSize=incrFont+size_unit;}
function dcrFontContent(id)
{var dcrFont=getFontSize();dcrFont-=.25;if(dcrFont<=cnbc_minSize)
{dcrFont=cnbc_minSize;}
setFontSize(dcrFont);if(id==null){id="cnbc_textbody";}
document.getElementById(id).style.fontSize=dcrFont+size_unit;}
function setDefault(id)
{if(id==null){id="cnbc_textbody";}
element=document.getElementById(id);element.style.fontSize=cnbc_defaultSize;cnbc_fontSize=cnbc_defaultSize;}
function setFontSize(value)
{cnbc_fontSize=value;}
function getFontSize()
{return cnbc_fontSize;}
function printThis(){var x,s=location.href;if((x=s.indexOf('#'))>=0)
{s=s.substr(0,x);}
if(s.indexOf('?')>=0)
{s+='&print=1&displaymode=1098';}
else
{if(s.charAt(s.length-1)!='/')
{s+='/';}
s+='print/1/displaymode/1098/';}
var rdid=/[\?|&|\/]did[=|\/](\d*)/;var mdid=s.match(rdid);if(mdid!=null&&mdid[1]!='')
{var rid=/[\?|&|\/]id[=|\/](\d*)/;var mid=s.match(rid);if(mid!=null&&mid[1]!='')
{s=s.replace(mid[1],mdid[1])}}
var o=new UberSniff();if(o.webtv)
{location.href=s;}
else
{OCW(s,'print','width=640,height=480,scrollbars=1,resizable=1');}}
function CNBC_toggleTabs(id,parent,activetab_class,tab_class,element){var tabobj=document.getElementById(id);var els=document.getElementsByTagName(element);for(i=0;i<els.length;i++){if(els[i].parentNode.id==parent){els[i].className=tab_class;}}
if(tabobj.className==tab_class){tabobj.className=activetab_class;}}
function CNBC_toggleSections(id,parent,element){var sectobj=document.getElementById(id);var els=document.getElementsByTagName(element);for(i=0;i<els.length;i++){if(els[i].parentNode.id==parent){els[i].style.display="none";}}
sectobj.style.display="block";}
function cnbc_elementState(x,el,value){if(el=='cursor'){x.style.cursor=value;}else if(el=='background'){x.style.backgroundColor=value;}}
function cnbc_multiover(x){x.style.backgroundColor='#f7f7f7';}
function cnbc_multiout(x){x.style.backgroundColor='#FFFFFF';}
function cnbc_multionclick(loc){window.location=loc;}
function cnbc_toggleOnOff(on,off){var onObj=document.getElementById(on);var offObj=document.getElementById(off);if(onObj.className==""){onObj.className="bold";offObj.className="";}}
function submitenter(symbol,event){var temp=symbol.action;var keycode;if(window.event)keycode=window.event.keyCode;if(temp.indexOf('?q=')!=-1)temp=temp.substr(0,temp.indexOf('?q='));if(keycode==13)
{symbol.action=temp+'?q='+escape(event);symbol.submit();}
else if(event.which==13)
{symbol.action=temp+'?q='+escape(event);symbol.submit();}}
function cnbc_setSymbolInputField(){var strSymbol=cnbc_getURLParam('q');document.getElementById("symbol_input").value=strSymbol;}
function cnbc_getURLwithSymbol(url){location.href=url+'?q='+cnbc_getURLParam('q');}
function cnbc_addtoWatchlistTabs(){cnbc_watchlist_addSymbol(cnbc_getURLParam('q'));}
function cnbc_gotomodURL(url,params){var cnbc_index=location.href.indexOf("http://www.cnbc.com");var cnbc_index2=location.href.indexOf("http://cnbc.com");var index=params.indexOf("url");if(cnbc_index!=-1||cnbc_index2!=-1){if(index!=-1){window.location=url+params.replace(/url/,location.href.replace("=","/").replace("?","/").replace("&","/"));}}else{if(index!=-1){window.location=url+params.replace(/url/,location.href);}}}
function cnbc_toggleUserState(){var user_state=cnbc_watchlist_isRegistered();if(user_state){document.getElementById("reg_user").style.display="block";document.getElementById("unreg_user").style.display="none";}
else{document.getElementById("unreg_user").style.display="block";document.getElementById("reg_user").style.display="none";}}
function cnbc_displayUsername(parent,id){var x=document.getElementById(id);var user_state=cnbc_watchlist_isRegistered();if(user_state){var CookieUser=cnbc_readCookie('SUBSCRIBERINFO');if(!CookieUser)
{var temp=cnbc_readCookie('ACEGI_SECURITY_HASHED_REMEMBER_ME_COOKIE');if(temp)
{CookieUser=temp.split(":")[0];}
else
{CookieUser=cnbc_readCookie('CASTOKEN');if(!CookieUser)
{CookieUser="Guest";}}}
if(CookieUser.length>24)
{x.innerHTML=CookieUser;var p=document.getElementById(parent);var t=p.style.top;p.style.top="25px";}else{x.innerHTML="Welcome, "+CookieUser;}}else{x.innerHTML="Welcome, Guest";}}
function emailThis(){trackit();var et='mailto:?subject='+(pd_me.nw?'Newsweek.com%20on%20MSNBC':'CNBC.com')+'%20Article:%20'+pd_esc(pd_me.h)+'&body='+pd_esc(pd_me.h)+'%0D%0A'+pd_esc(pd_me.d)+'%0D%0Ahttp://'+location.host+'/id/'+pd_me.id+pd_me.su+'/from/ET/';if(pd_me.ep!='')et+='%0D%0A_____________________________%0D%0A'+pd_me.ep;location.href=et;}
function setPermalink(){var pLink=document.getElementById("cnbc_permalink");pLink.innerHTML=location.href;}
function buildTagSheets(id,target,taglist,size)
{var oB=new UberSniff();if(oB.safari)
{var sheet=getObj(id+0);var ul_cnbctab=sheet.parentNode.childNodes[0];for(var i=0;i<ul_cnbctab.childNodes.length;i++)
{ul_cnbctab.childNodes[i].style.fontSize=11;}}
for(var i=0;i<taglist.length;i++)
{var sheet=getObj(id+i);var len=taglist[i].length;if(len>60)
size=Math.floor(len/3)+1;var start=0,end=size;while(len>size)
{buildTagUL(sheet,target,taglist[i],start,end);start+=size;end+=size;len-=size;}
if(start<taglist[i].length&&taglist[i][start])
{buildTagUL(sheet,target,taglist[i],start,taglist[i].length);}
setMPTabOffsetHeight(sheet);}}
function buildTagUL(parent,target,taglist,start,end)
{var list=createEl('ul');parent.appendChild(list);for(var j=start;j<end;j++)
{if(taglist[j])
{var item=createEl('li');item.innerHTML="<a href='/id/"+target+"/cid/"+taglist[j].id+"'>"+taglist[j].name+"</a>";list.appendChild(item);}}}
function switchMPTab(tab,sheetName)
{if(tab.className.indexOf("active")==0)return;var children=tab.parentNode.childNodes;var display;for(var i=0;i<children.length;i++)
{if(children[i]!=tab)
{children[i].className="inactive";display="none";}
else
{if(i==children.length-1)
tab.className="activeR";else
tab.className="active";display="";if(typeof(footLink)!="undefined"&&footLink[i])
{var foot=getObj("mpfootlink");foot.href=footLink[i].link;foot.innerHTML=footLink[i].text;}}
getObj(sheetName+i).style.display=display;setMPTabOffsetHeight(getObj(sheetName+i));}}
function setMPTabOffsetHeight(sheet)
{var ulChildren=sheet.childNodes;var maxUlHeight=0;for(var i=0;i<ulChildren.length;i++)
{maxUlHeight=ulChildren[i].offsetHeight>maxUlHeight?ulChildren[i].offsetHeight:maxUlHeight;}
sheet.style.height=maxUlHeight;}
function CNBCUpdateTimeStamp(pdt,mode){if(pdt!=''&&window.DateTime){var str;var d=parseInt((pdt-621355968000000000)/10000);var c=new Date();var m=parseInt(((c-d)/1000)/60);var h=Math.floor(m/60);if(h<1){if(m>=1){str=m+' min';if(mode=='normal')str+='ute';if(m>1)str+='s';str+=' ago';}}
else{str=h+' h';if(mode=='normal')str+='ou';str+='r';if(h>1)str+='s';str+=' ago';}
if(str!=undefined)
document.write(str);}}
function cnbc_readPartnerSessionCookie(name){if(document.cookie.length>0)
{c_start=document.cookie.indexOf(name+"=");if(c_start!=-1)
{c_start=c_start+name.length+1;c_end=document.cookie.indexOf(";",c_start);if(c_end==-1)c_end=document.cookie.length
var c_value=unescape(document.cookie.substring(c_start,c_end));return c_value;}}
return null;}
function cnbc_createPartnerSessionCookie(c_name,value){var mydomain='cnbc.com';document.cookie=c_name+"="+value+";domain="+mydomain+";path=/";}
function cnbc_erasePartnerSessionCookie(c_name,value)
{var mydomain='cnbc.com';document.cookie=c_name+"="+value+";path=/"+";expires=Thu, 01-Jan-1970 00:00:01 GMT"+";domain="+mydomain;}
function cnbc_drpdwnmouseOver(subid){try{cnbc_getID(subid).style.display='block';}
catch(e){};}
function cnbc_drpdwnmouseOut(subid){try{cnbc_getID(subid).style.display='none';}
catch(e){};}
function cnbc_findPosLeft(adobj){var curleft=0;if(adobj.offsetParent){curleft=adobj.offsetLeft
while(adobj=adobj.offsetParent){curleft+=adobj.offsetLeft}}
return curleft;}
function cnbc_findPosTop(adobj){var curtop=0;if(adobj.offsetParent){curtop=adobj.offsetTop
while(adobj=adobj.offsetParent){curtop+=adobj.offsetTop}}
return curtop;}
function cnbc_drpdwnpos(hid,subid)
{try
{cnbc_getID(subid).style.left=cnbc_findPosLeft(cnbc_getID(hid))+"px";cnbc_getID(subid).style.top=cnbc_findPosTop(cnbc_getID(hid))+19+"px";}
catch(e){};}
function cnbc_getID(obj)
{return document.getElementById(obj);}
function cnbc_init_droparrows(str,element,holder)
{try
{var els=cnbc_getID(holder).getElementsByTagName(element);for(i=0;i<els.length;i++){if(els[i].id.indexOf(str)!=-1){els[i].style.display='inline';}}}
catch(e){};}
function cnbc_highlightSubText(curpageid,class_nam)
{try
{cnbc_getID('hsubnav_'+curpageid).className=class_nam;}
catch(e){};}
var cur_navSect="cnbc_hdsect";function cnbc_toggleElementsByID(hideID,showID,isRemovable,cookieName)
{if(hideID!=null)
{if(isRemovable==true)
{var pshd_value=cnbc_readPartnerSessionCookie(cookieName);if(cookieName==null||cookieName.length<=0||pshd_value!=null)
{var removeID=cnbc_getID(hideID);if(removeID!=null)removeID.parentNode.removeChild(removeID);cnbc_getID(showID).style.display="block";cur_navSect=showID;}}
else
{var removeID=cnbc_getID(showID);if(removeID!=null)removeID.parentNode.removeChild(removeID);cnbc_getID(hideID).style.display="block";cur_navSect=hideID;}}}
function cnbc_checkPageReferrer(ref_url,cookie)
{var cnbc_url="cnbc.com";var pshd_value=cnbc_readPartnerSessionCookie(cookie);if((pshd_value!=null)&&(ref_url!=null)&&(ref_url.length>0))
{var pshd_fun_value=pshd_value.split('|');var psh_PartnerURL=pshd_fun_value[7];var params_index=ref_url.indexOf("?");if(params_index!=-1)
{ref_url=ref_url.substring(0,params_index);}
var ref_index=ref_url.indexOf(psh_PartnerURL);var cnbc_index=ref_url.indexOf(cnbc_url);if((ref_index==-1)&&(cnbc_index==-1))
{cnbc_erasePartnerSessionCookie(cookie,"");return null;}
else
{return pshd_value;}}
else
{return pshd_value;}}
var storehref;var preloader_iframe_count=0;var preloader_iframe_link;var preloader_iframe_id;function cnbcwsod_loadchart(symbol,hrefparam,chartid,symbolname){var new_display=symbolname;var get_symbol=symbol;var chart_id;chart_id=chartid;document.getElementById('cnbcchart_symbol'+chartid).innerHTML=new_display;preloader_iframe_link=get_symbol;preloader_iframe_id='thumb_chart'+chartid;storehref=hrefparam;document.getElementById('thumb_chart'+chartid).src='http://media.cnbc.com/i/CNBC/CNBC_Images/blank.gif';cnbc_chart_clear_load();}
function chartlinkload(){try
{window.location=storehref;}
catch(e){};}
function cnbc_chart_clear_load(){preloader_iframe_count+=1
if(preloader_iframe_count<=4)
{document.getElementById(preloader_iframe_id).style.display='none';setTimeout("cnbc_chart_clear_load()",20);}
else
{document.getElementById(preloader_iframe_id).style.display='block';document.getElementById(preloader_iframe_id).src=preloader_iframe_link;preloader_iframe_count=0;}}
function init_sw_tab_MO(a,b,c){var init_store_MO_level=c;var init_start_tab='';var init_start_div='';var cookie_MO_recall_init=cnbc_readCookie("MarketOverviewRememberTabsLast"+init_store_MO_level);if(cookie_MO_recall_init!=null)
{var cookie_MO_div_init=cnbc_readCookie("MarketOverviewRememberDivLast"+init_store_MO_level);init_start_tab=document.getElementById(cookie_MO_recall_init);init_start_div=document.getElementById(cookie_MO_div_init);}
else if(cookie_MO_recall_init==null)
{init_start_tab=document.getElementById(a);init_start_div=document.getElementById(b);}
init_start_tab.className='h18 fL cnbc_MO_bd oranfont';init_start_tab.style.color='#fc7410';init_start_tab.style.backgroundColor='#ffffff';init_start_tab.style.borderBottom='1px solid #ffffff';init_start_div.style.display='block';}
function sw_tab_MO(x,y,z){var store_MO_level=z;var cookie_MO_recall='';var cookie_MO_recall_div='';var currentSelectionTab=x;var currentSelectionDiv=y;cookie_MO_recall=cnbc_readCookie("MarketOverviewRememberTabsLast"+store_MO_level);if(cookie_MO_recall!=null)
{cookie_MO_recall=cnbc_readCookie("MarketOverviewRememberTabsLast"+store_MO_level);cookie_MO_recall_div=cnbc_readCookie("MarketOverviewRememberDivLast"+store_MO_level);}
else if(cookie_MO_recall==null){cookie_MO_recall=cnbc_readCookie("MarketOverviewRememberTabs"+store_MO_level);cookie_MO_recall_div=cnbc_readCookie("MarketOverviewRememberDiv"+store_MO_level);}
if(currentSelectionTab!=cookie_MO_recall){var tab_sw_MO_A=document.getElementById(cookie_MO_recall);var tab_sw_MO_B=document.getElementById(currentSelectionTab);var div_sw_MO_A=document.getElementById(cookie_MO_recall_div);var div_sw_MO_B=document.getElementById(currentSelectionDiv);tab_sw_MO_B.style.color='#fc7410';tab_sw_MO_B.style.backgroundColor='#ffffff';tab_sw_MO_B.style.borderBottom='1px solid #ffffff';div_sw_MO_B.style.display='block';tab_sw_MO_B.className='h18 fL cnbc_MO_bd oranfont';tab_sw_MO_A.style.color='#004276';tab_sw_MO_A.className='h18 fL cnbc_MO_bd';tab_sw_MO_A.style.backgroundColor='#eeeeee';tab_sw_MO_A.style.borderBottom='1px solid #ccd6db';div_sw_MO_A.style.display='none';cnbc_createCookie("MarketOverviewRememberTabs"+store_MO_level,currentSelectionTab,"")
cnbc_createCookie("MarketOverviewRememberDiv"+store_MO_level,currentSelectionDiv,"")
cnbc_createCookie("MarketOverviewRememberTabsLast"+store_MO_level,currentSelectionTab,"")
cnbc_createCookie("MarketOverviewRememberDivLast"+store_MO_level,currentSelectionDiv,"")}
else{return;}}
function init_sw_tab_PG(a,b,c){var init_store_PG_level=c;var init_start_tab;var init_start_div;var cookie_PG_recall_init=cnbc_readCookie("Program_LinksRememberTabs_last"+init_store_PG_level);if(cookie_PG_recall_init!=null)
{var cookie_PG_div_init=cnbc_readCookie("Program_LinksRememberDiv_last"+init_store_PG_level);init_start_tab=document.getElementById(cookie_PG_recall_init);init_start_div=document.getElementById(cookie_PG_div_init);}
else
{init_start_tab=document.getElementById(a);init_start_div=document.getElementById(b);}
init_start_tab.className='h18 fL oranfont';init_start_tab.style.color='#fc7410';init_start_div.style.display='block';}
function sw_tab_PG(x,y,z){var store_PG_level=z;var cookie_PG_recall
var cookie_PG_recall_div
cookie_PG_recall=cnbc_readCookie("Program_LinksRememberTabs_last"+store_PG_level);if(cookie_PG_recall!=null)
{cookie_PG_recall=cnbc_readCookie("Program_LinksRememberTabs_last"+store_PG_level);cookie_PG_recall_div=cnbc_readCookie("Program_LinksRememberDiv_last"+store_PG_level);}
else{cookie_PG_recall=cnbc_readCookie("Program_LinksRememberTabs"+store_PG_level);cookie_PG_recall_div=cnbc_readCookie("Program_LinksRememberDiv"+store_PG_level);}
if(x!=cookie_PG_recall){var tab_sw_PG_A=document.getElementById(cookie_PG_recall);var tab_sw_PG_B=document.getElementById(x);var div_sw_PG_A=document.getElementById(cookie_PG_recall_div);var div_sw_PG_B=document.getElementById(y);tab_sw_PG_B.style.color='#fc7410';div_sw_PG_B.style.display='block';tab_sw_PG_B.className='h18 fL cnbc_PG_bd oranfont';tab_sw_PG_A.style.color='#004276';tab_sw_PG_A.className='h18 fL cnbc_PG_bd';div_sw_PG_A.style.display='none';cnbc_createCookie("Program_LinksRememberTabs"+store_PG_level,x,"")
cnbc_createCookie("Program_LinksRememberDiv"+store_PG_level,y,"")
cnbc_createCookie("Program_LinksRememberTabs_last"+store_PG_level,x,"")
cnbc_createCookie("Program_LinksRememberDiv_last"+store_PG_level,y,"")}
else{return;}}
function redirect(x){if(x.options[x.selectedIndex].value != '#') {var url = x.options[x.selectedIndex].value;eval("parent.location='"+url+"'");}}
function cnbc_renderTickerSymbol(cmpId){var strSymbol=cnbc_getURLParam('q');if(!strSymbol)
strSymbol='';for(var i=0;i<4;i++)
{var elem=document.getElementById('cnbc_rss_ticker_'+cmpId+'_'+i);elem.href=elem.href.replace('%7B$symbol%7D',escape(strSymbol));if(i<2)
{elem.innerHTML=elem.innerHTML.replace('{$symbol}',strSymbol.toUpperCase());}}}
function cnbc_addLink(rawHref,rawTitle)
{var heads=document.getElementsByTagName("head");var head=null;if(heads.length>0)
{head=heads[0];}
if(head)
{var tickerSymbol=cnbc_getURLParam('q');link=document.createElement("link");link.rel="alternate";link.type="application/rss+xml";link.href=rawHref.replace('{$symbol}',tickerSymbol);link.title=rawTitle.replace('{$symbol}',tickerSymbol.toUpperCase());head.appendChild(link);}}
var hexcase=0;var b64pad="";var chrsz=8;function hex_md5(s){return binl2hex(core_md5(str2binl(s),s.length*chrsz));}
function b64_md5(s){return binl2b64(core_md5(str2binl(s),s.length*chrsz));}
function str_md5(s){return binl2str(core_md5(str2binl(s),s.length*chrsz));}
function hex_hmac_md5(key,data){return binl2hex(core_hmac_md5(key,data));}
function b64_hmac_md5(key,data){return binl2b64(core_hmac_md5(key,data));}
function str_hmac_md5(key,data){return binl2str(core_hmac_md5(key,data));}
function md5_vm_test()
{return hex_md5("abc")=="900150983cd24fb0d6963f7d28e17f72";}
function core_md5(x,len)
{x[len>>5]|=0x80<<((len)%32);x[(((len+64)>>>9)<<4)+14]=len;var a=1732584193;var b=-271733879;var c=-1732584194;var d=271733878;for(var i=0;i<x.length;i+=16)
{var olda=a;var oldb=b;var oldc=c;var oldd=d;a=md5_ff(a,b,c,d,x[i+0],7,-680876936);d=md5_ff(d,a,b,c,x[i+1],12,-389564586);c=md5_ff(c,d,a,b,x[i+2],17,606105819);b=md5_ff(b,c,d,a,x[i+3],22,-1044525330);a=md5_ff(a,b,c,d,x[i+4],7,-176418897);d=md5_ff(d,a,b,c,x[i+5],12,1200080426);c=md5_ff(c,d,a,b,x[i+6],17,-1473231341);b=md5_ff(b,c,d,a,x[i+7],22,-45705983);a=md5_ff(a,b,c,d,x[i+8],7,1770035416);d=md5_ff(d,a,b,c,x[i+9],12,-1958414417);c=md5_ff(c,d,a,b,x[i+10],17,-42063);b=md5_ff(b,c,d,a,x[i+11],22,-1990404162);a=md5_ff(a,b,c,d,x[i+12],7,1804603682);d=md5_ff(d,a,b,c,x[i+13],12,-40341101);c=md5_ff(c,d,a,b,x[i+14],17,-1502002290);b=md5_ff(b,c,d,a,x[i+15],22,1236535329);a=md5_gg(a,b,c,d,x[i+1],5,-165796510);d=md5_gg(d,a,b,c,x[i+6],9,-1069501632);c=md5_gg(c,d,a,b,x[i+11],14,643717713);b=md5_gg(b,c,d,a,x[i+0],20,-373897302);a=md5_gg(a,b,c,d,x[i+5],5,-701558691);d=md5_gg(d,a,b,c,x[i+10],9,38016083);c=md5_gg(c,d,a,b,x[i+15],14,-660478335);b=md5_gg(b,c,d,a,x[i+4],20,-405537848);a=md5_gg(a,b,c,d,x[i+9],5,568446438);d=md5_gg(d,a,b,c,x[i+14],9,-1019803690);c=md5_gg(c,d,a,b,x[i+3],14,-187363961);b=md5_gg(b,c,d,a,x[i+8],20,1163531501);a=md5_gg(a,b,c,d,x[i+13],5,-1444681467);d=md5_gg(d,a,b,c,x[i+2],9,-51403784);c=md5_gg(c,d,a,b,x[i+7],14,1735328473);b=md5_gg(b,c,d,a,x[i+12],20,-1926607734);a=md5_hh(a,b,c,d,x[i+5],4,-378558);d=md5_hh(d,a,b,c,x[i+8],11,-2022574463);c=md5_hh(c,d,a,b,x[i+11],16,1839030562);b=md5_hh(b,c,d,a,x[i+14],23,-35309556);a=md5_hh(a,b,c,d,x[i+1],4,-1530992060);d=md5_hh(d,a,b,c,x[i+4],11,1272893353);c=md5_hh(c,d,a,b,x[i+7],16,-155497632);b=md5_hh(b,c,d,a,x[i+10],23,-1094730640);a=md5_hh(a,b,c,d,x[i+13],4,681279174);d=md5_hh(d,a,b,c,x[i+0],11,-358537222);c=md5_hh(c,d,a,b,x[i+3],16,-722521979);b=md5_hh(b,c,d,a,x[i+6],23,76029189);a=md5_hh(a,b,c,d,x[i+9],4,-640364487);d=md5_hh(d,a,b,c,x[i+12],11,-421815835);c=md5_hh(c,d,a,b,x[i+15],16,530742520);b=md5_hh(b,c,d,a,x[i+2],23,-995338651);a=md5_ii(a,b,c,d,x[i+0],6,-198630844);d=md5_ii(d,a,b,c,x[i+7],10,1126891415);c=md5_ii(c,d,a,b,x[i+14],15,-1416354905);b=md5_ii(b,c,d,a,x[i+5],21,-57434055);a=md5_ii(a,b,c,d,x[i+12],6,1700485571);d=md5_ii(d,a,b,c,x[i+3],10,-1894986606);c=md5_ii(c,d,a,b,x[i+10],15,-1051523);b=md5_ii(b,c,d,a,x[i+1],21,-2054922799);a=md5_ii(a,b,c,d,x[i+8],6,1873313359);d=md5_ii(d,a,b,c,x[i+15],10,-30611744);c=md5_ii(c,d,a,b,x[i+6],15,-1560198380);b=md5_ii(b,c,d,a,x[i+13],21,1309151649);a=md5_ii(a,b,c,d,x[i+4],6,-145523070);d=md5_ii(d,a,b,c,x[i+11],10,-1120210379);c=md5_ii(c,d,a,b,x[i+2],15,718787259);b=md5_ii(b,c,d,a,x[i+9],21,-343485551);a=safe_add(a,olda);b=safe_add(b,oldb);c=safe_add(c,oldc);d=safe_add(d,oldd);}
return Array(a,b,c,d);}
function md5_cmn(q,a,b,x,s,t)
{return safe_add(bit_rol(safe_add(safe_add(a,q),safe_add(x,t)),s),b);}
function md5_ff(a,b,c,d,x,s,t)
{return md5_cmn((b&c)|((~b)&d),a,b,x,s,t);}
function md5_gg(a,b,c,d,x,s,t)
{return md5_cmn((b&d)|(c&(~d)),a,b,x,s,t);}
function md5_hh(a,b,c,d,x,s,t)
{return md5_cmn(b^c^d,a,b,x,s,t);}
function md5_ii(a,b,c,d,x,s,t)
{return md5_cmn(c^(b|(~d)),a,b,x,s,t);}
function core_hmac_md5(key,data)
{var bkey=str2binl(key);if(bkey.length>16)bkey=core_md5(bkey,key.length*chrsz);var ipad=Array(16),opad=Array(16);for(var i=0;i<16;i++)
{ipad[i]=bkey[i]^0x36363636;opad[i]=bkey[i]^0x5C5C5C5C;}
var hash=core_md5(ipad.concat(str2binl(data)),512+data.length*chrsz);return core_md5(opad.concat(hash),512+128);}
function safe_add(x,y)
{var lsw=(x&0xFFFF)+(y&0xFFFF);var msw=(x>>16)+(y>>16)+(lsw>>16);return(msw<<16)|(lsw&0xFFFF);}
function bit_rol(num,cnt)
{return(num<<cnt)|(num>>>(32-cnt));}
function str2binl(str)
{var bin=Array();var mask=(1<<chrsz)-1;for(var i=0;i<str.length*chrsz;i+=chrsz)
bin[i>>5]|=(str.charCodeAt(i/chrsz)&mask)<<(i%32);return bin;}
function binl2str(bin)
{var str="";var mask=(1<<chrsz)-1;for(var i=0;i<bin.length*32;i+=chrsz)
str+=String.fromCharCode((bin[i>>5]>>>(i%32))&mask);return str;}
function binl2hex(binarray)
{var hex_tab=hexcase?"0123456789ABCDEF":"0123456789abcdef";var str="";for(var i=0;i<binarray.length*4;i++)
{str+=hex_tab.charAt((binarray[i>>2]>>((i%4)*8+4))&0xF)+
hex_tab.charAt((binarray[i>>2]>>((i%4)*8))&0xF);}
return str;}
function binl2b64(binarray)
{var tab="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";var str="";for(var i=0;i<binarray.length*4;i+=3)
{var triplet=(((binarray[i>>2]>>8*(i%4))&0xFF)<<16)|(((binarray[i+1>>2]>>8*((i+1)%4))&0xFF)<<8)|((binarray[i+2>>2]>>8*((i+2)%4))&0xFF);for(var j=0;j<4;j++)
{if(i*8+j*6>binarray.length*32)str+=b64pad;else str+=tab.charAt((triplet>>6*(3-j))&0x3F);}}
return str;}
function cnbc_rssCmpClass(cmpId,className)
{if(window.location.href.indexOf("/sh/3")>-1||window.location.href.indexOf("&sh=3")>-1||window.location.href.indexOf("?sh=3")>-1)
{var rssCmp=document.getElementById(cmpId);if(rssCmp!=null)rssCmp.className+=' '+className;}}
function cnbc_RunQuoteStrip(w,x,y,z,update){var url=window.location.toString();url.match(/\?(.+)$/);var params=RegExp.$1;var params=params.split("&");var queryStringList={};var new_param;for(var i=0;i<params.length;i++)
{var tmp=params[i].split("=");queryStringList[tmp[0]]=unescape(tmp[1]);}
if((queryStringList[tmp[0]]=='')|(queryStringList[tmp[0]]=='undefined'|(queryStringList[tmp[0]]=='null')))
{return;}
else{new_param=queryStringList[tmp[0]].toUpperCase();var imgsrc;document.getElementById("WSODQ"+w+"_"+x+"_NAME_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_NAME_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_SYMBOL_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_SYMBOL_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+new_param+"_SYMBOL_"+y+"_"+z).innerHTML=new_param;document.getElementById("WSODQ"+w+"_"+x+"_EXCHANGE_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_EXCHANGE_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_LAST_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_LAST_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_DYNACOLOR0_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_DYNACOLOR0_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_CHANGEARROW_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_CHANGEARROW_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_CHANGE_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_CHANGE_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_CHANGEPCT_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_CHANGEPCT_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_VOLUME_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_VOLUME_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_LASTTIME_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_LASTTIME_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_FLASH_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_FLASH_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_DISPLAYPARENT_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_DISPLAYPARENT_"+y+"_"+z;document.getElementById("WSODQ"+w+"_"+x+"_PROVIDER_"+y+"_"+z).id="WSODQ"+w+"_"+new_param+"_PROVIDER_"+y+"_"+z;document.getElementById("WSODQQUOTESTRIP_VALUE").value=new_param;imgsrc=document.getElementById("WSODQQUOTESTRIP_CHART_VALUE").value;var newimgsrc=imgsrc.replace(x,new_param)
document.getElementById("WSODQ_QUOTESTRIP_CHART").src=newimgsrc;cnbc_quoteComponent_init_getData(new_param,"WSODQ_COMPONENT_"+z,"WSODQ","true");cnbc_master_service_pushSymbols(new_param,"true");cnbc_master_service_update(update);}}
function cnbc_RunQuoteStripAdd(){cnbc_watchlist_addSymbolsFromTextArea("WSODQQUOTESTRIP_VALUE");}