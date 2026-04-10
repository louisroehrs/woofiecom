//##############################################################################
//# FILE: BillData.java
//# VERSION: 1.15
//# DATE: 1/31/96
//# AUTHOR: Robert Temple (templer@db.erau.edu)
//#
//# Copyright (c) 1996 Robert Temple, All Rights Reserved.
//##############################################################################

import java.awt.image.PixelGrabber;
import java.net.URL;
import java.awt.Image;

//##############################################################################
//# CLASS: BillData
//#
//# The BillData class is used to store unique data about individual BillBoards
//#
//# USAGE NOTE: Call initPixels before attempting to use the image_pixels[]
//#   array.
//#
//# DESIGN NOTE: The initialization of the image_pixels is separated from the
//#   constructor to allow the constructor to return in the fastest time
//#   possible.  This is because the PixelGrabber required to initialize the
//#   image pixels waits until _all_ of the pixels have been delivered by the
//#   image's ImageProducer before returning.
//#
//#   Because the DynamicBillBoard class attempts to get an image to the screen
//#   ASAP upon startup, it is essential that the initPixel method is called
//#   after the image is displayed on the screen
//##############################################################################
//# VARIABLE: link
//#   store the URL of the page that this BillBoard will go to
//# VARIABLE: image
//# store the image that this BillBoard will show on the screen
//# VARIABLE: image_pixels
//# store the pixels of the image of this BillBoard.  These pixels are used
//#   by BillTransition classes to create new images that represent transitions
//# between two BillBoards
//# CONSTRUCTOR
//#   initialize the link and image variables
//# NOTE: The image pixel variable is initialized in the initPixels method
//# METHOD: initPixels
//#   method is used to initialize the image_pixels[] variable
//#   PARAMETERS:
//#   int image_width - the width of the image variable
//#     int image_height - the height of the image variable
//#   NOTE: this method could also have the ImageObserver of the image
//#   variable as a parameter.  The width and height could then be
//#   obtained from the image itself.
//##############################################################################
public class BillData {

  public URL link;
  public Image image;
  public int image_pixels[];

  public BillData(URL link, Image image) {
    this.link = link;
    this.image = image;
  }

  public void initPixels(int image_width, int image_height) {

    image_pixels = new int[image_width * image_height];

    //# Create a PixelGrabber to Get the Pixels of the image and store
    //# them into the image_pixels array
    PixelGrabber pixel_grabber = new PixelGrabber(image.getSource(), 0, 0,
              image_width, image_height, image_pixels, 0, image_width);

    try {
      pixel_grabber.grabPixels();
    } catch (InterruptedException e) {
      //# I assume if there was an interrupt, the applet has been aborted
      //# and doesn't need the pixels anymore anyways.
      return;
    }
  }

}
