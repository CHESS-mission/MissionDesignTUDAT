%% EPFL Spacecraft Team - CHESS Mission Design
% Arnaud Muller & Antoine Clout
% Autumn 2020
%% Function description
% This function computes and returns the elevation in degrees of a satellite as seen from a ground
% station using ECI coordinates of both.

% The inputs are n*3 double arrays of identical dimensions.
%% Test values
% PosGS=[0 0 1;0 0 1;0 0 1;0 0 1];
% PosSat=[0 0 2;1 1 1;1 1 2;-1 -1 -2];

function [elev] = ComputeElevation(GS_position,Position_CHESS)

% Epochs_CHESS_10 = CHESS_State(:,1); % Array with every 10s epochs
% Epochs_CHESS_1 = (Epochs_CHESS_10(1):1:Epochs_CHESS_10(end))'; % Array with every 1s epochs
% 
% x_CHESS_10 = CHESS_State(:,2); % Position every 10s
% y_CHESS_10 = CHESS_State(:,3); % Position every 10s
% z_CHESS_10 = CHESS_State(:,4); % Position every 10s
% 
% 
% x_CHESS_1 = interp1(Epochs_CHESS_10, x_CHESS_10, Epochs_CHESS_1); % Position every second
% y_CHESS_1 = interp1(Epochs_CHESS_10, y_CHESS_10, Epochs_CHESS_1); % Position every second
% z_CHESS_1 = interp1(Epochs_CHESS_10, z_CHESS_10, Epochs_CHESS_1); % Position every second


PosGS = GS_position;
% Position_CHESS = [x_CHESS_1,y_CHESS_1,z_CHESS_1];

GS=Position_CHESS-PosGS;
elev=asind((dot(PosGS',GS')')./(sqrt(dot(PosGS',PosGS')').*sqrt(dot(GS',GS')')));

end



