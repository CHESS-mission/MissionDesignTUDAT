J2=1082.63e-6; %J2 coefficient gravity field of Earth
Rearth=6378.136; %Radius Earth in km
muEarth=398600.441; %Gravitational parameter Earth in km3/s2
EarthRot=2*pi/(365.256363004*86400);
alt=550;
a=Rearth+alt;
V=sqrt(muEarth/a);
e=0;


i=acosd(-(2*EarthRot*a.^(7/2)).*(1-e^2)^2./(3*J2*Rearth^2*sqrt(muEarth)));
