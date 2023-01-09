# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,md:myst,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0-dev
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
#

# %%
import a301_lib
#from sat_lib import radiation
import sys
from sat_lib.radiation import calc_radiance, planck_invert
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5agg')

# %%
import numpy as np
domega=2/36000.**2.
print('domega: ',domega)

H=10000.
k=3.e-2
rmix=6.e-3
tau=k*rmix*H
print("tau: ",tau)
Tr=np.exp(-tau)
print("Tr: ",Tr)

Bsfc=calc_radiance(9.e-6,300.)*1.e-6
Batm=calc_radiance(9.e-6,270.)*1.e-6
print('Bsfc, Batm ',Bsfc,Batm)
TOA=Bsfc*Tr + (1 - Tr)*Batm
print('TOA radiance: ',TOA)
Tb=planck_invert(9.e-6,TOA*1.e6)
print('Tb: ',Tb)
flux=TOA*domega*2.
print("flux: ",flux)

cos35 = np.cos(35*np.pi/180.)
print('cos35: ',cos35)
print('omega: ',2*np.pi*(1. - cos35))


# %%
from sat_lib.radiation import sigma

microns=np.linspace(0.1,700,500000)
meters=microns*1.e-6
cms=microns*1.e-4
inv_cms=1./cms
inv_microns=1./microns
inv_meters=1/meters

temp=280.
planck_len=calc_radiance(meters,temp)

fig, ax2 = plt.subplots(1,1,figsize=(10,10))
temp=260.
planck_len=calc_radiance(meters,temp)
l0=ax2.plot(microns,np.pi*planck_len*1.e-6,':',lw=4)
temp=270.
planck_len=calc_radiance(meters,temp)
l1=ax2.plot(microns,np.pi*planck_len*1.e-6,'-',lw=4)
temp=280.
planck_len=calc_radiance(meters,temp)
l2=ax2.plot(microns,np.pi*planck_len*1.e-6,'--',lw=3)
temp=290.
planck_len=calc_radiance(meters,temp)
l3=ax2.plot(microns,np.pi*planck_len*1.e-6,'-.',lw=4)
temp=300.
planck_len=calc_radiance(meters,temp)
l4=ax2.plot(microns,np.pi*planck_len*1.e-6,':',lw=4)
ax2.set_xlabel(r'wavelength ($\mu m$)')
ax2.set_ylabel(r'Monochromatic blackbody flux $E_{bb\lambda}$ ($W\,m^{-2}\,\mu m^{-1}$)')
ax2.set_title("Blackbody flux vs. wavelength")
# Major ticks every 20, minor ticks every 5
major_ticks = np.arange(0, 31, 5)
minor_ticks = np.arange(0, 31, 1)

ax2.set_xticks(major_ticks)
ax2.set_xticks(minor_ticks, minor=True)
major_ticks = np.arange(0, 36, 5)
minor_ticks = np.arange(0, 36, 1)
ax2.set_yticks(major_ticks)
ax2.set_yticks(minor_ticks, minor=True)

# And a corresponding grid
ax2.grid(which='both')

# Or if you want different settings for the grids:
ax2.grid(which='minor', alpha=0.5)
ax2.grid(which='major', alpha=0.7)
ax2.grid(color='k', linestyle=':', linewidth=1)
ax2.set_xlim(0,30)
#ax2.set_ylim()
legax=ax2.legend(('260 K','270 K','280 K','290 K','300 K'),loc='upper left')
ax2.figure.savefig('a301_planck.pdf')
ax2.figure.savefig('a301_planck.png')
fig.tight_layout()
fig.canvas.draw()
plt.show()
print(f"sb flux: {sigma*temp**4.}")
integlen=np.sum(np.diff(meters)*planck_len[:-1])*np.pi
print(f"integrated flux: {integlen}")
microns=np.array([10.,12.])
meters=microns*1.e-6
planck_len=calc_radiance(meters,temp)
print(np.mean(planck_len)*2.e-6)

# %% [markdown]
# Answer all four questions (note weights). Show all your work, using
# extra blank pages if needed. Include the attached planck function figure
# if used for the calculations.
#
#   - (10) A satellite orbiting at an altitude of 36000 km observes the
#     surface in a thermal channel with a wavelength range of
#     $8\ \mu m < \lambda < 10\ \mu m$.
#     
#       - Assuming that the atmosphere has density scale height of
#         $H_\rho=10$ km and a surface air density of $\rho_{air}=1$
#         and that the absorber has mass absorption coefficient of
#         $k_\lambda = 3 \times 10^{-2}\ m^2/kg$ at $\lambda=9\ \mu m$
#         and a mixing ratio $6 \times 10^{-3}$ kg/kg, find the vertical
#         optical thickness $\tau$ and transmittance of the atmosphere
#         directly beneath the satellite

