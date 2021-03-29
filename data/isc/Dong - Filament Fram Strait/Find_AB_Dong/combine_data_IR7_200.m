% combine_data.m
% script to put the data into a workable format, write out
% need to run this only once for a given set of data

clear

          % create a cell array with names of input files
          
cfilein = {'IR7_190-195.xlsx','IR7_195-200.xlsx','IR7_200-205.xlsx','IR7_205-210.xlsx'};

ctrapflux = [0.02779795418 0.02779795418 0.02779795418 0.02779795418];       % measured trap flux, g-C m^-2 d^-1

%0.640321 upper carbon flux
%0.263757 lower carbon flux

npts = length(cfilein);              % find out how many files we have
                                      % we can add new files

% allocate memory
nspec = cell(npts,1);                %  number spectrum, #/cm^-4
d_cm  = cell(npts,1);                %  particle diameter, cm
d_mm  = cell(npts,1);                % particle diameter, mm
                                      
          %loop on the data files
for ispec =1 : npts
   ndata = xlsread(cfilein{ispec});
   nspec{ispec} = ndata(:,2);                % number spectrum, #/cm^-4
   d_cm{ispec}  = ndata(:,1);                % particle diamter, cm
   d_mm{ispec} = 10 * d_cm{ispec};
end

save nspecdata cfilein npts ctrapflux nspec d_cm d_mm

   