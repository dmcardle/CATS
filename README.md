CATS: Convert Audio to Score
=================

The purpose of this project is to generate sheet music from audio.

Goals
-----

- [x] Take "clean" audio file as input -- generated on computer so all pitches are perfect and there is no background noise. Recognize single notes and output names of those notes.
    - [x] In MATLAB
        ![alt text](https://raw.github.com/crazedgremlin/CATS/master/doc/img/proof_of_concept.png "Spectrogram with Notes Labeled")
    
    - [x] In Python
        ![alt text](https://raw.github.com/crazedgremlin/CATS/master/doc/img/python_implementation.png "Spectrogram with Notes Labeled")
- [x] Recognize multiple notes
    - [x] Harmonic removal algorithm
- [ ] Recognize basic rhythms
- [ ] Recognize complex rhythm
- [ ] Recognize "dirty" audio files, taken from real recordings


Requirements
------------

FAQ
---

- *Where are the examples?* They are not included in the git repository. You have to run generateExamples.py to create them.
