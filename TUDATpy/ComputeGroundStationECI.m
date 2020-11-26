%% EPFL Spacecraft Team - CHESS Mission Design
% Arnaud Muller & Antoine Clout
% Autumn 2020

clc
clear 
close all
%% Ground Station Coordinates
% S-band
LatS=dms2degrees([47,00,52.3]);   % Degrees
LonS=dms2degrees([8,18,22.1]);   % Degrees
% VHF/UHF
LatU=dms2degrees([47,00,52.1]);   % Degrees
LonU=dms2degrees([8,18,21.6]);   % Degrees
Alt=508; %Meters
%% Initial & Final Dates, Timestep
InitialDate=    datetime(2020,01,01,00,00,00);  % Year Month Day Hours Minutes Seconds
FinalDate=      datetime(2020,12,31,23,59,59);  % Year Month Day Hours Minutes Seconds
Timestep= 1;
TimestepSec=   seconds(Timestep); % Seconds
%% Computations
Dates=(InitialDate:TimestepSec:FinalDate)';
[Year,Month,Day]=ymd(InitialDate);
[Hours,Minutes,Seconds]=hms(InitialDate);
Time=Timestep*(0:(length(Dates)-1));
EarthRotation=7.292115e-5;
Phi=EarthRotation*Time;

GS_llaS=[LatS,LonS,Alt];
GS_llaU=[LatU,LonU,Alt];
GS_ECI_S=zeros(length(Dates),3);
GS_ECI_U=zeros(length(Dates),3);
GS_ECI_S(1,:)=lla2eci(GS_llaS,[Year,Month,Day,Hours,Minutes,Seconds]);
GS_ECI_U(1,:)=lla2eci(GS_llaU,[Year,Month,Day,Hours,Minutes,Seconds]);
for k=2:length(Dates)
    R=[cos(Phi(k)) -sin(Phi(k)) 0;sin(Phi(k)) cos(Phi(k)) 0;0 0 1];
    GS_ECI_S(k,:)=(R*GS_ECI_S(k-1,:)')';    
    GS_ECI_U(k,:)=(R*GS_ECI_U(k-1,:)')';
end
%% Export results
ExportS=table(Dates,GS_ECI_S);
ExportU=table(Dates,GS_ECI_U);
save('2020_GS_ECI_SBand.mat','ExportS')
save('2020_GS_ECI_UHFVHF.mat','ExportU')