# %%
1/15

# %%
import math as m
Hrho = 11e3
rho_air = 1.2
k_lambda = 0.15
ztop = 20.e3
rmix = 4.e-4
decay = (1 - m.exp(-ztop/Hrho))
tau = Hrho*rho_air*k_lambda*rmix*decay
print(tau)
print(m.exp(-tau))

# %% [markdown]
#     
#       - If the surface is black with a temperature of 290 K, and the
#         atmosphere has an average temperature of 270 K, find the
#         
#           - radiance observed by the satellite in at 9 $\mu m$
#   

# %%
Bsfc=calc_radiance(15.e-6,290.)*1.e-6
Batm=calc_radiance(15.e-6,270.)*1.e-6
print('Bsfc, Batm ',Bsfc,Batm)
TOA=Bsfc*Tr + (1 - Tr)*Batm
print('TOA radiance: ',TOA)
Tb=planck_invert(15.e-6,TOA*1.e6)
print('Tb: ',Tb)
print('Esfc, Eatm ',m.pi*Bsfc,m.pi*Batm)
E_TOA=m.pi*(Bsfc*Tr + (1 - Tr)*Batm)
print('TOA flux: ',E_TOA)


# %% [markdown]
#    
#       - Given a pixel size 4 $km^2$, what is the flux, in , reaching
#         the satellite in this channel?
#     


# %%
microns=np.linspace(14.,16.,5000)
meters=microns*1.e-6
planck_vals=calc_radiance(meters,temp)
integlen=np.sum(np.diff(meters)*planck_len[:-1])
area = 4.
orbit = 36.e3
fov = area/orbit**2.
print(f"integrated radiance: {integlen}")
print(f"fov {fov}")
print(f"flux at satellite {integlen*fov}")


