% find_Ab.m
%find the optimal values of A, b for morten's data
%

clear

x0 = [1.7e-08, -0.3186];         % initial values for coeffs, Lionels
                              % 
                              
xbest = fminsearch(@myerrcalc,x0);

errorlionel = myerrcalc(x0)

errorhere = myerrcalc(xbest)