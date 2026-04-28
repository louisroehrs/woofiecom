
gamecount=30;
           function PickGameAndPlay() {{
		a = Math.random() * gamecount;
		a = Math.floor(a);
		URL =   a + ".tmpl";
		window.location = URL;
	}

	function GetCell(x,y) {{
		var xstartGetCell = x;
		var xstopGetCell  = x+1; 
		woofie="st:" + xstartGetCell + " stp:" + xstopGetCell
	//	alert(woofie);
		return (puzzle[y].substring(xstartGetCell, xstopGetCell));
	}

	function DisplayStatus(iPointsSelected) {{

		if (iPointsSelected == 0) {{
			status = "Select the first letter of the word.";
		} else {{
			status = "Select the last letter of the word.";
		}
	}

	sGameState="inplay";
	iMinutesLeft = 4;
	iSecondsLeft = 15;
	kOtherFormElements = 22;
	kHintLength = 3000; // 1.5sec
	var sImagePath = "../images/";
	LoadImages();
	

	iPointsSelected = 0;
	iStartX = 0;  iStopX = 0;
	iStaryY = 0;  iStopY = 0;
              
	iWordsLeft  = iTotalWords;
		  
	abWordFound = new Array(iTotalWords);
	for (i=0; i < iTotalWords; i++)
		abWordFound[i] = "false";
	
	DisplayStatus(iPointsSelected);
	sLetterLookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	
	function RandomLetter() {{
		iLetterASCII = Math.round(Math.random()*25);
		return(sLetterLookup.charAt(iLetterASCII));
	}

	function BuildPuzzle() {{

		puzzle = new Array(kHeight);
	
		for (y=0; y < kHeight; y++) {{
			puzzle[y] = "";
				for (x=0; x < kWidth; x++) {{
					if (GetInCell(x,y) == "+") {{
						puzzle[y] = puzzle[y] + RandomLetter();
					} else {{
						puzzle[y] = puzzle[y] + GetInCell(x,y);
				}			
			}
		}

	}

	function CheckSelection(iStartX, iStartY, iStopX, iStopY) {{
		var i=0;
		for (i=0; i < iTotalWords; i++) {{
	      if (iStartX == eval(aStartX[i]) &&
				iStartY == eval(aStartY[i]) &&
				iStopX == eval(aStopX[i]) &&
				iStopY == eval(aStopY[i]) ||
		      	iStopX == eval(aStartX[i]) &&
				iStopY == eval(aStartY[i]) &&
				iStartX == eval(aStopX[i]) &&
				iStartY == eval(aStopY[i])) {{

				return (i);
			}
	
		}
		return (-1);
		
	}
	
	function StartLevel() {{
		sGameState="inplay";
	}

	function ComputeSlope(fDiff) {{
                 
		var fSlope;
	
		if (fDiff == 0) {{
			fSlope = 0;
	 	} else {{
			if (fDiff < 0) {{
	 			fSlope = -1;
			} else {{
				fSlope = 1;
			}
		}   
	
		return(fSlope); 
	}

	function pos(x,y)  {{
		var position = x + (y * kWidth) +  kOtherFormElements;
		return (position);
	}
	
	function HintLetter(iStartX, iStartY, iStopX, iStopY, iLetter, bSelected, sSaveImg) {{
		var fxDiff = iStopX - iStartX;
		var fyDiff = iStopY - iStartY;

		var fySlope = ComputeSlope(fyDiff);
		var fxSlope = ComputeSlope(fxDiff);

		var iCurrX = iStartX + iLetter * fxSlope;  
		var iCurrY = iStartY + iLetter * fySlope;  
		var position = pos(iCurrX,iCurrY);
		if (bSelected == "true") {{
			var sSaveImag = document.images[position].src;
			document.images[position].src = sImagePath + GetCell(iCurrX, iCurrY)+"ONN.JPG";

			return (sSaveImag);
		} else {{
			document.images[position].src = sSaveImg;
		}
		return (sSaveImg);
	}

	function HighlightSelection(iStartX, iStartY, iStopX, iStopY) {{
		var position = 0;
		var fxDiff = iStopX - iStartX;
		var fyDiff = iStopY - iStartY;

		var fxSlope = ComputeSlope(fxDiff);
		var fySlope = ComputeSlope(fyDiff);

		iCurrX = iStartX;
		iCurrY = iStartY;

		while ( (iCurrX != iStopX) || (iCurrY != iStopY) ) {{
		position = pos(iCurrX,iCurrY);

//	   alert("first"+GetCell(iCurrX, iCurrY)+"ONN.JPG");
		document.images[ position ].src = sImagePath+GetCell(iCurrX, iCurrY)+"ONN.JPG";
	    
		iCurrX = iCurrX + fxSlope;
		iCurrY = iCurrY + fySlope;
				      
	}
		position = pos(iCurrX,iCurrY);
//		  alert("2nd"+GetCell(iCurrX, iCurrY)+"ONN.JPG");
	      document.images[position].src = sImagePath+GetCell(iCurrX, iCurrY)+"ONN.JPG";
	    
		}

        function PlaySound(sound) {{

          if (sound == null) {{  
            return;
          } else {{
            sound.play(false);
          }

        }
	function SelectEndpoint(x,y) {{

		if (sGameState == "preplay") {{
			StartLevel();
		}

		if (sGameState != "inplay")
			return;
			
		// alert("game inplay");



		if (iPointsSelected == 0) {{
			iStartX = x;
			iStartY = y;
			iPointsSelected = 1;
			// alert("first point");
			DisplayStatus(iPointsSelected);
			// alert("display status ok");
			sSelectEndOld = HintLetter(x, y, x, y, 0, "true", "");
			// alert("hint letters ok");
			return;
		}

		iStopX = x;
		iStopY = y;
		if ((iStopX == iStartX) && (iStopY == iStartY)) {{
			iPointsSelected = 0;
			DisplayStatus(iPointsSelected);
			HintLetter(iStopX, iStopY, iStopX, iStopY, 0, "false", sSelectEndOld);
			return;
		}
		// alert("before check seleciton");
		iWordSelected = CheckSelection(iStartX, iStartY, iStopX, iStopY);
		// alert(iWordSelected);
		if ((iWordSelected != -1) && (abWordFound[iWordSelected] != "true")) {{
			abWordFound[iWordSelected] = "true";
			// alert(10);
			HighlightSelection(iStartX, iStartY, iStopX, iStopY);
			
			ComputeWordsLeft();

			UpdateWordsLeft();

			PlaySound(document.bell);
		} else {{

			HintLetter(iStartX, iStartY, iStopX, iStopY, 0, "false", sSelectEndOld);

			PlaySound(document.buzzer);
		} 
		iPointsSelected = 0;
		DisplayStatus(iPointsSelected);

	}



	function GetDigit(iNumber, iDigit) {{

	  iNumber = "" + iNumber;  // Convert to "String" if it isn't already...

	  while (iNumber.length < 2) {{
	    iNumber = "0" + iNumber;
	  }

		  return(iNumber.charAt(iDigit));

		}

       
			

	function GetInCell(x, y) {{
		var end = x+1;
		letter = inpuzzle[y].substring(x, end)
		return (letter.toUpperCase());
	}

	function ComputeWordsLeft() {{

	  iWordsLeft = 0;
	  for (i=0; i < iTotalWords; i++) {{
	     if (abWordFound[i] == "false")
	       iWordsLeft++;
	  }

	  if (eval(iWordsLeft) == 0) {{
	    
	    sGameState = "won";
	    PlaySound(document.applause);
	    window.location="../win.tmpl";
			
	  }

	}

	function UpdateWordsLeft() {{

	  if (eval(iWordsLeft) >= 10) {{
	    document.twords.src = sImagePath+GetDigit(iWordsLeft, 0)+".gif";         
	      } else {{
		    document.twords.src = "/ROMCache/spacer.gif";
		  }
			   
	      document.owords.src = sImagePath+GetDigit(iWordsLeft, 1)+".gif";         

	}


	function LoadImages() {{

		image0 = new Image();
		image0.src = sImagePath + "0.gif";


		  image1 = new Image();
	  image1.src = sImagePath+"1.gif";

	      image2 = new Image();
	  image2.src = sImagePath+"2.gif";

		  image3 = new Image();
	  image3.src = sImagePath+"3.gif";

		  image4 = new Image();
	  image4.src = sImagePath+"4.gif";

		  image5 = new Image();
	  image5.src = sImagePath+"5.gif";

	      image6 = new Image();
	  image6.src = sImagePath+"6.gif";

		  image7 = new Image();
	  image7.src = sImagePath+"7.gif";

	      image8 = new Image();
	  image8.src = sImagePath+"8.gif";

	  imageAON = new Image();
	  imageAON.src = sImagePath+"AONN.JPG";
	  imageBON = new Image();
	  imageBON.src = sImagePath+"BONN.JPG";
	  imageCON = new Image();
	  imageCON.src = sImagePath+"CONN.JPG";
	  imageDON = new Image();
	  imageDON.src = sImagePath+"DONN.JPG";
	  imageEON = new Image();
	  imageEON.src = sImagePath+"EONN.JPG";
	  imageFON = new Image();
	  imageFON.src = sImagePath+"FONN.JPG";
	  imageGON = new Image();
	  imageGON.src = sImagePath+"GONN.JPG";
	  imageHON = new Image();
	  imageHON.src = sImagePath+"HONN.JPG";
	  imageION = new Image();
	  imageION.src = sImagePath+"IONN.JPG";
	  imageJON = new Image();
	  imageJON.src = sImagePath+"JONN.JPG";
	  imageKON = new Image();
	  imageKON.src = sImagePath+"KONN.JPG";
	  imageLON = new Image();
	  imageLON.src = sImagePath+"LONN.JPG";
	  imageMON = new Image();
	  imageMON.src = sImagePath+"MONN.JPG";
	  imageNON = new Image();
	  imageNON.src = sImagePath+"NONN.JPG";
	  imageOON = new Image();
	  imageOON.src = sImagePath+"OONN.JPG";
	  imagePON = new Image();
	  imagePON.src = sImagePath+"PONN.JPG";
	  imageQON = new Image();
	  imageQON.src = sImagePath+"QONN.JPG";
	  imageRON = new Image();
	  imageRON.src = sImagePath+"RONN.JPG";
	  imageSON = new Image();
	  imageSON.src = sImagePath+"SONN.JPG";
	  imageTON = new Image();
	  imageTON.src = sImagePath+"TONN.JPG";
	  imageUON = new Image();
	  imageUON.src = sImagePath+"UONN.JPG";
	  imageVON = new Image();
	  imageVON.src = sImagePath+"VONN.JPG";
	  imageWON = new Image();
	  imageWON.src = sImagePath+"WONN.JPG";
	  imageXON = new Image();
	  imageXON.src = sImagePath+"XONN.JPG";
	  imageYON = new Image();
	  imageYON.src = sImagePath+"YONN.JPG";
	  imageZON = new Image();
	  imageZON.src = sImagePath+"ZONN.JPG";
		status="WebTV WordFinder";
	}


	function RenderCell(x, y) {{ 

		letter = GetCell(x,y);

		document.write("<td abswidth=20 width=20 absheight=20 height=20 bgcolor=666666 align=center valign=bottom>");
		document.write("  <a selected href=\"javascript:SelectEndpoint("+x+","+y+")\"><img src="+sImagePath+letter+"OFF.JPG></a>");
		document.write("</td>");
}

	    function RenderRow(y) {{

	  document.write("<tr>");

	  for (x=0; x < kWidth; x++) {{
	     RenderCell(x,y);
	  }

	  document.write("</tr>");

	}

	function RenderPuzzle() {{
	 
	  document.write("<table border=0 cellspacing=3 cellpadding=0 bgcolor=222222>");

	  for (y=0; y < kHeight; y++) {{
	     RenderRow(y);
	  }

 	       document.write("</table>");

	     }

		function Restart() {{
		  location.reload();
		}

		function Quit() {{
			window.location="wtv-home:/home";
		}

		function SolvePuzzle() {{

		  for (i=0; i < iTotalWords; i++) {{
		  
		     var startx = eval(aStartX[i]);
		     var starty = eval(aStartY[i]);
		     var stopx  = eval(aStopX[i]);
		     var stopy  = eval(aStopY[i]);      
		  
		     abWordFound[i] = "true";
		     HighlightSelection(startx,starty,stopx,stopy);
		     
		  }

		  sGameState = "solved";
		  iWordsLeft = 0;
		  UpdateWordsLeft();

		}

		function Highlight1LengthWords() {{

		  for (i=0; i < iTotalWords; i++) {{
		     var startx = aStartX[i];
			 if (aLength[i] == 1) {{
               HighlightSelection(eval(aStartX[i]), eval(aStartY[i]), eval(aStopX[i]), eval(aStopY[i]));
               abWordFound[i] = "true";
             }
          }

		}

		function ShowHint() {{
			var iHintAnswer=0;
			var iHintLetter=0;
		  // Find Answer to Hint

		  if (sGameState != "inplay")
		    return;

		  for (iHintAnswer=0;(abWordFound[iHintAnswer] != "false") && (iHintAnswer < iTotalWords); iHintAnswer++ ) {{ }


		  if (iHintAnswer == iTotalWords)
		    return;


		  // Find Letter to Hint

		  iHintLetter = Math.round(Math.random()*(aLength[iHintAnswer]-1));

		  // Invert Letter


		
		  //  PlaySound(document.swoosh);
		  var a1 = eval(aStartX[iHintAnswer]);
		  var a2 = eval(aStartY[iHintAnswer]);
		  var a3 = eval(aStopX[iHintAnswer]);
		  var a4 = eval(aStopY[iHintAnswer]);
		  sHintOld = HintLetter(a1,a2,a3,a4, iHintLetter, "true", "");


		  // Set Timer to Reinvert.
	  
		  sCommand = "HintLetter(" + eval(aStartX[iHintAnswer]) + "," + eval(aStartY[iHintAnswer]) + "," + eval(aStopX[iHintAnswer]) + "," + eval(aStopY[iHintAnswer]) + "," + iHintLetter + ",\"false\",\"" + sHintOld + "\")";
	  window.setTimeout(sCommand, kHintLength);

		 
	
		}