# %% [markdown]
#     Extra space for problem 1
#     
#     2$ Short answer (6):
#     
#       - (3) A cone has a spreading angle of 35 degrees between its
#         center and its side. What is its subtended solid angle?
#     
#       - (3) Assuming that radiance is independent of the distance $d$
#         between an instrument and a surface, show that the flux from the
#         surface decreases as $1/d^2$
#
#   - (5) Integrate the Schwartzchild equation
#     ([\[eq:schwarz\]](#eq:schwarz)) for constant temperature and show
#     you get ([\[eq:isothermal\]](#eq:isothermal))
#
#   - Pyresample (10)
#     
#     Consider the following code:
#     
#         from pyresample import  SwathDefinition, kd_tree, geometry
#         proj_params = get_proj_params(m5_file)
#         swath_def = SwathDefinition(lons_5km, lats_5km)
#         area_def_lr=swath_def.compute_optimal_bb_area(proj_dict=proj_params)
#         area_def_lr.name="ir wv retrieval modis 5 km resolution (lr=low resolution)"
#         area_def_lr.area_id='modis_ir_wv'
#         area_def_lr.job_id = area_def_lr.area_id
#         fill_value=-9999.
#         image_wv_ir = kd_tree.resample_nearest(swath_def, wv_ir_scaled.ravel(),
#                                           area_def_lr, radius_of_influence=5000, 
#                                               nprocs=2,fill_value=fill_value)
#         image_wv_ir[image_wv_ir < -9000]=np.nan
#         print(f'\ndump area definition:\n{area_def_lr}\n')
#         print((f'\nx and y pixel dimensions in meters:'
#                f'\n{area_def_lr.pixel_size_x}\n{area_def_lr.pixel_size_y}\n'))
#     
#     In the context of this snippet, explain what the following objects
#     (i.e. their type, what some of their attributes are, etc.) and how
#     they are used to map a satellite image:
#     
#       - proj\_params
#     
#       - swath\_def
#     
#       - area\_def\_lr
#     
#       - wv\_ir\_scaled.ravel()
#     
#       - kd\_tree.resample\_nearest
#
# Extra space for problem 4
#
# ![image](a301_planck.pdf)
#
# **Useful Equations:**
#
# <span>2</span>
#
# \[\begin{aligned}
#   \label{eq:nu}
#   \nu &=& c / \lambda\\
#    E &=& h \nu\end{aligned}\]
#
# \[\label{eq:omega}
#   d \omega = \sin \theta d\theta d\phi = -d\mu d\phi \approx \frac{ A}{r^2}\]
#
# \[\label{eq:cos}
#   S = S_0 \cos(\theta)\]
#
# \[\label{eq:conservation}
#   a_\lambda + r_\lambda + t_\lambda = 1\]
#
# \[\label{eq:intensity}
#   L_\lambda = \frac{\Delta E}{\Delta \omega \Delta \lambda}\]
#
# \[\label{eq:flux_int}
#   E = \int_0^{2 \pi} \int_0^{\pi/2} L \cos \theta \sin \theta d \theta d \phi\]
#
# \[\label{planck}
# B_\lambda(T)  = \frac{2 h c^2}{\lambda^5 \left [ \exp (h c/(\lambda k_B T )) -1 \right ] }\]
#
# \[\label{eq:pi}
#   E_{\lambda\,BB} = \pi B_\lambda\]
#
# \[\label{eq:stefan}
#   E^* =\sigma T^4\]
#
# \[\label{eq:taylor}
#   E_\lambda(T) \approx E_{\lambda\, 0} + \left .\frac{dE_\lambda}{dT}  \right |_{T_0,\lambda} \!\!\! (T - T_0) + \ldots\]
#
# \[\label{eq:exp}
#   \exp(x) = 1 + x +  \frac{x^2}{2} + \frac{x^3}{3!} + \ldots\]
#
# $~$
#
# Beer’s law for extinction: \[\begin{aligned}
#   \label{eq:extinct}
# \frac{dL_\lambda}{L_\lambda}  & = & - \kappa_{\lambda\, s} \rho_{g} ds - 
#                     \kappa_{\lambda\,a } \rho_{g} ds \nonumber\\
#         &=& - \kappa_{\lambda e} \rho_{g} ds = \kappa_{\lambda e} \rho_{g} dz\end{aligned}\]
# (assuming $\rho_{a}$=$\rho_{s}$=$\rho_{g}$).
#
# Beer’s law integrated:
#
# \[\label{eq:binteg}
#   E= E_0 \exp (- \tau)\]
#
# $~$
#
# Hydrostatic equation:
#
# \[\label{eq:hydro}
#   dp = -\rho_{air}\, g\, dz\]
#
# $~$
#
# Hydrostatic equation integrated:
#
# \[\label{eq:hydroint}
# p = p_0 \exp(-z/H)\]
#
# Equation of state
#
# \[\label{eq:state}
#   p = R_d \rho_{air} T\]
#
# $~$
#
# vertical optical thickness:
#
# \[\label{eq:tauThick}
#   d \tau =  \kappa_\lambda \rho_g dz = \kappa_\lambda r_{mix} \rho_{air} dz = \beta_a dz\]
#
# integrate vertical optical thickness:
#
# \[\label{eq:tauup}
#   \tau(z_1, z_2 ) = \int_{z_1}^{z_{2}} k_\lambda r_{mix} \rho_{air}\, dz^\prime\]
#
# Transmission function for upwelling radiation
#
# \[\begin{aligned}
# \hat{t} &=& \exp ( - (\tau - \tau^\prime) ) \nonumber\\\end{aligned}\]
#
# $~$
#
# $~$
#
# Schwarzchild’s equation for an absorbing/emitting gas
#
# \[\label{eq:schwarz}
#   dL = -L\, d\tau + B_{\lambda}(z) d \tau\]
#
# $~$
#
# Radiance an isothermal layer:
#
# \[\label{eq:isothermal}
# L_\uparrow(\tau_T) = L_0 \exp( - \tau_T ) + (1 - \exp( - \tau_T)) B_\lambda(T)\]
#
# Integrated Schwartzchild I:
#
# \[\label{eq:integI}
# \begin{gathered}
#               L_\lambda = B_\lambda(T_{skin} ) \hat{t}_{tot} + \sum_{j=1}^n e_\lambda B_\lambda(T_j) \hat{t}_{\lambda,j}
# \end{gathered}\]
#
# Integrated Schwartzchild II:
#
# \[\label{eq:integII}
#          \begin{gathered}
#            L_\lambda = B_\lambda(T_{skin}) \hat{t}_{\lambda,tot} + \sum_{j=1}^n  
#            B_\lambda(T_j) \Delta \hat{t}_{\lambda,j}
#          \end{gathered}\]
#
# -----
#
# $~$
#
# Useful constants:
#
# $~$
#
# $c_{pd}=1004$ ,
#
# $\sigma=5.67 \times  10^{-8}$
#
# $k_b = 1.381  \times 10^{-23}$
#
# $c=3 \times 10^{8}$
#
# $h=6.626 \times 10^{-34}$
#
# $\pi \approx 3.14159$
#
# $R_d=287 \un{J\,kg^{-1}\,K^{-1}}$
#
# Solar radius=$7 \times 10^8$ m
#
# Earth-sun distance =$1.5 \times 10^{11}$ m
