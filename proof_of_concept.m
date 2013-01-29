%{
AI Music Project - Proof of Concept
 	
This is a proof of concept for my group' s AI project.  We are going to
attempt to load a WAV file and recognize the individual notes.
%}

%% create a spectrogram
signal = wavread('examples/BakerStreet.wav');
window = 256;
overlap = 128;
fftLength = 1024;
samplingFreq = 44100;

figure, spectrogram(signal, window, overlap, fftLength, samplingFreq, 'yaxis')

%% look for notes