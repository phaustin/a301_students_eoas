---
jupytext:
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(assign6a-solution)=
# Assignment 6a Solution -- diffuse flux

```{code-cell} ipython3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import expn
```

In the {ref}`flux_schwartzchild` notes I claimed
 that the following approximation was a good one:

 $$\hat{t}_f =  2 \int_0^1 \mu \exp \left (- \frac{\tau }{\mu} \right ) d\mu
       \approx  \exp \left (-1.66 \tau \right )$$

 We can check this with an exact answer, since this integral is important enough to have a function defined for it in the scipy math module.  First, be sure you understand how the change in variables

 $$u = \mu^{-1}$$

 Transforms this equation into the **third exponential integral**:

 $$\hat{t}_f = 2 \int_1^\infty \frac{\exp(-u \tau)}{u^3} du$$

 The cell below graphs this function which in python is available as::

     scipy.special.expn(3,the_tau))

```{code-cell} ipython3
"""
   plot 2*scipy.special.expn(3,the_tau))
   this is the accurate version of the flux transmission function
   defined above
"""

matplotlib.style.use("ggplot")
tau = np.arange(0.1, 5, 0.1)
flux_trans = 2 * expn(3.0, tau)
fig, ax = plt.subplots(1, 1)
ax.plot(tau, flux_trans, label="exact")
ax.plot(tau, np.exp(-1.66 * tau), label="approx")
ax.legend()
ax.set(ylabel="flux_trans", xlabel=r"vertical optical depth $\tau$")
```

## 6a Flux transmission problem

In the cell below, add 2 lines to ax.

The first line should plot the numerical approximation to

$$\hat{t}_f = 2 \int_1^\infty \frac{\exp(-u \tau)}{u^3} du$$

using np.sum and np.diff as usual.  The x axis should use these tau values

    tau=np.arange(0.1,5,0.1)

Make the line green, with a linewidth of lw=5 so it stands out. Add it to the legend

For the second line, plot the ordinary vertical transmission:

$$\hat{t} = \exp(-\tau)$$

for comparison, as a black line with lw=5.

```{code-cell} ipython3
---
deletable: false
nbgrader:
  cell_type: code
  checksum: 60325a97c3b77fdfa8af1e71a221d271
  grade: true
  grade_id: cell-dc415abb23bb771d
  locked: false
  points: 5
  schema_version: 2
  solution: true
---
def trans_fun(tau,mu):
    output = 2*mu*np.exp(-tau/mu)
    return output

def do_int(tau,mu_vec):
    
    trans_vec=np.empty_like(mu_vec)
    
    for index, the_mu in enumerate(mu_vec):
        trans_vec[index]=trans_fun(tau,the_mu)
    dmu=np.diff(mu_vec)
    mid_trans = (trans_vec[1:] + trans_vec[:-1])/2.
    return np.sum(mid_trans*dmu)       
    

mu_vec = np.linspace(0.01,1,150)
tau_vec=np.arange(0.1,5,0.1)
flux_trans = np.empty_like(tau_vec)
for index,tau in enumerate(tau_vec):
    flux_trans[index] = do_int(tau,mu_vec)
    
fig, ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(tau_vec,flux_trans,'r+',markersize=15,label="numeric integration: flux");
ax.set_xlabel('optical depth (unitless)')
ax.set_ylabel('transmission (unitless)')
ax.plot(tau_vec,np.exp(-tau_vec),label='beam transmission')
ax.plot(tau_vec,np.exp(-1.666*tau_vec),label='diffusivity approx',lw=3)
flux_trans = 2 * expn(3.0, tau_vec)
ax.plot(tau_vec,flux_trans,label='flux transmission: exact',lw=3)

ax.legend();
```
