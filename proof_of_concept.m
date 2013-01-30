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
% We will treat the spectrogram as an image and use image processing
% techniques to attempt to find the notes being played.

[H,theta,rho] = hough(P);
hPeaks = houghpeaks(H,5,'threshold',ceil(0.3*max(H(:))));
lines = houghlines(P,theta,rho,hPeaks,'FillGap',5,'MinLength',7);

figure,hold on
max_len = 0;
for k = 1:length(lines)
   xy = [lines(k).point1; lines(k).point2];
   plot(xy(:,1),xy(:,2),'LineWidth',2,'Color','green');

   % Plot beginnings and ends of lines
   plot(xy(1,1),xy(1,2),'x','LineWidth',2,'Color','yellow');
   plot(xy(2,1),xy(2,2),'x','LineWidth',2,'Color','red');

   % Determine the endpoints of the longest line segment
   len = norm(lines(k).point1 - lines(k).point2);
   if ( len > max_len)
      max_len = len;
      xy_long = xy;
   end
end

% highlight the longest line segment
plot(xy_long(:,1),xy_long(:,2),'LineWidth',2,'Color','red');


hold off