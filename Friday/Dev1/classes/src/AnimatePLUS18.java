/* AnimatePLUS, Copyright 1996, Eric C Harshbarger.
This code is available for public use and modification as long as this notice of copyright is kept in tact. Additional credit is allowable for modifications.

Documentation on this applet may be found at:
http://www.auburn.edu/~harshec/WWW/slideshow.html

Questions or comments should be directed to:

Eric Harshbarger ( http://www.auburn.edu/~harshec/ )
harshec@mail.auburn.edu   OR    harshec@cdware.eng.sun.com   */

import java.applet.*;
import java.awt.*;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Rectangle;
import java.awt.Color;
import java.util.StringTokenizer;
import java.util.Vector;
import java.lang.*;
import java.util.Hashtable;
import java.net.URL;
import java.awt.image.*;
import java.net.MalformedURLException;

public class AnimatePLUS18 extends Applet implements Runnable {

	
	URL hotlink[];
	URL defaulturl;
	Thread woohoo = null;
	Image frame[];
	Image foo, tmpmoo, pixyimg, backimage, foreimage;
	Graphics hoo,tmpnoo,pixy;
	String posx[];
	String posy[];
	String transition[];
	String rantrans[] = new String[38]; //***At least the number of transitions in string below.
	String randomtrans = "SHRINK1 SHRINK2 SHRINK3 SHRINK4 SHRINK5 SHRINK6 SHRINK7 SHRINK8 SHRINK9 EXPAND1 EXPAND2 EXPAND3 EXPAND4 EXPAND5 EXPAND6 EXPAND7 EXPAND8 EXPAND9 SLIDEIN1 SLIDEIN2 SLIDEIN3 SLIDEIN4 SLIDEIN5 SLIDEIN6 SLIDEIN7 SLIDEIN8 SLIDEOUT1 SLIDEOUT2 SLIDEOUT3 SLIDEOUT4 SLIDEOUT5 SLIDEOUT6 SLIDEOUT7 SLIDEOUT8 SCROLL1 SCROLL3 SCROLL5 SCROLL7";
	String soundactivate;
	boolean background = false;
	boolean foreground = false;
	boolean def=false;
	boolean slidein=false;
	boolean slideout=false;
	boolean scroll=false;
	boolean expand=false;
	boolean shrink=false;
	boolean border=false;
	boolean bgcolor=false;
	boolean check=true;
	int pause[];
	int framenum=0;
	int iw,ih,dx,dy,fw,fh,ew,eh,px,py,previousx,previousy,defaultpause,finalpause,step;
	int cx=0;
	int cy=0;
	int number,blah,w,h,cycles,c,bordersize,red,green,blue,rate,defx,defy,bgr,bgg,bgb;
	AudioClip sounddefault;
	AudioClip sound[] = new AudioClip[100];
	

