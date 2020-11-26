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

function elev = ComputeElevation(Position_GS,Position_CHESS)
GS=Position_CHESS-Position_GS;
elev=asind((dot(Position_GS',GS')')./(sqrt(dot(Position_GS',Position_GS')').*sqrt(dot(GS',GS')')));
end



