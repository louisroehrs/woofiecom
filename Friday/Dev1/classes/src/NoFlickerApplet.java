import java.awt.*;
import java.awt.image.ColorModel;
import java.net.URL;
import java.net.MalformedURLException;
import java.applet.Applet;
 
/**
 *
 *  Extension to base applet class to avoid display flicker
 *
 * @version             1.0, 27 Oct 1995
 * @author Matthew Gray
 */
 
public class NoFlickerApplet extends Applet {
  private Image offScreenImage;
  private Graphics offScreenGraphics;
  private Dimension offScreenSize;
  
  public final synchronized void update (Graphics theG)
    {
      Dimension d = size();
      if((offScreenImage == null) || (d.width != offScreenSize.width) ||
         (d.height != offScreenSize.height)) 
        {
          offScreenImage = createImage(d.width, d.height);
          offScreenSize = d;
          offScreenGraphics = offScreenImage.getGraphics();
          offScreenGraphics.setFont(getFont());
        }
      offScreenGraphics.fillRect(0,0,d.width, d.height);
      paint(offScreenGraphics);
      theG.drawImage(offScreenImage, 0, 0, null);
    }
}
