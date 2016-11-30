# Subjective Assesment Video Player

This Subsective Assesment Video Player used to create the INRS Audiovisual Quality Dataset [1]

Files:

PrepareFileList.py: This sscript list the files in a given directory, shuffle the list and then save the list to file system. This is used to make sure every observer rates the audiovisual file randomly but with the same order.

VideoPlayer.py: This script is based on the VLC Python bindings example and modified as needed.

vlc.py: This is the original VLC Python binding. There might be a newer version at from https://wiki.videolan.org/python_bindings.

This player is used in [1, 2] and the technical implementation is explained in [3].

[1] Demirbilek, Edip, and Jean-Charles Grégoire. “The INRS Audiovisual Quality Dataset."  2016 ACM Multimedia Conference.

[2] Edip Demirbilek and Jean-Charles Grégoire. Towards reduced reference parametric models for estimating audiovisual quality in multimedia services. IEEE International Conference on Communications (ICC), 2016, IEEE.

[3] Edip Demirbilek and Jean-Charles Grégoire. Multimedia communication quality assessment testbeds. arXiv preprint arXiv:1609.06612, (2016).
