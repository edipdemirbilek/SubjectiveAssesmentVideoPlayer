# Subjective Assesment Video Player

This Subsective Assesment Video Player used to create the INRS Audiovisual Quality Dataset [1]

Files:

PrepareFileList.py: This sscript list the files in a given directory, shuffle the list and then save the list to file system. This is used to make sure every observer rates the audiovisual file randomly but with the same order.

VideoPlayer.py: This script is based on the VLC Python bindings example and modified as needed.

vlc.py: This is the original VLC Python binding. There might be a newer version at from https://wiki.videolan.org/python_bindings.

[1] Demirbilek, Edip, and Jean-Charles Grégoire. “The INRS Audiovisual Quality Dataset."  2016 ACM Multimedia Conference (accepted).
