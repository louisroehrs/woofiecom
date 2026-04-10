//#############################################################################
//# FILE: ColumnTransition.java
//# VERSION: 1.0
//# DATE: 1/2/96
//# AUTHOR: Robert Temple (templer@db.erau.edu)
//#
//# Copyright (c) 1996 Robert Temple, All Rights Reserved.
//#############################################################################

import BillBoard.*;
import java.awt.image.MemoryImageSource;
import java.awt.Image;

//#############################################################################
//# CLASS: ColumnTransition
//#
//# The ColumnTransition class changes one image into another by drawing
//# increasingly larger columns of the new image onto the old image.  The
//# column sizes increases to the left, and the same pixels are always drawn
//# on the left side of each column.  This makes the image appear to be sliding
//# in from behind the old image.
//#
//#############################################################################
//# STATIC CONSTANT: FRAMES
//#   The total number of frames this transition will show on the screen before
//#   the new image is shown in its entirety
//# STATIC CONSTANT: MAX_COLUMN_WIDTH
//#   The maximum pixel size a column can grow to be.  This determines how many
//#   columns there will be, the width divided by this number.
//# STATIC CONSTANT: WIDTH_INCREMENT
//#   The pixel amount a column show grow every frame
//# VARIABLE: last_max_columns_width
//#   The width of the last column, because the width of the last column will
//#   usually not be the same size as the MAX_COLUMN_WIDTH, unless the width
//#   of the image is evenly divisible by the MAX_COLUMNS_WIDTH
//# VARIABLE: last_columns_start
//#   starting from the left hand side of the image, the pixel that the last
//#   column will start at.
//# VARIABLE: column_width
//#   the current size of the columns in pixels, the number of pixels to
//#   draw from the new images onto the old one in this column
//# CONSTRUCTOR
//#   initialize all instance variables
//# METHOD NextFrame
//#   Create the next frame in the work pixel array
//#############################################################################
public class ColumnTransition extends BillBoard.BillTransition {
  //### STATIC MEMBERS
  final static int FRAMES = 7;
  final static int WIDTH_INCREMENT = 3;   
  final static int MAX_COLUMN_WIDTH = 24; //# this number should be evenly 
                                          //# divisible by the WIDTH_INCREMENT

  //### INSTANCE MEMBERS
  int last_max_columns_width;
  int last_columns_start;
  int column_width = WIDTH_INCREMENT;

  public ColumnTransition() {
    super(FRAMES);

    //# make it run a little slower then the other ones so the viewer
    //# can see the image slide in from under the other one
    delay = 200;

    last_max_columns_width = image_w % MAX_COLUMN_WIDTH;
    last_columns_start = image_w - last_max_columns_width;

    //# copy the whole of the old image into the work pixel array.
    System.arraycopy((Object)
              owner.billboards[owner.current_billboard].image_pixels,
              0, (Object)work_pixels, 0, pixels_per_image);

    //# create all the image frames
    for(int f = 0; f < number_of_frames; ++f) {

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(100);
      } catch (InterruptedException e) {}

      //# draw the next frame into the work pixels
      NextFrame();

      //# give other threads some more processor time.  How generous of us
      try {
        Thread.sleep(150);
      } catch (InterruptedException e) {}

      //# create the new frame image from the work pixels
      frames[f] = owner.createImage(new MemoryImageSource(image_w, 
                image_h, work_pixels, 0, image_w));

      owner.prepareImage(frames[f], owner);

      //# make the column width wider for the next frame
      column_width += WIDTH_INCREMENT;
    }

    //# we don't need the work pixels anymore
    work_pixels = null;
  }

  void NextFrame() {    

    int old_column_width = MAX_COLUMN_WIDTH - column_width;

    //# iterate through each row of the image
    for(int p = pixels_per_image - image_w; p >= 0; p -= image_w) {

      //# iterate through each column of the image, except the last
      for (int x = 0; x < last_columns_start; x += MAX_COLUMN_WIDTH) {

          //# copy one row of a column of the new pixels into the work
          //# pixels
          System.arraycopy((Object)
                    owner.billboards[owner.next_billboard].image_pixels,
                    x + p, (Object)work_pixels, old_column_width + x + p, 
                    column_width);
      }

      //# now do the last column if we need to
      if(old_column_width <= last_max_columns_width) {
        System.arraycopy((Object)
                    owner.billboards[owner.next_billboard].image_pixels,
                    last_columns_start + p, (Object)work_pixels, 
                    last_columns_start + old_column_width + p - 1, 
                    last_max_columns_width - old_column_width + 1);
      }
    }
  }

}
