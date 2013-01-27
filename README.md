AudioToSheetMusic
=================

The purpose of this project is to generate sheet music from audio.

Goals
-----

1. Take "clean" audio file as input -- generated on computer so all pitches are perfect and there is no background noise. Recognize single notes and output names of those notes.
2. Recognize multiple notes
3. Recognize basic rhythms
4. Recognize complex rhythm
5. Recognize "dirty" audio files, taken from real recordings 


Requirements
------------

NSound library - http://nsound.sourceforge.net/examples/index.html

Note: the installation on OSX 10.8 has a hitch because the /Developer directory has been moved.

To install on OSX 10.8, you must 

1. edit the NSoundConfig\_Mac.py file

2. change lib\_dir variable on line 50 to read
> lib\_dir = "/Applicatiens/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/%s/usr/lib" % ver

3. run python-specific instructions from INSTALL file as you would
