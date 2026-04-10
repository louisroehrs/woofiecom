//##############################################################################
//# FILE: FadeTransition.java
//# VERSION: 1.0
//# DATE: 1/1/96
//# AUTHOR: Robert Temple (templer@db.erau.edu)
//#
//# Copyright (c) 1996 Robert Temple, All Rights Reserved.
//##############################################################################
import BillBoard.*;
import java.awt.Image;
import java.awt.image.MemoryImageSource;

//##############################################################################
//# CLASS: FadeTransition
//#
//# The FadeTransition class changes one image into another by drawing
//# a set of random pixels from the new image onto the old image each frame.
//# the number of pixels draw each frame is the same for each frame.
//#
//# DESIGN NOTE: This class uses a bunch of random number to fill in the pixels
//#   of each frame.  If found Java's random number generator too slow for
//#   this purpose, and wrote a really simple one.  The numbers are not very
//#   random, but it is very fast compared to Sun's.  The numbers generated
//#   are more then random enough for my purposes.  Also the it only generates
//#   numbers between 0-7.  The only numbers we need
//#############################################################################
//# STATIC CONSTANT: FRAMES
//#   The total number of frames this transition will show on the screen before
//#   the new image is shown in its entirety
//# STATIC CONSTANT: TOTAL_FRAMES
//#   FRAMES + 1 
//# STATIC CONSTANT: MULTIPLIER
//#   Used by a very-pseudo random number generator
//# STATIC VARIABLE: random[][]
//#   A multidimensional array that hold indexs into the work pixel array
//#   for every single pixel in the work pixel array.  The first dimension
//#   Holds the pixels for each frame, the other dimension is the pixels
//#   indicies.  
//# STATIC VARIABLE: pixels_per_frame
//#   The number of new pixels drawn into the new image each frame
//# STATIC METHOD: initClass
//#   Called once to initialize the random number array.  Every instance
//#   will use the same random numbers
//# CONSTRUCTOR
//#   initialize all of the member variables
//##############################################################################
public class FadeTransition extends BillBoard.BillTransition {

  //# DONT CHANGES THESE NUMBERS, the random number generator will not
  //# work because it only produces number between 0-7
  static final int FRAMES = 7;
  static final int TOTAL_FRAMES = 8;
  static final int MULTIPLIER = 0x5D1E2F;

  static short random[][] = null;
  static int pixels_per_frame = 0;

  static public void initClass() {

    //# is the class already initialized?
    if(pixels_per_frame > 0) {
      return;
    }
    pixels_per_frame = pixels_per_image / TOTAL_FRAMES;

    random = new short[TOTAL_FRAMES][pixels_per_frame];

    //# every frame will have the same number of new pixels draw into
    //# the image.  No more no less.  So keep track of the number
    //# of random values added to each random frame, so that we don't
    //# try to add too many.  The array below keeps count 
    int random_count[] = new int[TOTAL_FRAMES];
    for(int s = 0; s < TOTAL_FRAMES; ++s) {
      random_count[s] = 0;
    }

    int frame;
    int rounded_pixels_per_image = pixels_per_frame * TOTAL_FRAMES;

    //# inline random number generator starts here
    //# *** read DESIGN NOTES above ***
    int seed = (int)System.currentTimeMillis();

    int denominator = 10;
    while((pixels_per_frame % denominator > 0 ||
            image_h % denominator == 0) && denominator > 1) {
      --denominator;
    }

    int new_randoms_per_frame = pixels_per_frame / denominator;
    int new_randoms = rounded_pixels_per_image / denominator;

    //# create a bunch of random numbers and put them into the
    //# array without checking to see if any particular array
    //# is full.   Do this until it is possible that one filled
    //# up.
    for(int p = 0; p < new_randoms_per_frame; ++p) {
      //# Generate a random number between 0 - 7
      seed *= MULTIPLIER;
      frame = (seed >>> 29);
      random[frame][random_count[frame]++] = (short)p;
    }

    //# might as well as mix up the random number generator a bit more                                       
    seed += 0x5050;
    
    //# give other threads a shot at the CPU
    try {
      Thread.sleep(150);
    } catch (InterruptedException e) {}

    //# generate the rest of the random numbers
    for(int p = new_randoms_per_frame; p < new_randoms; ++p) {
      //# Generate a random number between 0 - 7
      seed *= MULTIPLIER;
      frame = (seed >>> 29);

      //# if the frame this number is supposed to go in is
      //# full, put it in the next frame
      while(random_count[frame] >= new_randoms_per_frame) {
        if(++frame >= TOTAL_FRAMES) {
          frame = 0;
        }
      }
      random[frame][random_count[frame]++] = (short)p;
    }

    //# we only actually filled up the arrays part of the way.
    //# now fill them up the rest of the way using the numbers
    //# we already generated.  Also, we don't need to fill in
    //# the numbers for the last frame, since at the last frame
    //# we know that all the work_pixels would have been filled 
    //# in with pixels from the new image anyways.
    for(int s = 0; s < FRAMES; ++s) {

      for(int ps = new_randoms_per_frame; ps < pixels_per_frame;
                              ps += new_randoms_per_frame) {

        for(int p = 0; p < new_randoms_per_frame; ++p) {

          random[s][ps + p] = (short)(random[s][p] + ps * TOTAL_FRAMES);
        }
      }

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(50);
      } catch (InterruptedException e) {}

    }
  }

  public FadeTransition() {
    super(FRAMES);
    initClass();
  
    //# copy all of the old image into the work pixels
    System.arraycopy((Object)
              owner.billboards[owner.current_billboard].image_pixels, 0,
              (Object)work_pixels, 0, pixels_per_image);

    //# create all the image frames
    for(int f = 0; f < number_of_frames; ++f) {

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(100);
      } catch (InterruptedException e) {}

      //# draw in the pixels that the random array specifies for
      //# this frame from the new image into the work pixels
      for(int p = 0; p < pixels_per_frame; ++p) {
        work_pixels[random[f][p]] =
                  owner.billboards[owner.next_billboard].image_pixels[
                  random[f][p] ];
      }

      //# give other threads a shot at the CPU
      try {
        Thread.sleep(50);
      } catch (InterruptedException e) {}

      //# create the new frame image from the work pixels
      frames[f] = owner.createImage(new MemoryImageSource(image_w,
                image_h, work_pixels, 0, image_w));

      owner.prepareImage(frames[f], owner);

    }

    //# we don't need the work pixels anymore
    work_pixels = null;
  }
}
