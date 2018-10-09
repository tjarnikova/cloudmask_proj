#for each lat and lon square (nested loops, lats = 180, lons = 360)

2 steps: in first, create a big variables array in h5
For each lat lon need:
1 lat
2 lon 
3 sst >from h5sst
4 kl19  >from h5sst >coeff | micro_coeffs
5 kv19 >from h5sst> coeff
6 kl37 >from h5sst >coeff
7 kv37 >from h5sst >coeff
8 tox19 >from h5sst > coef
9 tox37 >from h5sst > coef
10 Rh37 >from h5btemps >windspeed >emissf |write_data.py
11 Rv37 >from h5btemps >windspeed >emissf  |write_data.py
12 Rh19 >from h5btemps >windspeed >emissf  | write_data.py
13 Rv19 >from h5btemps >windspeed >emissf  
14 deltaT19 >from h5 file of brightness temps | given by write_data.py
15 delta T37 >from h5 file of brightness temps | given by write_data.py
16 R1 >from 3, 8-16
17 R2 >from 3, 8-16
18 W
19 L



19 columns, 360*180 rows


2) run emiss:
a) use brightness temperatures to calculate windspeed
b) input windspeed, freq 37, theta to get emmiss h and emiss v for 37, calculate Rh37 and Rv37
c) do the same for freq 19, calc Rh19 Rv19
3) run coeff:
a) use sst to get 6 coefficients
4) from brightness temperatures get deltaT 19, delta T37
5) 

