/*
 * David Nicol
 * Calum Smeaton
 *
 * Aug 28, 1995
 * by David Nicol d.nicol@virtual-inn.co.uk
 *    Calum Smeaton, calum@virtual-inn.co.uk
 *
 * Orbital Technologies Limited
 * 
 */

import java.util.*;
import java.applet.*;
import java.io.*;
import java.awt.*;
import java.net.*;

/**
 * The Advertising Space Applet
 *
 * @author D. Nicol & C. Smeaton
 **/

public class adSpace extends Applet implements Runnable {

  /**
   * Internal width and height
   **/
  int width,height;

  /**
   * Records whether the mouse is within the applet or not
   **/
  boolean mouseIn=false;

  /**
   * The thread that does the animation etc.
   **/
  Thread kicker=null;

  /**
   * Boolean variable to track whether the applet is running or not
   **/
  boolean running=false;

  /**
   * Index of currently displayed advert in Vector of advert objects
   **/
  int curIndex=0;

  /**
   * Boolean to record whether the animation is in progress or not
   **/
  boolean inScroll=false;

  /**
   * Handle to the current Advert object
   **/
  Advert curAdvert;

  /**
   * Handle to the next Advert object
   **/
  Advert newAdvert;

  /**
   * Length of time (milliseconds) to to display advert, before
   * animating to the next applet (default 4000)
   **/
  int pause=4000;

  /**
   * Pause between animation frames (default 100)
   **/
  int scrollPause=100;

  /**
   * The number of pixels between each frame in the scrolling animation
   **/
  int deltaY=2;

  /**
   * Number of frames in each scrolling animation. Defaults to -1 to
   * ensure initialisation
   **/
  int numFrames=-1;

  /**
   * Global audio clip played at the commencement of each animation
   **/
  AudioClip aniAudio = null;

  /**
   * Array of Advert objects. 1 Advert is created for each '{' '}' pair
   * found while parsing the configuration file
   **/
  Vector adverts = new Vector();

  /**
   * Total number of advers
   **/
  int numAds;
	

  /**
   * Loads configuration file and images/audio. Sets up dimensions,
   * animation style etc.
   **/
  public void init() {

        // Get the html parameters
	String adList = getParameter("adList");
	if (adList == null) {
		adList = "adlist.txt";
	}
	System.out.println("Got param: adList = " + adList);
   
        // retrieve the config file and parse it. This also creates
        // the array of Advert's
	parse_adlist(adList);
        System.out.println("Got " + adverts.size() + " adverts");

  	String attr;
	attr=getParameter("pause");
	if (attr == null) {
		pause = 4000;
	} else {
		pause = Integer.parseInt(attr);
	}
	attr=getParameter("deltaY");
	if (attr == null) {
		deltaY = 2;
	} else {
		deltaY = Integer.parseInt(attr);
	}
	attr=getParameter("scrollPause");
	if (attr == null) {
		scrollPause = 40;
	} else {
		scrollPause = Integer.parseInt(attr);
	}
	attr=getParameter("numFrames");
	if (attr == null) {
		numFrames = -1;
	} else {
		numFrames = Integer.parseInt(attr);
	}
	attr=getParameter("aniAudio");
	if (attr == null) {
		aniAudio = null;
	} else {
		try {aniAudio = getAudioClip(new URL(getDocumentBase(),attr));} 
		catch (java.net.MalformedURLException e){};
	}

	numAds = adverts.size();

	curAdvert = (Advert)adverts.elementAt(0);
	newAdvert = curAdvert;
	curIndex=1;

        resize (curAdvert.image.getWidth(this), curAdvert.image.getHeight(this));
        width = size().width;
        height = size().height;

	if (numFrames != -1) {
		// ie. precedence goes to the user setting number of frames
		// in a scroll
		System.out.println("Overriding deltaY from " + deltaY + " to " +
					(size().height / numFrames) + " ie. " + numFrames +
					" frames");
		deltaY = size().height / numFrames;
	} else {
		numFrames = (int) Math.round((double)size().height / (double)deltaY);
	}

	try {
                im = createImage(size().width,size().height);
		out = im.getGraphics();
                System.out.println("GOT DOUBLE BUFFERING");
	} catch (Exception e) {
		// double-buffering not available
		out = null;
                System.out.println("NO DOUBLE BUFFERING");
	}
  }

