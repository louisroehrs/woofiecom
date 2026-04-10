//##############################################################################
//# FILE: BillTransition.java
//# VERSION: 1.15
//# DATE: 1/31/96
//# AUTHOR: Robert Temple (templer@db.erau.edu)
//#
//# Copyright (c) 1996 Robert Temple, All Rights Reserved.
//##############################################################################

import java.awt.image.MemoryImageSource;
import java.awt.Image;

//##############################################################################
//# CLASS: BillTransition
//#
//# The BillData class is used as a base class for other classes that will
//# create transition images between two BillData image's
//#
//# USAGE NOTE: This class is abstract.  Create subclasses from it.
//##############################################################################
//# STATIC VARIABLE: owner
//#   Used to provide the ImageObserver often needed when dealing with the
//#   images and to create new images from pixel arrays
//# STATIC VARIABLE: pixels_per_image
//#   the total number of pixels that will be in all images
//# STATIC VARIABLE: image_w
//#   the width all images
//# STATIC VARIABLE: image_h
//#   the width all images
//# STATIC METHOD: initClass
//#   method used to initialize this classes static variables.
//#   *** Call this before Using this Class Type ***
//#   PARAMETERS:
//#   DynamicBillBoard parent - the class that will use objects of this class
//#     to create transitions
//# VARIABLE: number_of_frames
//#   the number of frames that will be created by this transition
//# VARIABLE: delay
//#   the time in miiliseconds the owner will delay between each frame
//# VARIABLE: frames[]
//#   the actual images that will be displayed on the screen when the
//#   transition is run.
//# VARIABLE: work_pixels[]
//#   an array of pixels that will be used as a canvas to draw new frames
//# CONSTRUCTOR (int)
//#   initialize all of the member variables
//#   PARAMETERS:
//#     int number_of_frames - value of member variable number_of_frames
//# METHOD: clearFrames
//#   used to clear out memory used by objects of this class
//#   NOTE: it seemed like memory was not being cleaned up fast enough
//#     when setting a variable pointing to objects of this class to null
//#     so call this member before setting to null to clean up the memory
//#     used by the images
//##############################################################################
public abstract class BillTransition {
  //### STATIC MEMBERS
  protected static DynamicBillBoard owner = null;
  protected static int pixels_per_image = 0;
  protected static int image_w = 0;
  protected static int image_h = 0;

  static public void initClass(DynamicBillBoard parent) {
    owner = parent;
    image_w = owner.size().width;
    image_h = owner.size().height;
    pixels_per_image = image_w * image_h;
  }

  //### INSTANCE MEMBERS
  public int number_of_frames;
  public int delay;
  public Image frames[];
  protected int work_pixels[];

  public BillTransition(int number_of_frames) {
    this.number_of_frames = number_of_frames;
    frames = new Image[number_of_frames];
    work_pixels = new int[pixels_per_image];
    delay = 120;
  }

  final public void clearFrames() {
    //# clean up all the resources used by the frames
    for(int i = 0; i < number_of_frames; ++i) {
      frames[i].flush();
    }
    number_of_frames = 0;
  }
}
