<script language="JavaScript1.2">
	<!-- This script and many more are available free online at -->
	<!-- The JavaScript Source!! http://javascript.internet.com -->
	<!-- Modified by Flash kit  http://www.flashkit.com -->

	function shake_xy(n) {
	if (self.moveBy) {
		for (i = 10; i > 0; i--) {
			for (j = n; j > 0; j--) {
			self.moveBy(0,i);
			self.moveBy(i,0);
			self.moveBy(0,-i);
			self.moveBy(-i,0);
		    }
	      }
	   }
	setTimeout("powerdown()",2000);
	}

	function shake_x(n) {
	if (self.moveBy) {
		for (i = 10; i > 0; i--) {
			for (j = n; j > 0; j--) {
			self.moveBy(i,0);
			self.moveBy(-i,0);
		    }
	      }
	   }
	}

	function shake_y(n) {
	if (self.moveBy) {
		for (i = 10; i > 0; i--) {
			for (j = n; j > 0; j--) {
			self.moveBy(0,i);
			self.moveBy(0,-i);
		    }
	      }
	   }
	}

	function powerdown() {
	    location = "dark.html";
//	 	document.bgColor="000000";
//		document.alinkColor = "000000";
//		document.vlinkColor = "000000";
//		document.linkColor = "000000";
//		document.fgColor = "000000";
	}

	function powerup() {
	 	document.bgColor="ffffff";
		document.alinkColor = "0000ff";
		document.vlinkColor = "0000ff";
		document.linkColor = "0000ff";
		document.fgColor = "0000ff";
		setTimeout("self.shake_xy(10)",5000);
	}
	//-->
</script>