  /**
   * Infinite loop which performs the animation etc.
   **/
  public void run () {
	while (running == true) {
		Thread.currentThread().setPriority(Thread.MIN_PRIORITY);

		if (inScroll == false) {
			if (curIndex >= numAds) {
			 	curIndex = 0;
			}
			curAdvert = newAdvert;
			newAdvert = (Advert)adverts.elementAt(curIndex);

                        try {Thread.sleep(pause);} catch (InterruptedException e){}

			curIndex++;
			inScroll = true;
		} else {
			try {Thread.sleep(scrollPause);} catch (InterruptedException e){}
			repaint();
			if (frameIdx >= numFrames) {
				curAdvert = newAdvert;
				inScroll = false;
				frameIdx = 0;
				printMessage();
			} else {
				if ((frameIdx == 0) && (aniAudio != null)) {
					aniAudio.play();
				//	curAdvert.voice.play();
				}
				frameIdx++;
			}
		}
	}
  }

  /**
   * Creates the Thread
   **/
  public void start() {
	if (kicker == null) {
		kicker = new Thread(this);
		kicker.start();
		running = true;
	}
  }

  /**
   * Stop function is called when change page requested (by mouseDown)
   **/
  public void stop() {
	running = false;
	kicker = null;
  }

  /**
   * Do the painting, if we have double buffering use it.
   *
   * @param g   Graphics object to draw to
   **/
  public void paint(Graphics g) {
	if (out != null) {
		// double-buffering available
		adSpacePaint(out);
		g.drawImage(im,0,0, this);
	} else {	
		adSpacePaint(g);
	}
  }

  /**
   * Calls paint to perform the painting
   *
   * @param g   Graphics object to draw to
   **/
  public void update(Graphics g) {
	paint(g);
  }

  /**
   * The off-screen double buffering Graphics
   **/
  Graphics out;

  /**
   * The image which will be linked to the off-screen off-screen Graphics
   **/
  Image im;

  /**
   * Index of current frame in animation scrolling
   **/
  int frameIdx=0;

  /**
   * This is the function which does all the painting work
   *
   * @param g   Graphics object to draw to
   **/
  private void adSpacePaint(Graphics g){

        // g.setColor(Color.black);
        // g.fillRect(0,0,size().width,size().height);

	if (newAdvert == null || curAdvert == null) {
		return;
	}

	Image scaled;
	g.clipRect(0, 0, size().width, size().height);
	if (inScroll == true) {
	
		/* This function is called at the browser's discretion, so must
		 * check the value of frameIdx, make sure it isn't overrunning.
		 */
		if ((newAdvert.image != null) && (frameIdx < numFrames) &&
			(curAdvert.image != null) && (frameIdx < numFrames)) {

			newAdvert.paintFrame(g,0,0,frameIdx,0);
                        curAdvert.paintFrame(g,0,frameIdx*deltaY+1,frameIdx,1);

		} else {
			g.drawImage(newAdvert.image,0,0, this);
		}
	} else {
		g.drawImage(curAdvert.image,0,0, this);
	}
  }

  /**
   * The mouse entering applet method
   **/
  public boolean mouseEnter(java.awt.Event evt, int x, int y) {
	mouseIn = true;
	printMessage();

	return true;
  }

  /**
   * The mouse leaving applet method
   **/
  public boolean mouseExit(java.awt.Event evt, int x, int y) {
	mouseIn = false;
	eraseMessage();

	return true;
  }

  /**
   * The mouse down applet method
   **/
  public boolean mouseDown(java.awt.Event evt, int x, int y) {
	stop();
	getAppletContext().showDocument(curAdvert.link);
	mouseIn = false;

	return true;
  }

  /**
   * The method to print the "Go to: ....." message at the foot of the page
   **/
  private void printMessage() {
	if (mouseIn) {
		if (curAdvert != null)
		{
			if (curAdvert.link != null) {
				getAppletContext().showStatus("Go to " 
					+ curAdvert.link.toExternalForm());
			} else {
				getAppletContext().showStatus("No URL to link to");
			}
		}
	}
  }

  /**
   * Erase the message when the mouse leaves the applet area
   **/
  private void eraseMessage() {
	if (! mouseIn) {
		getAppletContext().showStatus("");
	}
  }

