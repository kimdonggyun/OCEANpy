function summed = myerrcalc(x);
% INPUT: 2 element vector containing A, b values will use to calculate error
% OUTPUT: summed is a single value which we want to have minimized, here our error

      % start by setting things up
A = x(1);
b = x(2);
      % these are the coefficients used to calculate 
      %  the mass*sinking velocity particle: m*v = A* d^b
      %  where d is in cm, m*v is in g-C m/d

load nspecdata
      %  use cells to store data
      %  npts  , number of cases to work with
      %  cfilein, strings containing names of xcel sheets used, cell{ndata},
      %  ctrapflux, measured trap flux, g-C m^-2 d^-1, 1x ndata
      %  nspec, number spectrum, #/cm^-4, each cell contains a vector 
      %  d_cm, diameter corresponding to each nspec, vector in a cell
      %  d_mm, d_cm in mm
      
cm3_m3 = 1e6;       % factor to convert from #/cm^3 to #/m^3 
estflux = zeros(1,npts);   % flux estmated from spectra 
% parameters for the log-normal fit
 a = 4.9975;
 b1 = 0.4334;
 x0 = 0.0177;
for idata = 1 : npts
  dd = d_cm{idata};
  ran = dd>0;               % need to delete bad ds, messing up integ
  dd=dd(ran);
  m_v = A * dd .^ b;       % calc m*v for diff dias
  flspec = m_v .* nspec{idata}(ran);
  estflux(idata) = cm3_m3 * trapz(dd, flspec);
end

% now for error calc

summed = sum( ( log(estflux) -log(ctrapflux) ).^2 ); 

% worry about negative values of A
if A<0
  summed = 1000;
end
  