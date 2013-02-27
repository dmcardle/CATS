function [C] = noteElimination(N, D)
%NOTE ELIMINIATION
%   Deletes some of the note candidates in an attempt to find the correct
%   note intended

%N is the array of note energies
%D is the array of note durations

%C is the array of candidates
%E is the array of eliminated notes

%initialize the variables
sum = 0;
i = 1;


%calculate the minAvgNoteEnergy
for j = 1:length(N)
    sum = sum + N(j);
end
minAvgNoteEnergy = sum / length(N);


%eliminate low energy notes
for j=1:length(N)
  if (N(j) < minAvgNoteEnergy)
		E(i) = N(j);
        %note is no longer a candidate
    
	else
		C(i) = N(j); %put the note in the possible candidates 
		i=i+1;
    end
end

        
%calculate the minimum trajectory length
sort(D);
minTrajLen = D(1);

%eliminate short duration notes
for j=1:length(N)
	if D(j) < minTrajLen
		E(end+1) = N(j);
		%eliminate note
	else
		C(end+1) = N(j) ;
		i=i+1;
    end
end


%finds and eliminates harmonics
sort(N); %first sort N into ascending order
for j=1:length(N)
	for i = j+1:length(N)
		if N(j) < N(i)*(.5)
			C(end+1) = N(j);
			E(end+1) = N(j);
			%eliminate higher note
			%keep lower note as candidate
        end
    end
end


end