  /**
   * Parse the configuration file creating a new Advert and appending it
   * to the Vector of adverts for each '{' '}' pair found
   *
   * @param u   The string URL of the configuration file
   **/
  private void parse_adlist (String u) {
	// Create the url. Pass this URL in case relative url specified

	URL url = null;
	try {url = new URL (getDocumentBase(),u);}
	catch (java.net.MalformedURLException e) {
		System.out.println ("Can't get adlist " + u);
	}

	Advert advert=null;

	InputStream in = null;
	try {
		in = url.openStream();
	} catch (java.io.IOException e) {
		System.out.println("Didn't find URL: " + url.toExternalForm());
		return;
	}

	StreamTokenizer st = new StreamTokenizer(in);
	st.wordChars(0,255);
	st.eolIsSignificant(false);
	st.commentChar('#');
	st.whitespaceChars(' ',' ');
	st.whitespaceChars('\t','\t');
	st.whitespaceChars('\n','\n');
	st.whitespaceChars('\r','\r');
	st.ordinaryChar('{');
	st.ordinaryChar('}');

	int i=0;
	
	// while (st.nextToken() != StreamTokenizer.TT_EOF) {
	while (true) {
		try {
			if (st.nextToken() == StreamTokenizer.TT_EOF) {
				break;
			}
		} catch (IOException e) {break;}

		if (st.ttype == '{') {
			// System.out.println("In a record");
			advert = new Advert (this);
		} else if ((st.ttype == StreamTokenizer.TT_WORD) && (i==0)) {
                        System.out.println("Got ad URL: " + st.sval);
			advert.addImage(st.sval);
			i++;
		} else if ((st.ttype == StreamTokenizer.TT_WORD) && (i==1)) {
			System.out.println("Got Link: " + st.sval);
			advert.addLink(st.sval);
			i++;
		}else if ((st.ttype == StreamTokenizer.TT_WORD) && (i==2)) {
			System.out.println("Got Audio: " + st.sval);
			advert.addAudio(st.sval);
			i++;
		} else if (st.ttype == '}') {
			// System.out.println("Out of a record");
			if (advert != null) {
				adverts.addElement(advert);
				advert = null;
			}
			i=0;
		}
	}
  }
}


/**
 * Advert Class
 *
 * @author D. Nicol & C. Smeaton
 **/

class Advert {
        
        /**
         * The advertising image
         **/
	public Image image=null;

        /**
         * The URL this advert links to
         **/
	public URL link=null;

        /**
         * The containing applet object
         **/
	adSpace applet=null;

        /**
         * An audio clip to play (if present) when this advert is displayed
         **/
	public AudioClip voice=null;

        /** 
         * A static MediaTracker object to monitor down-load of images, 
         * and check for errors in image down-load
         **/
        static MediaTracker tracker;

        /**
         * Full construction of the object
         **/
	Advert (adSpace a, Image i, String s) {
		applet = a;

		try {link = new URL (applet.getDocumentBase(), s);}
		catch (java.net.MalformedURLException e) {};

		image = i;

                tracker = new MediaTracker(applet);
	}

        /**
         * Constructor with no members (other than Applet owner)
         **/
	Advert (adSpace a) {
		applet = a;
		image = null;
		link = null;

                tracker = new MediaTracker(applet);
	}

        /**
         * Add the image to the Advert. Uses media tracker to wait for loading
         **/
	public void addImage (Image i) {
		image = i;

                tracker.addImage(image,0);
                try {
                        tracker.waitForID(0);
                } catch (InterruptedException e) {
                        System.out.println("**Interrupted while waiting for image**");
                }
	}

        /**
         * Load the image, from the url.
         **/
	public void addImage (String s) {
		System.out.println("Imaghe is " + s);
		Image i = applet.getImage(applet.getDocumentBase(), s);
		addImage (i);
	}

        /**
         * Add the URL to link to
         **/
	public void addLink (String s) {
		try {link = new URL (applet.getDocumentBase(), s);}
		catch (java.net.MalformedURLException e){};
	}

        /**
         * Add an audio file to the Advert
         **/
	public void addAudio (String s) {
		try {voice = applet.getAudioClip(new URL(s));} 
		catch (java.net.MalformedURLException e){};

	}

        /**
         * Paint an animation frame. Frame determined from paramaters
         *
         * @param g     Graphics to draw to
         * @param x     x coordinate of area to draw to
         * @param y     y coordinate of area to draw to
         * @param idx   Index of frame to draw
         * @param type  0 = Shrinking (old advert); 1 = Growing (new advert)
         **/
	public boolean paintFrame (Graphics g, int x, int y, int idx, int type) {
		// Work out which frame we really want
		int frame=0;

		if (type == 0) {
			// Ok frame is idx
			frame = idx;
		} else if (type == 1) {
			// Right, frame is mirror image number
			int centre = applet.numFrames/2;
			int r = centre - idx - 1;
			frame = r + centre;	
		}

		if ((applet != null) && (image != null)) {
			int fh = (int)((double)frame * Math.abs(applet.deltaY) + 1.0f);
                        fh = Math.min (fh, applet.size().height);

			try {
                                g.drawImage (image, x, y, image.getWidth(applet), fh, applet);
			} catch (Exception e) {
				return false;
			}
		} else {
				return false;
		}

		return true;
	}

        /**
         * Simple check to see if everything went ok with creation of this
         * Advert object
         **/
	public boolean isSetup () {
                if (tracker.isErrorAny()) {
                        System.out.println("ERROR IN LOADING IMAGES");
                        return false;
                } else {
                        return true;
                }
	}
}
 