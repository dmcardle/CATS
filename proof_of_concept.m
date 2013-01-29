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

% create a new figure
figure

% compute the spectrogram
[S,F,T,P] = spectrogram(signal, window, overlap, fftLength, samplingFreq, 'yaxis');

% view the spectrogram 
surf(T,F,10*log10(P),'edgecolor','none'); axis tight; 
view(0,90);
xlabel('Time (Seconds)'); ylabel('Hz');

%% look for notes

