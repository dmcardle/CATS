function [ noteName ] = getNoteName( freq )
%GETNOTENAME Gets note name from a given frequency in Hz
%   Given a frequency in Hz, this function determines the note's name in
%   Scientific Pitch Notation.

    C0_FREQ = 16.352;

    NOTE_NAMES = {
        'C'
        'C#'
        'D'
        'D#'
        'E'
        'F'
        'F#'
        'G'
        'G#'
        'A'
        'A#'
        'B'
    };
    
    % number of half steps from note C0
    totalHalfStepsFromC = round(log(freq/C0_FREQ) * 12.0 / log(2));

    % which octave in Scientific Pitch Notation
    octave = floor(totalHalfStepsFromC / 12);
    
    % how many half steps from closest C below note
    halfSteps = mod(totalHalfStepsFromC + 1, 12);
    
    noteName = sprintf('%s%d', NOTE_NAMES{halfSteps}, octave);
    
end

