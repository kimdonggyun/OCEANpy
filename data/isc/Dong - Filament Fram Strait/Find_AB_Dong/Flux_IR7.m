clear variables
cfile = mfilename;


name = 'IR7_ParticleSizeSpectra.xlsx';
ndata = xlsread(name);                   % reads d and n from excell file
d_mu = ndata(:,1);                                 % puts column d from excell into vector d in matlab
n = ndata(:,2);                                 % puts column n from excell into vector n in matlab
d_mm =  d_mu / 1000;                        % diameter in mm
d_cm =  d_mu / 10000;                        % diameter in mm

name2 = 'IR7_Depth.xlsx';
ndata2 = xlsread(name2);                   % reads d and n from excell file
depth = ndata2(:,1);                                 % puts column d from excell into vector d in matlab

d_temp = [0; d_cm(1:14)];
diamid = d_cm - d_temp;

fact_MW_100 = 1.1258e-010 .* d_mm .^-2.22;     % 100 m - integration factor g_POC m/agg/d
fact_MW_200 = 3.8835e-009 .* d_mm .^-1.1885;     % 200 m - integration factor g_POC m/agg/d
fact_MW_400 = 1.6304e-006 .* d_mm .^0.1927;     % 400 m - integration factor g_POC m/agg/d
fact_MW_All = 1.4571e-006 .* d_mm .^0.1709;     % All - integration factor g_POC m/agg/d
 
ndeps = length(ndata);
for idep =2:ndeps
    nspec(:,idep)  = ndata(:,idep);            % num spec
    temp  = nspec(:,idep) .* fact_MW_All .* 1e6 ;     % nspec to #/m^3/cm, mult fact
    temp(isnan(temp)) = 0;
    flux_m_All(idep)  = trapz(d_cm,temp);           % integ to get flux, g dwt/m^2/d
end

flux_All = flux_m_All(2:end)';

for idep =2:102
    nspec(:,idep)  = ndata(:,idep);            % num spec
    temp  = nspec(:,idep) .* fact_MW_100 .* 1e6 ;     % nspec to #/m^3/cm, mult fact
    temp(isnan(temp)) = 0;
    flux_m_100(idep)  = trapz(d_cm,temp);           % integ to get flux, g dwt/m^2/d
end
flux_100 = flux_m_100(2:end)';

for idep =103:161
    nspec(:,idep)  = ndata(:,idep);            % num spec
    temp  = nspec(:,idep) .* fact_MW_200 .* 1e6 ;     % nspec to #/m^3/cm, mult fact
    temp(isnan(temp)) = 0;
    flux_m_200(idep)  = trapz(d_cm,temp);           % integ to get flux, g dwt/m^2/d
end
flux_200 = flux_m_200';

for idep =162:294
    nspec(:,idep)  = ndata(:,idep);            % num spec
    temp  = nspec(:,idep) .* fact_MW_400 .* 1e6 ;     % nspec to #/m^3/cm, mult fact
    temp(isnan(temp)) = 0;
    flux_m_400(idep)  = trapz(d_cm,temp);           % integ to get flux, g dwt/m^2/d
end
flux_400 = flux_m_400';
flux = [flux_100; flux_200(103:161); flux_400(162:294)];

depbin = ceil((depth+eps)/5);        % calculate index
  for iz = 1:max(depbin)
    ran = iz==depbin;                     %  find the ones I want
    depave(iz)=mean(depth(ran));
    fluxave(iz)=mean(flux_All(ran));
    nspecave(:,iz) = mean(nspec(:,ran),2);
  end          
%%

figure(1)
clf

%hp1 =zeros(ncases,1);
%for icase=1:ncases
  hp1=loglog(fluxave,depave);
  hold on
%end

hold off;  
hax1=gca;
xlabel('Integrated particle flux (gC m^{-2} d^{-1})');
ylabel('depth(m)');
ylim([1,3000]);
set(gca,'ydir','rev');
set(hp1,'linew',2);
title(['IR5 as Carbon Flux']);



%%
% put some of this out
% use the diary function

fileout ='IR7_All_5mBin_fluxes.txt';

diary off
if ~isempty(dir(fileout))                   % delete old output file
  delete (fileout)
end
diary(fileout);

% start with headers
disp([' ',date,'    ',mfilename,'.m']);
disp('Integrated particle flux (gC m^{-2} d^{-1})');
disp('depth(m)');


  disp(' ');
  disp('+++++++++++++')
  disp(name);
  disp(' ');
  disp('    depth             flux');
  [depth',flux']


diary off

disp(' ');
disp('*****');
disp(['   results printed to ',fileout]);
