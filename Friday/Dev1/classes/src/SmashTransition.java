//##############################################################################
//# FILE: SmashTransition.java
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
//# CLASS: SmashTransition
//#
//# The SmashTransition class changes one image into another by dropping the
//# new image onto the old one.  The old image appears to crumble under the
//# weight of the new image.
//#
//# USAGE NOTE:
//##############################################################################
//# STATIC CONSTANT: FRAMES
//#   The total number of frames this transition will show on the screen before
//#   the new image is shown in its entirety
//# STATIC CONSTANT: FOLDS
//#   The old image will appear to be folded back and forth under the weigth
//#   of the new image falling on it.  This constant holds the value of the
//#   number of folds that will appear each frame
//# STATIC VARIABLE: fill_pixels
//#   an array of white pixels used to fill in pixels where neither image will
//#   appear in for a frame
//# STATIC METHOD: initClass
//#   Called once to initialize the fill_pixelsr array.
//# VARIABLE: drop_amount
//#   The amount of pixels to move the new image onto the old image each frame
//# VARIABLE: location
//#   The index into the work_pixel array that the start of the old image
//#   current is at
//# CONSTRUCTOR
//#   initialize all of the member variables
//# METHOD: Smash
//#   Create the next frame in the work pixel array
//##############################################################################
public class SmashTransition extends BillBoard.BillTransition {
  //### STATIC MEMBERS
  final static int FRAMES = 8;
  final static float FOLDS = 8.0f;
  static int fill_pixels[] = null;

  public static void initClass() {
    if(fill_pixels != null) {
      return;
    }
    fill_pixels = new int[image_w];
    for(int f = 0; f < image_w; ++f) {
      fill_pixels[f] = 0xFFFFFFFF;
    }
  }

  //### INSTANCE MEMBERS
  int drop_amount;
  int location;

  public SmashTransition() {
    super(FRAMES);
    initClass();

    drop_amount =  (image_h / number_of_frames) * image_w;

    location = pixels_per_image - ((image_h / number_of_frames) / 2) * image_w;

    for(int f = number_of_frames - 1; f >= 0; --f) {

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(100);
      } catch (InterruptedException e) {}

      Smash(f + 1);

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(150);
      } catch (InterruptedException e) {}

      //# create the new frame image from the work pixels
      frames[f] = owner.createImage(new MemoryImageSource(image_w,
                image_h, work_pixels, 0, image_w));

      owner.prepareImage(frames[f], owner);

      location -= drop_amount;
    }

    //# we don't need the work pixels anymore
    work_pixels = null;
  }

  void Smash(int max_fold) {
    System.arraycopy((Object)
              owner.billboards[owner.next_billboard].image_pixels,
              pixels_per_image - location,
              (Object)work_pixels, 0, location);

    int height = image_h - location / image_w;

    float fold_offset_adder = (float)max_fold * FOLDS / (float)height;
    float fold_offset = 0.0f;
    int fold_width = image_w - max_fold;

    float src_y_adder = (float)image_h / (float)height;
    float src_y_offset = image_h - src_y_adder / 2;

    for(int p = pixels_per_image - image_w; p >= location; p -= image_w) {

      System.arraycopy((Object)fill_pixels, 0, (Object)work_pixels, p,
              image_w);

      System.arraycopy((Object)
              owner.billboards[owner.current_billboard].image_pixels,
              (int)src_y_offset * image_w, (Object)work_pixels,
              p + (int)fold_offset, fold_width);

      src_y_offset -= src_y_adder;
      fold_offset += fold_offset_adder;

      if(fold_offset < 0.0 || fold_offset >= max_fold) {
        fold_offset_adder *= -1.0f;
      }
    }
  }
}
