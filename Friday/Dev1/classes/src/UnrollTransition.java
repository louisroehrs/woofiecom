//##############################################################################
//# FILE: UnrollTransition.java
//# VERSION: 0.99
//# DATE: 1/12/96
//# AUTHOR: Robert Temple (templer@db.erau.edu)
//#
//# Copyright (c) 1996 Robert Temple, All Rights Reserved.
//##############################################################################

import BillBoard.*;
import java.awt.image.MemoryImageSource;
import java.awt.Image;

//##############################################################################
//# CLASS: UnrollTransition
//#
//# The UnrollTransition class changes one image into another by setting a roll
//# which is the new image on top of the old image, and then unrolling the new
//# image until it covers the old image.
//#
//##############################################################################
//# STATIC CONSTANT: FRAMES
//#   The total number of frames this transition will show on the screen before
//#   the new image is shown in its entirety
//# STATIC VARIABLE: fill_pixels
//#   short array of three pixels used to fill in the right hand side of the
//#   roll
//# STATIC VARIABLE: unroll_amount[]
//#   An array which holds the amount of verticle pixels to unroll the
//#   image each frame
//# STATIC METHOD initClass
//#   initialize the unroll_amount array here
//# VARIABLE: location
//#   The index into the work_pixel array that the start of the roll is at
//# CONSTRUCTOR
//#   initialize all of the member variables
//# METHOD: UnrollDown
//#   Create the next frame in the work pixel array
//##############################################################################
public class UnrollTransition extends BillBoard.BillTransition {
  //### STATIC MEMBERS
  final static int FRAMES = 9;
  static int fill_pixels[] = { 0xFFFFFFFF, 0xFF000000, 
                               0xFF000000, 0xFFFFFFFF };

  static int unroll_amount[] = null;

  protected static void initClass() {
    if(unroll_amount != null) {
      return;
    }

    //# The First line of the statement below determines that average 
    //# amount each frame must unroll the image in order to completely
    //# unroll the image during the transition.  Note that we add one
    //# to the FRAMES count because the drawing of the whole next 
    //# image to the screen is part of the unrolling process too.
    //# the second line determines the location the across the x-axis
    //# that this average will fall if the first frame starts at a
    //# x point of 1.  This is why one more is added to FRAMES
    //# then the top.
    //# The divide determines the slope of the line from (0,0) to
    //# (x_avg, y_avg)
    //# if you are confused here, don't worry, so was I...  but
    //# it works...
    float unroll_increment = ((float)image_h / (float)(FRAMES + 1)) /
    			    ((float)(FRAMES + 2) / 2.0f);
    
    int total = 0;
    unroll_amount = new int[FRAMES + 1];
    for(int u = 0; u <= FRAMES; ++u) {
      unroll_amount[u] = (int)(unroll_increment * (FRAMES - u + 1));
      total += unroll_amount[u];
    }
    
    //# make sure we did not round our way to unrolling more of the
    //# image then there is to unroll
    if(total < 0) {
      unroll_amount[0] -= 1;
    }
  }

  //### INSTANCE MEMBERS
  int location;

  public UnrollTransition() {
    super(FRAMES);
    initClass();

    location = pixels_per_image;
    
    System.arraycopy((Object)
              owner.billboards[owner.current_billboard].image_pixels,
              0, (Object)work_pixels, 0, 
              pixels_per_image);

    for(int f = 0; f < number_of_frames; ++f) {

      //# Unroll the Image
      location -= unroll_amount[f] * image_w;

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(150);
      } catch (InterruptedException e) {}

      Unroll(f);

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(100);
      } catch (InterruptedException e) {}

      //# create the new frame image from the work pixels
      frames[f] = owner.createImage(new MemoryImageSource(image_w,
                image_h, work_pixels, 0, image_w));

      owner.prepareImage(frames[f], owner);

      //# copy over the new image onto where the roll last appeared
      System.arraycopy((Object)
              owner.billboards[owner.next_billboard].image_pixels,
              location,
              (Object)work_pixels, location, unroll_amount[f] * image_w);
    }

    //# we don't need the work pixels anymore
    work_pixels = null;
  }

  void Unroll(int f) {
    
    int y_flip = image_w;

    //# the offset is what makes the roll appear to be raised up

    int offset[] = new int[unroll_amount[f]];
    for(int o = 0; o < unroll_amount[f]; ++o) {
      offset[o] = 4;
    }
    offset[0] = 2;

    if(unroll_amount[f] > 1) {
      offset[1] = 3;
    }
    if(unroll_amount[f] > 2) { 
      offset[unroll_amount[f] - 1] = 2;
    }  
    if(unroll_amount[f] > 3) {
      offset[unroll_amount[f] - 2] = 3;
    }

    int offset_index = 0;
    for(int p = location; p < location + unroll_amount[f] * image_w; p += image_w) {

      System.arraycopy((Object)
              owner.billboards[owner.next_billboard].image_pixels,
              p - y_flip + offset[offset_index], (Object)work_pixels,
              p, image_w - offset[offset_index]);

      //# draw in the right side of the roll
      System.arraycopy((Object)fill_pixels, 0, (Object)work_pixels,
              p + image_w - offset[offset_index], offset[offset_index]);
    
      ++offset_index;
  
      y_flip += image_w + image_w;  

    }
  }
}
