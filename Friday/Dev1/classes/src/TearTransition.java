//##############################################################################
//# FILE: TearTransition.java
//# VERSION: 1.0
//# DATE: 1/1/96
//# AUTHOR: Robert Temple (templer@db.erau.edu)
//#
//# Copyright (c) 1996 Robert Temple, All Rights Reserved.
//##############################################################################

import BillBoard.*;
import java.awt.image.MemoryImageSource;
import java.awt.Image;

//##############################################################################
//# CLASS: TearTransition
//#
//# The TearTransition class changes one image into another by making it appear
//# as if the old image is covering the new image, and the old image is torn
//# out from over the new image.
//#
//##############################################################################
//# STATIC CONSTANT: FRAMES
//#   The total number of frames this transition will show on the screen before
//#   the new image is shown in its entirety
//# STATIC CONSTANT: INITIAL_X_CROSS
//#   The number to start the x_cross variable at
//# STATIC CONSTANT: X_CROSS_DIVISOR
//#   The amount the x_cross number is divided by after each frame
//# VARIABLE: x_cross
//#   A number the cross product of the x and y values of a pixel are
//#   multiplied by to give a new x value
//# CONSTRUCTOR
//#   initialize all of the member variables
//# METHOD: Tear
//#   Create the next frame in the work pixel array
//##############################################################################
public class TearTransition extends BillBoard.BillTransition {
  static final int FRAMES = 7;
  static final float INITIAL_X_CROSS = 1.6f;
  static final float X_CROSS_DIVISOR = 3.5f;

  float x_cross;

  public TearTransition() {
    super(FRAMES);

    //# The first row of the all the transition images will always be from the
    //# old image.  So copy the first row into the work pixels now, and forget
    //# we can skip them the rest of the way.
    System.arraycopy((Object)
              owner.billboards[owner.current_billboard].image_pixels, 0,
              (Object)work_pixels, 0, image_w);

    //# Starting after the first row, Copy the new image into the work pixels
    System.arraycopy((Object)
              owner.billboards[owner.next_billboard].image_pixels,
              image_w, (Object)work_pixels, image_w,
              pixels_per_image - image_w);

    x_cross = INITIAL_X_CROSS;

    //# Create all the image frames, starting with the last frame.  Since each
    //# frame progressively covers more and more of the old image, we start
    //# from the last frame to reduce the amount of drawing we need to do from
    //# frame to frame.   This is because the last frame covers the least 
    //# amount of the old image.  So, after drawing the last frame, we can draw 
    //# right over the work pixels, since we know that we will be covering all 
    //# that the later frame (the one we had previouly drawn) drew onto the
    //# work pixels anyways.  So now we can just draw the pixels of the new
    //# image, and don't have to worry about drawing pixels from the old image.
    //# email me if this is not clear.  templer@db.erau.edu
    for(int i = number_of_frames - 1; i >= 0; --i) {

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(100);
      } catch (InterruptedException e) {}
                                                                      
      //# draw the next frame into the work pixels
      Tear();

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(150);
      } catch (InterruptedException e) {}

       //# create the new frame image from the work pixels
      frames[i] = owner.createImage(new MemoryImageSource(image_w,
                image_h, work_pixels, 0, image_w));

      owner.prepareImage(frames[i], owner);

      //# set the x_cross for the next frame
      x_cross /= X_CROSS_DIVISOR;
    }

    //# we don't need the work pixels anymore
    work_pixels = null;
  }

  public void Tear() {
    float h_multi;
    int p, height_adder;

    //# p represent the current offset into the work pixels that we are
    //# drawing at
    p = height_adder = image_w;

    //# starting after the first row, draw all the rows, individually into the
    //# work pixels
    for (int y = 1; y < image_h; ++y) {

      //# the cross product will equal x_cross * x * y.  Since we are gonna
      //# have the same x_cross and y values for this row, calculate it
      //# x_cross * y  once for this row, so we don't have to do it for each
      //# pixel in this row.  For each pixel we will multiply this value by x
      h_multi = x_cross * y;

      //# This if-else structure is a speed optimization.  The first block
      //# draws the pixels, pixel by pixel.  The else block draws the pixels
      //# by copying sequences of pixels onto the work pixels.
      //###
      //# A value of h_multi over 0.50 means that there will never be two 
      //# adjacent pixels from the old image that will be copied onto the work
      //# pixels
      if(h_multi >= 0.50f) {
        float fx = 0.0f;

        //# Adding x to a running sum of h_multi each time is the
        //# equivalent of multiplying x * h_multi
        //####
        //# NOTE 1/6/96: 
        //# Hmm, shouldn't I have started at 0?  Well I know it works...
        h_multi += 1.0f;
        int x = 0;

        //# draw in the pixels for this row until the end of the row is
        //# reached
        do {
          work_pixels[p++] = owner.billboards[owner.current_billboard
                    ].image_pixels[height_adder + x];

          //# Adding x to a running sum of h_multi each time is the
          //# equivalent of multiplying x * h_multi
          x = (int)(fx += h_multi);
        } while(x < image_w);
      }
      else {

        float overflow = 1.0f / h_multi;
        float dst_end = overflow / 2.0f  + 1.49999999f;
        int dst_start = 0, src_offset = 0, length = (int)dst_end;

        while(dst_start + src_offset + length < image_w) {

          System.arraycopy((Object)owner.billboards[owner.current_billboard].image_pixels,
                    p + src_offset, (Object)work_pixels, p, length);

          ++src_offset;
          dst_end += overflow;
          p += length;
          dst_start += length;
          length = (int)dst_end - dst_start;
        }

        length = image_w - src_offset - dst_start;

        System.arraycopy((Object)owner.billboards[owner.current_billboard].image_pixels,
                  p + src_offset, (Object)work_pixels, p, length);

      }
      p = height_adder += image_w;
    }
  }
}
