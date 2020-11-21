function date = epochToDate(epoch,referenceDate,format)

if nargin < 3
    format = 'yyyy-MM-dd HH:mm:ss';
    if nargin < 2
        referenceDate = '2000-01-01 12:00:00';  % J2000
    end
end

date = datetime(epoch,'ConvertFrom','epochtime','Epoch',referenceDate,'Format',format);

end
