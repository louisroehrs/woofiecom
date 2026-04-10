

var intMenuShiftAmount=150;
var intMenuCurrentShift=0;

var ie6 = (navigator.userAgent.indexOf("MSIE 6.")>-1);

function init() {
   
   function setupMenu(element) {
      var menus = $(element + " ul");
      var largestMenuSize=0;
      var menuEntryHeight= $("#gennav li").outerHeight();
      lists= menus ;
      for (i=0; i< lists.size(); i++) {
         largestMenuSize = Math.max(largestMenuSize, $(lists[i]).children().size());
      }

      var genreNavHeight=menuEntryHeight*largestMenuSize;
      $(element).css("height",genreNavHeight);

      if (ie6) {
        $("#gennav").removeClass(":hover");

        $(element +" li").not(".genre").mouseover(function(event) {
           if ($(event.target).is("li")) {
             $(event.target).css("background-color","#ccc");
           }
           event.stopPropagation();
         });

         $(element +" li").not(".genre").mouseout(function(event) {
           if ($(event.target).is("li")) {
             $(event.target).css("background-color","transparent");
           }
           event.stopPropagation();
         });
      }

      $(element +" .hasmore").click(function(event) {
        if ($(event.target).is(".hasmore")) {
          $(event.target).children().show();
          intMenuCurrentShift-=intMenuShiftAmount;
          $(element +" #top").animate({left:intMenuCurrentShift},200);
        }
        event.stopPropagation();
      })

      $(element +" .back").click(function(event) {
        intMenuCurrentShift+=intMenuShiftAmount;
        $("#top").animate({left:intMenuCurrentShift},200,"linear",
           function() {$(event.target).parent().hide();} );
        event.stopPropagation();
      })
   }

   setupMenu("#gennav");
   
}

$().ready(init);