	public void init() {
		String param,frameindex,boo,positioning,piece;
		StringTokenizer tokens;
		Dimension roo = this.size();
		int k=0;

		param = getParameter("BACKGROUND");
		if (param != null) {
			background = true;
			backimage = getImage(getDocumentBase(), param+".gif");
		}

		param = getParameter("BGCOLOR");
		if (param != null) {
		bgcolor = true;
			if (param.equals("random")) {
				bgr = (int)(256*Math.random());
				bgg = (int)(256*Math.random());
				bgb = (int)(256*Math.random());
			}
			else {
				tokens = new StringTokenizer(param, ",");
				bgr = Integer.parseInt(tokens.nextToken());
				bgg = Integer.parseInt(tokens.nextToken());
				bgb = Integer.parseInt(tokens.nextToken());
			}
		}

		

		param = getParameter("FOREGROUND");
		if (param != null) {
			foreground = true;
			foreimage = getImage(getDocumentBase(), param+".gif");
		}

		param = getParameter("NUMBER");
		number = (param != null) ? Math.min(Integer.parseInt(param),100) : 1;

		param = getParameter("STEP");
		step = (param != null) ? Math.min(Integer.parseInt(param),100) : 10;

		param= getParameter("CYCLES");
		if (param != null) {
			if (param.equalsIgnoreCase("infinite")) {
				cycles = 1;
				c = 0;
			}
			else {
				cycles = Integer.parseInt(param);
				c = 1;
			}
		}
		else {
			cycles = 1;
			c = 0;
		}



		param= getParameter("RATE");
		rate = (param != null) ? Math.max(Integer.parseInt(param),10) : 100;

		w = Math.min(roo.width,500);
		h = Math.min(roo.height,500);

		param = getParameter("DIMENSIONS");
		if (param == null) { iw = w; ih = h;}
		else {
			iw = Math.min(Integer.parseInt(param.substring(0,param.indexOf(","))),500);
			ih = Math.min(Integer.parseInt(param.substring(param.indexOf(",")+1)),500);
		}


		param = getParameter("BORDER");
		if (param == null || param.equalsIgnoreCase("no")) {
			border = false;
		}
		else {
			border = true;
			bordersize = Math.max(0,Integer.parseInt(param));
		}

		param = getParameter("BORDERCOLOR").toLowerCase();
		if (param == null) { red=green=blue=0;}
		if (param.equals("random")) {
			border = true;
			red = (int)(256*Math.random());
			green = (int)(256*Math.random());
			blue = (int)(256*Math.random());
		}
		else {
			border = true;
			tokens = new StringTokenizer(param, ",");
			red = Integer.parseInt(tokens.nextToken());
			green = Integer.parseInt(tokens.nextToken());
			blue = Integer.parseInt(tokens.nextToken());
		}
		
		tokens = new StringTokenizer(randomtrans);
		while (tokens.hasMoreTokens()) {
			rantrans[k] = tokens.nextToken();
			k++;
		}

		frame = new Image[number];

		if (getParameter("FRAMEORDER") == null) {
			for (int i=0;i<number;i++) {
				frame[i] = getImage(getDocumentBase(), getParameter("FRAMENAME")+i+".gif");
			}
		}

		else {
			number = 0;
			frameindex = getParameter("FRAMEORDER")+",";
			while (frameindex.indexOf(",") != -1) {
				blah = frameindex.indexOf(",");
				frameindex = frameindex.substring(blah+1);
				number++;
			}
System.out.println(number);
			frame = new Image[number];
			frameindex = getParameter("FRAMEORDER")+",";
			for (int i=0;i<number;i++) {
				blah = frameindex.indexOf(",");
				boo = frameindex.substring(0,blah);
				frame[i] = getImage(getDocumentBase(), getParameter("FRAMENAME")+boo+".gif");
				frameindex = frameindex.substring(blah+1);
			}
		}


//*****NUMBER is now defined********

		hotlink = new URL[number];
		pause = new int[number];
		posx = new String[number];
		posy = new String[number];
		transition = new String[number];

		param = getParameter("POSITIONDEFAULT");
		if (param == null) {
			defx = defy = 0;
		}
		else {
			defx = Integer.parseInt(param.substring(param.indexOf("(")+1,param.indexOf(")")));
			param = param.substring(param.indexOf(")")+1);
			defy = Integer.parseInt(param.substring(param.indexOf("(")+1,param.indexOf(")")));
		}

		param = getParameter("POSITIONING");
		if (param != null && getParameter("TRANSITIONS") == null) {
			positioning = param+",";
			for (int i=0; i<number; i++) {
				piece = positioning.substring(0,positioning.indexOf(","));
				posx[i] = (piece.indexOf("&") != -1) ? piece.substring(0,positioning.indexOf("&")) : "+0";
				posy[i] = (piece.indexOf("&") != -1) ? piece.substring(positioning.indexOf("&")+1,positioning.indexOf(",")) : "+0";
				positioning = positioning.substring(positioning.indexOf(",")+1);
			}
		}
		else for (int i=0; i<number; i++) {
			posx[i]="("+String.valueOf(defx)+")";
			posy[i]="("+String.valueOf(defy)+")";
		}

		param = getParameter("URLDEFAULT");
		if (param != null) {
			try {
				defaulturl = new URL("http://"+param);
			}
			catch (Exception e) {}
		}
		else {
			try {
				defaulturl = new URL("http://www.auburn.edu/~harshec/WWW/slideshow.html");
			}
			catch (Exception e) {}
		}

		param = getParameter("URLORDER");
		if (param != null) {
			param = param+",";
			for (int i=0; i<number; i++) {
				blah = param.indexOf(",");
				boo = (blah !=-1) ? param.substring(0,blah) : "";
				if (boo.equals("")) {
					try {
						hotlink[i] = defaulturl;
					}
					catch (Exception e) {}
				}
				else {
					try {
						hotlink[i] = new URL("http://"+boo);
					}
					catch (MalformedURLException e) {}
				}
				param = param.substring(blah+1);
			}
		}

		param= getParameter("PAUSE");
		defaultpause = (param != null) ? Integer.parseInt(param) : 200;


		if (getParameter("PAUSEORDER") == null) {
			for (int i=0;i<number;i++) {
				pause[i] = defaultpause;
			}
		}
		else {
			param = getParameter("PAUSEORDER")+",";
			for (int i=0;i<number;i++) {
				blah = param.indexOf(",");
				boo = (blah !=-1) ? param.substring(0,blah) : "";

				pause[i] = (boo.equals("")) ? defaultpause : Integer.parseInt(boo);

				param = param.substring(blah+1);
			}
		}

		param = getParameter("SOUNDDEFAULT");
		sounddefault = (param != null) ?  getAudioClip(getDocumentBase(),"audio/"+param+".au") : null;


		param = getParameter("SOUNDACTIVATE");
		soundactivate = (param == null) ? "enter" : param.toLowerCase();

		param = getParameter("SOUNDORDER");
		if (param != null) {
			param = param+",";
			for (int i=0;i<number;i++) {
				blah = param.indexOf(",");
				boo = (blah !=-1) ? param.substring(0,blah) : "";

				sound[i] = (boo.equals("")) ?  sounddefault : getAudioClip(getDocumentBase(),"audio/"+boo+".au");
				param = param.substring(param.indexOf(",")+1);
			}
		}
		else for (int i=0;i<number;i++) {
			sound[i] = sounddefault;
		}
				

		if (getParameter("TRANSITIONS") != null && getParameter("TRANSITIONS").equals("random") != true ){
			param = getParameter("TRANSITIONS")+",";
			for (int i=0;i<number;i++) {
				blah = param.indexOf(",");
				boo = (blah !=-1) ? param.substring(0,blah) : "";

				transition[i] = (boo.equals("")) ? "D" : boo;

				param = param.substring(blah+1);
			}
		}

		else {
			for (int i=0;i<number;i++) {
				transition[i] = "D";
			}
		}

		int maxdim = Math.max(iw,ih);

		foo = createImage(roo.width,roo.height);
		hoo = foo.getGraphics();

	}


