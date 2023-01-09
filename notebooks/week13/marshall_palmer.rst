(assign6c_marshall)=

# Assign 6c: Marshall Palmer Solution

Given a size distribution

$$
n(D) = n_0 \exp(-4.1 RR^{-0.21} D )
$$

with $n_0$ in units of $m^{-3}\,mm^{-1}$, D in mm,
so that $\Lambda=4.1 RR^{-0.21}$ has to have units
of $`mm^{-1}$.

If we use this to integrate:

$$
   Z=\int D^6 n(D) dD
$$

and use the hint that

$$
   \int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}
$$

with n=6 we get:

$$
   Z=\frac{n_0 6!}{\Lambda^7}
$$

with units of  $m^{-3}\,mm^{-1}/(mm^{-1})^7=mm^6\,m^{-3}$ as required.  Since
$n_0=8000\ m^{-3}\,mm^{-1}$ and 6!=720, the
numerical coeficient is 8000x720/(4.1**7)=295.75 and  the final form is:

$$
   Z=296 RR^{1.47}
$$

