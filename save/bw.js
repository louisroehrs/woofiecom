

function getQuote () {
	var ticker = document.formq.symb.value;
	var time = document.formq.time.selectedIndex;
	time = document.formq.time.options[time].value;
	var urlstring = "http://www.bigcharts.com/quickchart/quickchart.asp?sid=&o_symb=&symb="+ticker+"&time="+time;
	window.open(urlstring,"quote");
} 



function stuffit() {
    var keywords = getURLvar("keywords");
    if (keywords) {
	 
		esckey =  unescape(keywords);
		for (i=0; i<esckey.length; i++) {
	 		if (esckey.charAt(i) == '+') {
				esckey = esckey.substring(0,i)+ ' ' + esckey.substring(i+1);
			}
		}
    	document.woofie.keywords.value = esckey;
	}
	var typed = getURLvar("typed");

    if (typed) {
     	document.woofie.typed.selectedIndex = unescape(typed);
    }	 
}


function remote() {
	options = document.woofie.keywords.value;
	typed = document.woofie.typed.selectedIndex;
 	rem = window.open("remote.html?keywords="+options+"&typed="+typed,"remote","width=320,height=150,resizable,resizeable,left=677,top=25");
	forward(rem);
}
	
function forward(window) {
	if (navigator.appName.indexOf("Explorer")<1 ) {
	// Navigator
		window.focus();
		winh +=200;
	} else {
	// Dr. Evil
		winh +=300;
	}
}

function blurme() {
	var woof=1;
	if (navigator.appName.indexOf("Explorer")>0 ) {
		this.blur();
	} 
}

function winopts(order,qty) {
	if (qty==1 ) {
		dog =400;
		cat = 400;
	} else if (qty==2) {
		dog =300;
		cat = 300;
	} else if (qty==3) {
		dog =200;
		cat = 200;
	}

	winh = 25 + (order -1) * dog;
	woof = "width=660,height="+cat+",left=5,top="+winh+",resizable,resizeable,scrollbars=yes,toolbar=yes";
	return woof;
	}
	
function gogetit () {
	var winh = 25;
	var keyword = document.woofie.keywords.value;
	sendable = escape(keyword);
	var dog = document.woofie.typed.selectedIndex;
	var pickie = document.woofie.typed.options[dog].value;
    if (pickie ==0) { gogetbook(sendable);}
    if (pickie ==1) {  gogetmusic(sendable);}
    if (pickie ==2) { gogetcgames(sendable);}
    if (pickie ==3) { gogetcgames(sendable);}
	if (pickie ==4) { gogetgifts(sendable);}
	if (pickie ==5) { gogettoys(sendable);}
	if (pickie ==6) { gogetsports(sendable); }
	if (pickie ==7) { gogetgifts(sendable); }
	remote();
} 

function gogetbook(keyword) {
	var qty=2;
	var sp= window.open("http://booksearch.spree.com/books/bk_book_search_result.asp?x=BIGWOOFIE&link_id=14797365&Keywords="+keyword+"&Submit=search","spree",winopts(1,qty));
	forward(sp);
	var amz=window.open("http://www.amazon.com/exec/obidos/external-search?tag=bigwoofieenterta&keyword="+keyword+"&Submit=search&mode=books","amazon",winopts(2,qty));
//	var amz=window.open("../index.html?tag=bigwoofieenterta&keyword="+keyword+"&Submit=search&mode=books","amazon",winopts(2,qty));
	forward(amz);
	blurme();
}

function gogetgifts(keyword) {
	var qty=3;
	var sp= window.open("http://booksearch.spree.com/books/bk_book_search_result.asp?x=BIGWOOFIE&link_id=14797365&Keywords="+keyword+"&Submit=search","spree",winopts(1,qty));
	forward(sp);
	var amz=window.open("http://www.amazon.com/exec/obidos/external-search?tag=bigwoofieenterta&keyword="+keyword+"&Submit=search&mode=books","amazon",winopts(2,qty));
	forward(amz);
	var beyond=window.open("http://www.beyond.com/AF19040/search.htm?Query=Query&toggle=name&name_desc="+keyword+"&Submit=Find","beyond",winopts(3,qty));
	forward(beyond);
	blurme();
}


function gogetmusic(keyword) {
	var qty=2;
	var sp=window.open("http://musicsearch.spree.com/music/search/searchengine.asp?x=BIGWOOFIE&link_id=14797475&SORT=ALBUM&search_type=pop_keyword&search_string="+keyword+"&Submit=search","spree",winopts(1,qty));
	forward(sp);
	var amz=window.open("http://www.amazon.com/exec/obidos/external-search?tag=bigwoofieenterta&keyword="+keyword+"&Submit=search&mode=music","amazon",winopts(2,qty));
	forward(amz);
	blurme();
	
}

function gogetcgames(keyword) {
	var qty=2;

	var beyond=window.open("http://www.beyond.com/AF19040/search.htm?Query=Query&toggle=name&name_desc="+keyword+"&Submit=Find","beyond",winopts(1,qty));
	forward(beyond);
	var etoy = window.open("http://www.etoys.com//cgi-bin/search.cgi?store=e&emp=es&keyword="+keyword+"&go=","etoy",winopts(2,qty));
	forward(etoy);
//	var amz=window.open("http://www.amazon.com/exec/obidos/external-search?tag=bigwoofieenterta&keyword="+keyword+"&Submit=search&mode=music","amazon",winopts(3,qty));
	blurme();
	}
function gogettoys(keyword) {
	var qty=1;
	var etoy = window.open("http://www.etoys.com//cgi-bin/search.cgi?store=e&emp=et&c=etC&keyword="+keyword+"&submit=http://images.fogdog.com/toolkit/images/find_button.gif","etoy",winopts(1,qty));
	forward(etoy);
	
//	var beyond=window.open("http://www.beyond.com/AF19040/search.htm?Query=Query&toggle=name&name_desc="+keyword+"&Submit=Find","beyond",winopts(2,qty));
//	var amz=window.open("http://www.amazon.com/exec/obidos/external-search?tag=bigwoofieenterta&keyword="+keyword+"&Submit=search&mode=music","amazon",winopts(3,qty));

	blurme();
}

function gogetsports(keyword) {
	var qty=1;
	var sports = window.open("http://service.bfast.com/bfast/click/sportsite?siteid=296773&bfpage=bigsearchbox&url=/cgi-bin/SSDsearch.cgi&search="+keyword+"&submit=","etoy",winopts(1,qty));
	forward(sports);
	
//	var beyond=window.open("http://www.beyond.com/AF19040/search.htm?Query=Query&toggle=name&name_desc="+keyword+"&Submit=Find","beyond",winopts(2,qty));
//	var amz=window.open("http://www.amazon.com/exec/obidos/external-search?tag=bigwoofieenterta&keyword="+keyword+"&Submit=search&mode=music","amazon",winopts(3,qty));

	blurme();
}



	function getURLvar(Name) {
		var search = Name + "="
		var incoming = window.location.search
		if (incoming.length > 0) { // if there are any search parameters
			offset = incoming.indexOf(search) 
			if (offset != -1) { // if parameter exists 
				offset += search.length 
				// set index of beginning of value
				end = incoming.indexOf("&", offset) 
				// set index of end of cookie value
				if (end == -1) 
					end = incoming.length
				value = unescape(incoming.substring(offset, end))
				if (value == "") {
					return null
				} else {
					return value
				}
			}
			else return null
		}
		else return null
	}
	