	public void paint(Graphics goo) {
		paintBuffer(hoo);
		goo.drawImage(foo,0,0,this);
	}

	public void paintBuffer(Graphics g) {
		g.clipRect(0,0,w,h);


		if (bgcolor) {
			Color backcolor = new Color(bgr,bgg,bgb);
			g.setColor(backcolor);
			g.fillRect(0,0,w,h);
		}

		if (background) {
			g.drawImage(backimage, 0,0,this);
		}

		if (def) {
			g.drawImage(frame[framenum], px,py,iw,ih,this);
		}

		else if (slidein) {
			g.drawImage(frame[(framenum)], px+0,py+0,iw,ih,this);
			g.drawImage(frame[(framenum+1)%number], px+dx,py+dy,iw,ih,this);
		}
		else if (slideout) {
			g.drawImage(frame[(framenum+1)%number], px+0,py+0,iw,ih,this);
			g.drawImage(frame[(framenum)%number], px+dx,py+dy,iw,ih,this);
		}	
		else if (scroll) {
			g.drawImage(frame[(framenum+1)%number], px+cx,py+cy,iw,ih,this);
			g.drawImage(frame[(framenum)%number], px+dx,py+dy,iw,ih,this);
			cx=0;cy=0;
		}
		else if (expand) {
			g.drawImage(frame[(framenum)],px+0,py+0,iw,ih,this);
			g.drawImage(frame[(framenum+1)%number],px+cx,py+cy,ew,eh,this);
		}
		else if (shrink) {
			g.drawImage(frame[(framenum+1)%number],px+0,py+0,iw,ih,this);
			if (ew != 0 && eh != 0) {
				g.drawImage(frame[(framenum)],px+cx,py+cy,ew,eh,this);
			}
		}
	
		if (foreground) {
			g.drawImage(foreimage, 0,0,this);
		}
		if (border) {
			Color bordercolor = new Color(red,green,blue);
			g.setColor(bordercolor);
			for (int i=0;i<bordersize-1;i++) {
				g.drawRect(0+i,0+i,w-1-(2*i),h-1-(2*i));
			}
		}
	}


