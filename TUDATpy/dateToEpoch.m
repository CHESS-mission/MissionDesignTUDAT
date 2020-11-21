% function epoch = dateToEpoch(date,referenceDate)
function epoch = dateToEpoch(date)
% if ~isa(date,'datetime')
%     date = datetime(date);
% end

referenceDate = datetime(2000,01,01,12,00,00);

% if nargin < 2
%     referenceDate = '2000-01-01 12:00:00';  % J2000
% elseif ~isa(referenceDate,'datetime')
%     referenceDate = datetime(referenceDate);
% end

epoch = round(86400*(juliandate(date) - juliandate(referenceDate)));

end
