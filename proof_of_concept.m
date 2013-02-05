%{
AI Music Project - Proof of Concept
 	
This is a proof of concept for my group' s AI project.  We are going to
attempt to load a WAV file and recognize the individual notes.
%}



%% create a spectrogram
signal = wavread('examples/bakerStreet.wav');
window = 512;
overlap = 128;
fftLength = 1024;
samplingFreq = 44100;

% create a new figure
figure

% compute the spectrogram
[S,F,T,P] = spectrogram(signal, window, overlap, fftLength, samplingFreq, 'yaxis');

P = 10*log10(P);

% view the spectrogram 
surf(T,F,P,'edgecolor','none');
axis tight; 
view(0,90);
xlabel('Time (Seconds)'); ylabel('Hz');

%% look for notes


%for spectrum = S
spectrum = S(:, 10);

    % spectrum for this time slice
    s = abs(spectrum);
    
    [peakVals, peakLocs] = findPeaks(s, 'MINPEAKHEIGHT', 0.20);
    

    figure
    hold on

    plot( s )
    
    for i = 1:numel(peakLocs)
        thisPeakLoc = peakLocs(i);
        thisPeakVal = peakVals(i);
        
        thisPeakFreq = F(thisPeakLoc);
        
        fprintf( 'peak at %d\n', thisPeakLoc)
        rectangle( 'Position', [thisPeakLoc thisPeakVal 10 0.01 ])
        text(thisPeakLoc, thisPeakVal, getNoteName(thisPeakFreq));
    end

    hold off
%end


hold off