	public void update(Graphics g) {
		paint(g);
	}

	public void start() {
		if (woohoo == null) {
			woohoo = new Thread(this);
			woohoo.start();
		}
	}

/*	public void stop () {
		woohoo = null;
	}*/

	public void run() {
		for (int k=0;k<(cycles*number-1);k=k+c) {
		try {Thread.sleep(pause[framenum]);} catch (InterruptedException e){};
		dx=dy=cx=cy=px=py=0;
		ew=w;eh=h;
		def=slidein=slideout=scroll=expand=shrink=false;
		background = (getParameter("BACKGROUND") != null) ? true : false;

		if (getParameter("TRANSITIONS") != null && getParameter("TRANSITIONS").equalsIgnoreCase("random")) {
			transition[framenum] = rantrans[(int)(38*Math.random())];
		}

		if (posx[framenum].indexOf("+") != -1) {
			px = (framenum == 0) ? 0+Integer.parseInt(posx[framenum].substring(1)) : previousx+Integer.parseInt(posx[framenum].substring(1));
		}
		else if (posx[framenum].indexOf("-") != -1 && posx[framenum].indexOf("(") == -1) {
			px = (framenum == 0) ? 0-Integer.parseInt(posx[framenum].substring(1)) : previousx-Integer.parseInt(posx[framenum].substring(1));
		}
		else {
			px = Integer.parseInt(posx[framenum].substring(posx[framenum].indexOf("(")+1,posx[framenum].indexOf(")")));
		}

		if (posy[framenum].indexOf("+") != -1) {
			py = (framenum == 0) ? 0+Integer.parseInt(posy[framenum].substring(1)) : previousy+Integer.parseInt(posy[framenum].substring(1));
		}
		else if (posy[framenum].indexOf("-") != -1 && posx[framenum].indexOf("(") == -1) {
			py = (framenum == 0) ? 0-Integer.parseInt(posy[framenum].substring(1)) : previousy-Integer.parseInt(posy[framenum].substring(1));
		}
		else {
			py = Integer.parseInt(posy[framenum].substring(posy[framenum].indexOf("(")+1,posy[framenum].indexOf(")")));
		}

			previousx = px;
			previousy = py;


		if (transition[framenum].equals("D")) {
			def = true;
			repaint();
		}

		else if (transition[framenum].indexOf("SLIDEIN") != -1) {
			slidein = true;
			String temptransition = transition[framenum];
			for (int j=1;j<step+1;j++) {
				if (temptransition.indexOf("RANDOM") != -1) {
					temptransition = String.valueOf((int)(8*Math.random()+1));
				}

				if (temptransition.indexOf("1") != -1) {
					dy = (int)(-ih+j*ih/step);
				}
				else if (temptransition.indexOf("2") != -1) {
					dx = (int)(iw-j*iw/step);
					dy = (int)(-ih+j*ih/step);
				}
				else if (temptransition.indexOf("3") != -1) {
					dx = (int)(iw-j*iw/step);
				}
				else if (temptransition.indexOf("4") != -1) {
					dx = (int)(iw-j*iw/step);
					dy = (int)(ih-j*ih/step);
				}
				else if (temptransition.indexOf("5") != -1) {
					dy = (int)(ih-j*ih/step);
				}
				else if (temptransition.indexOf("6") != -1) {
					dx = (int)(-iw+j*iw/step);
					dy = (int)(ih-j*ih/step);
				}
				else if (temptransition.indexOf("7") != -1) {
					dx = (int)(-iw+j*iw/step);
				}
				else if (temptransition.indexOf("8") != -1) {
					dx = (int)(-iw+j*iw/step);
					dy = (int)(-ih+j*ih/step);
				}
				repaint();
				try {Thread.sleep(rate);} catch (InterruptedException e){};
			}
		}
		else if (transition[framenum].indexOf("SLIDEOUT") != -1) {
			slideout = true;
			String temptransition = transition[framenum];
			for (int j=1;j<step+1;j++) {
				if (temptransition.indexOf("RANDOM") != -1) {
					temptransition = String.valueOf((int)(8*Math.random()+1));
				}

				if (temptransition.indexOf("1") != -1) {
					dy = (int)(-j*ih/step);
				}
				else if (temptransition.indexOf("2") != -1) {
					dx = (int)(j*iw/step);
					dy = (int)(-j*ih/step);
				}
				else if (temptransition.indexOf("3") != -1) {
					dx = (int)(j*iw/step);
				}
				else if (temptransition.indexOf("4") != -1) {
					dx = (int)(j*iw/step);
					dy = (int)(j*ih/step);
				}
				else if (temptransition.indexOf("5") != -1) {
					dy = (int)(j*ih/step);
				}
				else if (temptransition.indexOf("6") != -1) {
					dx = (int)(-j*iw/step);
					dy = (int)(j*ih/step);
				}
				else if (temptransition.indexOf("7") != -1) {
					dx = (int)(-j*iw/step);
				}
				else if (temptransition.indexOf("8") != -1) {
					dx = (int)(-j*iw/step);
					dy = (int)(-j*ih/step);
				}
				repaint();
				try {Thread.sleep(rate);} catch (InterruptedException e){};
			}
		}
		else if (transition[framenum].indexOf("SCROLL") != -1) {
			scroll = true;
			String temptransition = transition[framenum];
			for (int j=1;j<step+1;j++) {
				if (temptransition.indexOf("RANDOM") != -1) {
					temptransition = String.valueOf(2*(int)(4*Math.random())+1);
				}

				if (temptransition.indexOf("1") != -1) {
					cy = (int)(-ih+j*ih/step);
					dy = cy+ih;
				}
				else if (temptransition.indexOf("3") != -1) {
					cx = (int)(iw-j*iw/step);
					dx = cx-iw;
				}
				else if (temptransition.indexOf("5") != -1) {
					cy = (int)(ih-j*ih/step);
					dy = cy-ih;
				}
				else if (temptransition.indexOf("7") != -1) {
					cx = (int)(-iw+j*iw/step);
					dx = cx+iw;
				}
				repaint();
				try {Thread.sleep(rate);} catch (InterruptedException e){};
			}
		}
		else if (transition[framenum].indexOf("EXPAND") != -1) {
			expand = true;
			String temptransition = transition[framenum];
			for (int j=1;j<step+1;j++) {
				ew = (int)(j*iw/step);
				eh = (int)(j*ih/step);
				if (temptransition.indexOf("RANDOM") != -1) {
					temptransition = String.valueOf((int)(9*Math.random()+1));
				}

				if (temptransition.indexOf("1") != -1) {
					cx = (int)(iw/2-j*iw/(2*step));
				}
				else if (temptransition.indexOf("2") != -1) {
					cx = (int)(iw-j*iw/step);
				}
				else if (temptransition.indexOf("3") != -1) {
					cx = (int)(iw-j*iw/step);
					cy = (int)(ih/2-j*ih/(2*step));
				}
				else if (temptransition.indexOf("4") != -1) {
					cx = (int)(iw-j*iw/step);
					cy = (int)(ih-j*ih/step);
				}
				else if (temptransition.indexOf("5") != -1) {
					cx = (int)(iw/2-j*iw/(2*step));
					cy = (int)(ih-j*ih/step);
				}
				else if (temptransition.indexOf("6") != -1) {
					cy = (int)(ih/2-j*ih/(2*step));
				}
				else if (temptransition.indexOf("7") != -1) {
					cy = (int)(ih/2-j*ih/(2*step));
				}
				else if (temptransition.indexOf("8") != -1) {
				}
				else if (temptransition.indexOf("9") != -1) {
					cx = (int)(iw/2-j*iw/(2*step));
					cy = (int)(ih/2-j*ih/(2*step));
				}
				else if (temptransition.indexOf("H") != -1) {
					cy = (int)(ih/2-j*ih/(2*step));
					ew = iw;
				}
				else if (temptransition.indexOf("V") != -1) {
					cx = (int)(iw/2-j*iw/(2*step));
					eh = ih;
				}
				repaint();
				try {Thread.sleep(rate);} catch (InterruptedException e){};
			}
		}
		else if (transition[framenum].indexOf("SHRINK") != -1) {
			shrink = true;
			String temptransition = transition[framenum];
			for (int j=1;j<step+1;j++) {
				ew = (int)(iw-j*iw/step);
				eh = (int)(ih-j*ih/step);
				if (temptransition.indexOf("RANDOM") != -1) {
					temptransition = String.valueOf((int)(9*Math.random()+1));
				}

				if (temptransition.indexOf("1") != -1) {
					cx = (int)(j*iw/(2*step));
				}
				else if (temptransition.indexOf("2") != -1) {
					cx = (int)(j*iw/step);
				}
				else if (temptransition.indexOf("3") != -1) {
					cx = (int)(j*iw/step);
					cy = (int)(j*ih/(2*step));
				}
				else if (temptransition.indexOf("4") != -1) {
					cx = (int)(j*iw/step);
					cy = (int)(j*ih/step);
				}
				else if (temptransition.indexOf("5") != -1) {
					cx = (int)(j*iw/(2*step));
					cy = (int)(j*ih/step);
				}
				else if (temptransition.indexOf("6") != -1) {
					cy = (int)(j*ih/(2*step));
				}
				else if (temptransition.indexOf("7") != -1) {
					cy = (int)(j*ih/(2*step));
				}
				else if (temptransition.indexOf("8") != -1) {
				}
				else if (temptransition.indexOf("9") != -1) {
					cx = (int)(j*iw/(2*step));
					cy = (int)(j*ih/(2*step));
				}
				else if (temptransition.indexOf("V") != -1) {
					cx = (int)(j*iw/(2*step));
					eh = ih;
				}
				else if (transition[framenum].indexOf("H") != -1) {
					cy = (int)(j*ih/(2*step));
					ew = iw;
				}
				repaint();
				try {Thread.sleep(rate);} catch (InterruptedException e){};
			}
		}
		if (sound[framenum] != null && soundactivate.equals("auto")) {
			sound[(framenum+1)%number].play();
		}

		framenum = (framenum+1)%number;
		}

		woohoo = null;
	}


	public boolean mouseEnter(java.awt.Event evt, int mx, int my) {
		if (sound[framenum] != null && soundactivate.equals("enter")) {
			sound[framenum].play();
		}
		if (hotlink[framenum] != null) {
			getAppletContext().showStatus(hotlink[framenum].toString());
		}
		return true;
	}

	public boolean mouseExit(java.awt.Event evt, int mx, int my) {
		getAppletContext().showStatus("AnimatePLUS Applet");
		return true;
	}

	public boolean mouseDown(java.awt.Event evt, int mx, int my) {
		URL moo;
		moo = (hotlink[framenum] == null) ? defaulturl : hotlink[framenum];
		if (sound[framenum] != null && soundactivate.equals("click")) {
			sound[framenum].play();
		}
		try {
			getAppletContext().showDocument(moo);
		} catch ( Exception e ) {}
		return true;
	}



}
