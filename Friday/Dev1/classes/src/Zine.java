/*
 *Zine Zine Zine Zine Zine Zine Zine
 * a demo program.
 * Implements popups for comic book style messages
 * on top of an image. 
 * uses a crummy form of markup language
 * designed only to be easy to parse with java
 * (read quick n dirty)
 *Zine (more...)
  * an app by Johan van der Hoeven.
  * johan@rosebud.com
  * http://www.rosebud.com/rb/rbhome.html
  * johan_van_der_Hoeven@terc.edu
  * 
  * can be viewed at:
  * http://http://www.fanzine.se/java/jo/zine.html (zine stuff)
  * http://teaparty.terc.edu/java/z/glob.html (network science education research)
*/




import java.awt.*;
import java.io.StreamTokenizer;
import java.io.InputStream;
import java.io.FileInputStream;
import java.net.URL;  
import java.util.Vector;
import java.util.Enumeration; 
import java.applet.Applet;

   class Rect
   {
 
   public int lX=0;
   public int tY=0;
   public int rX=0;
   public int bY=0;
   public Rect(int leftX, int topY, int rightX, int bottomY)
        {lX=leftX; tY=topY; rX=rightX; bY=bottomY;}

   public Rect(){};
   public boolean isPointInRect(int x, int y)
	     {
		  if(x<rX&&x>lX&&y>tY&&	y<bY)
		   return true;
		   else
		   return false;

		  }
   public void offset(int dx, int dy)
   		  {
		   lX+=dx;
		   rX+=dx;
			tY+=dy;
			bY+=dy;
		  };
   public int	width()	 { return (rX-lX);};
   public int height()	 { return (bY-tY);};
   } 

 class zineFrame
   {
   public   Point p;
   public	Rect r;
   public	Vector strvec;	
   	/*  add more later...type etc.*/
   
   public zineFrame()
		 { r = new Rect(); strvec = new Vector(); p =new Point(0,0);
		 };
   
   }  
  
  /* you may wonder why there is a clipR when it is the same as textR*/
  /* this is so that when the popup gets better looking the texrR */
  /* will be a part of it */    
 class zinePopUp
  {
   public Point p;   /* anchor */
   public Rect clipR; /* area it covers */
   public Rect textR; /*area for text*/
   public zineFrame xfrm=null;
   public Font font;
   public FontMetrics fm;
   public int lineHi, charWid;
   

   public zinePopUp	(Font f) {
                p= new Point(0,0); clipR = new Rect(); textR= new Rect();
                 //font = new java.awt.Font("TimesRoman", Font.PLAIN, 12);
				 font = f;
				 charWid= 12;// font.stringWidth(" ");
				 lineHi=  12;// font.height+2;
                };
   public boolean doLayout(Rect boundR, zineFrame zf)
          {
		   
		   xfrm=zf;
		   int wid=0;
		   int hi=0;
		    
		   for (Enumeration e = xfrm.strvec.elements(); e.hasMoreElements();)
				    {
				    	hi+=lineHi;

				    	String tmp=	(String) e.nextElement();

				    	 wid= Math.max(wid, 120 /* font.stringWidth(tmp) */);
				    
					
				    }; 
			wid+=2*charWid;
		   textR.bY=xfrm.p.y;
		   textR.lX=xfrm.p.x;
		   textR.rX=textR.lX+wid;
		   textR.tY=textR.bY-hi-lineHi/2;
		   	doRectMunge(boundR);
		   clipR=textR;

		  return true;
		  };
   protected void doRectMunge(Rect boundR)
          {
		  int xa=xfrm.p.x-boundR.lX;
		  int xb=boundR.rX-xfrm.p.x;
		  int ya=xfrm.p.y-boundR.tY;
		  int yb=boundR.bY-xfrm.p.y;

		  /* check if it fit, if not try moving it. */
		
			if(textR.rX>boundR.rX)
			   {  
				   //do a horizontal left shift
				   	int tmp= Math.min(textR.width(),xa);
				   textR.offset(-tmp,0);
			   }
			   else
			 if(textR.lX<boundR.lX)
			   {
				  //do a horizontal right shift
				   int tmp= Math.min(textR.width(),xb);
				   textR.offset(tmp,0);
			   }
			 /* vertical : (Has bugs! --OK for now....)*/
			   if(textR.tY<boundR.tY)
			   {
				   //do a vertical down shift
				    int tmp= Math.min(textR.height(),ya);
				    textR.offset(0,tmp);
			   }
			   else
			   if(textR.bY>boundR.bY)
			   {
			
				   //do a vertical down shift
				    int tmp= Math.min(textR.height(),yb);
				   textR.offset(0,-tmp);
			   }

		  };
    
   public void Draw(Graphics g)
          {

		   FontMetrics fm;

		   g.setFont(font);
		   g.setColor(Color.lightGray);
		   g.fill3DRect(textR.lX, textR.tY, textR.width(), textR.height(),true);
		   g.setColor(Color.black);
		   	int y=textR.tY;

		   fm = g.getFontMetrics(font);
		   charWid=fm.stringWidth(" ");
		   lineHi=fm.getHeight() + 2;

		   for (Enumeration e = xfrm.strvec.elements(); e.hasMoreElements();)
				    {
				    	y+=lineHi;
						g.drawString((String) e.nextElement() , textR.lX+charWid, y);
				   
				    }; 

		  };
  
  } 
   public class Zine extends Applet {
        
		protected String dana = null;
		protected String imgna = null;
		protected String shot=null;
		protected Image  daimg;
		Rect clipR;
		Vector framevect;
		boolean showhot=false;
	
		zineFrame cur_znfrm=null;
		zinePopUp pop=null;
		Font font;
        public void init() {
							font = new java.awt.Font("TimesRoman", Font.PLAIN, 12);
							framevect= new Vector(); 
	    					resize(200, 200);
							dana = getParameter("dataurl");
							getFrames();

							imgna = getParameter("imgurl");
							daimg= getImage(getCodeBase(), imgna);
							if(daimg!=null)
							 resize(daimg.getWidth(this),daimg.getHeight(this));
							else
							 resize(10, 10);
							 shot = getParameter("showhot");

							 if(shot!=null)
							 if(shot.equals("yes"))
							   	 showhot=true;
        					}
	
     		 public void paint(Graphics g) {
				 FontMetrics fm;
	
	    			
	    		 
				 g.drawImage(daimg, 0, 0, this);	

				 // fm = g.getFontMetrics(font);
				 // charWid=fm.stringWidth(" ");
				 // lineHi=fm.getHeight() +2;
	             				
				/*
					System.out.println("Zine Paint");
					System.out.println(zfrm);
					System.out.println(zfrm.p);
					System.out.println(zfrm.r);
					System.out.println(zfrm.strvec);
					System.out.println(framevect);
					*/
				
					
			
				if(showhot)
				for ( Enumeration ee = framevect.elements(); ee.hasMoreElements();)
				{
				   zineFrame fr= (zineFrame)ee.nextElement();
				 
				  g.draw3DRect(fr.r.lX, fr.r.tY, fr.r.width(), fr.r.height(),true);
				
				};
		
			if(pop!=null)
			   pop.Draw(g);	
			g.draw3DRect(0, 0, size().width, size().height,true);

      	}   
   		/* end paint */

	 public void update(Graphics g) {
	       // Clip to the affected area
		   	//make sure not outside applet: 
			//(needed else it can paint outside applet --java bug ?)
			int x=	Math.max(0,clipR.lX);
			int y=  Math.max(0,clipR.tY);
			int w= Math.min(size().width,clipR.width());
			int h= Math.min(size().height,clipR.height());
	g.clipRect(clipR.lX, clipR.tY, clipR.width(), clipR.height());
	          paint(g);
               }
	public boolean keyDown(java.awt.Event evt, int k)
	            {
				System.out.println("key");
				 
				   if(k=='s'||k=='S')
				   {
				      showhot=!showhot;
				      clipR.lX=0;
				      clipR.rX=size().width;
				      clipR.tY=0;
				      clipR.bY=size().height;
				      repaint();
				   }
			    return true;
				}
	public boolean mouseEnter(java.awt.Event evt)
	             { requestFocus();
				   return true;
				 }

	public boolean mouseExit(java.awt.Event evt)
	             { 
	             	 if(pop!=null)
					 {
					  cur_znfrm=null;
					  clipR=pop.clipR;
					  pop=null;
				      repaint();
					  };
				   return true;
	             }
	public boolean mouseMove(java.awt.Event evt, int x, int y)
	            {
					
				boolean change=false;
				  if(cur_znfrm==null)
				  {
   	   	 		 for ( Enumeration ee = framevect.elements(); ee.hasMoreElements();)
					{
				     zineFrame fr= (zineFrame)ee.nextElement();
				     if(fr.r.isPointInRect(x,y))
				        { change=true;
				          cur_znfrm=fr;
				          pop = new zinePopUp(font);
						  Rect r=new Rect(0,0,size().width,size().height);
						  pop.doLayout(r,cur_znfrm);
						  clipR=pop.clipR;
				          };
					};
						
				  }
				   else
				   {
				  if(!cur_znfrm.r.isPointInRect(x,y))
					 { 
					 cur_znfrm=null;
					 clipR=pop.clipR;
					 pop=null;
					  change=true;
					 };
					};
				 	

				 if(change)
				    {

				    repaint();


					};
				  return true;
                }  
     
     
     
     
       protected void getFrames()
		        {
				           	zineFrame zfrm=null;
							//System.out.println("zine get frames");
		 				
							InputStream is=null;

							try {
							  is = new URL(getDocumentBase(), dana).openStream();
							} 
							catch (Exception e){
							  System.out.println("error processing: ");
							  e.printStackTrace();
							  return;
							}
							 
							 StreamTokenizer st = new StreamTokenizer(is);
								st.eolIsSignificant(false);
								st.commentChar('#');
								
							 	
							 	
							 	/* parse file --NOT very clean can be improved alot */    
							   int i=0;
							  while (st.ttype != StreamTokenizer.TT_EOF)
			                        {
									try {
			                          st.nextToken();
									}
									catch (Exception e){
									  System.out.println("error processing: ");
									  e.printStackTrace();
									  break;
									}

								    
									   	/* got a new frame: */
									if(st.ttype == '{')
									  { 
									 
									  zfrm= new zineFrame(); 
									   	i=0;
										continue;
									   };
									 
									 if(st.ttype == '}')
									   {framevect.addElement(zfrm);
										 continue;
									   }

									 if(st.ttype==st.TT_NUMBER)
									   {
									   	 int  n = (int) st.nval;
										switch (i)
										  	{
											case 0:
											 zfrm.p.x=n;
											break;
											case 1:
											 zfrm.p.y=n;
											break;
											case 2:
											 zfrm.r.lX=n;
											break;
											case 3:
											 zfrm.r.tY=n;
											break;
											case 4:
											 zfrm.r.rX=n;
											break;
											case 5:
											 zfrm.r.bY=n;
											break;

									 
											};	 

											i++;
											continue;
									   };

									   if(st.ttype=='"')
									   { String tmp= st.sval;
									    zfrm.strvec.addElement(tmp);
										continue;
										};

									};	/* while */

				};	 /* end getFrames()	*/


     }   /* end zine class */ 
   
