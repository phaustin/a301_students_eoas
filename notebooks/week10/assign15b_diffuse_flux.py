# ---
# jupyter:
#   jupytext:
#     notebook_metadata_filter: all,-language_info,-toc,-latex_envs
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
#
import matplotlib
import matplotlib.pyplot as plt

# %%
import numpy as np
from scipy.special import expn

np.log(0.2)

# %% [markdown]
# # Introduction
#
#
#
# In the [flux_schwartzchild](https://clouds.eos.ubc.ca/~phil/courses/atsc301/flux_schwartzchild.html) notes I claimed
#  that the following approximation was a good one:
#
#  $$\hat{t}_f =  2 \int_0^1 \mu \exp \left (- \frac{\tau }{\mu} \right ) d\mu
#        \approx  \exp \left (-1.66 \tau \right )$$
#
#  We can check this with an exact answer, since this integral is important enough to have a function defined for it in the scipy math module.  First, be sure you understand how the change in variables
#
#  $$u = \mu^{-1}$$
#
#  Transforms this equation into the **third exponential integral**:
#
#  $$\hat{t}_f = 2 \int_1^\infty \frac{\exp(-u \tau)}{u^3} du$$
#
#  The cell below graphs this function which in python is available as::
#
#      scipy.special.expn(3,the_tau))

# %%
"""
   plot 2*scipy.special.expn(3,the_tau))
   this is the accurate version of the flux transmission function
   defined above
"""
# %matplotlib inline

matplotlib.style.use("ggplot")
tau = np.arange(0.1, 5, 0.1)
flux_trans = 2 * expn(3.0, tau)
fig, ax = plt.subplots(1, 1)
ax.plot(tau, flux_trans, label="exact")
ax.plot(tau, np.exp(-1.66 * tau), label="approx")
ax.legend()
ax.set(ylabel="flux_trans", xlabel=r"vertical optical depth $\tau$")

# %% [markdown]
# # 15B Flux transmission problem
#
# In the cell below, add 2 lines to ax.
#
# The first line should plot the numerical approximation to
#
# $$\hat{t}_f = 2 \int_1^\infty \frac{\exp(-u \tau)}{u^3} du$$
#
# using np.sum and np.diff as usual.  The x axis should use these tau values
#
#     tau=np.arange(0.1,5,0.1)
#
# Make the line green, with a linewidth of lw=5 so it stands out (it's too late
# at this point to add it to the legend easily, although that can be done).
#
# For the second line, plot the ordinary vertical transmission:
#
# $$\hat{t} = \exp(-\tau)$$
#
# for comparison, as a black line with lw=5.
#
# To show the figure, the last line in your cell should be::
#
#     display(fig)

# %% deletable=false nbgrader={"cell_type": "code", "checksum": "60325a97c3b77fdfa8af1e71a221d271", "grade": true, "grade_id": "cell-dc415abb23bb771d", "locked": false, "points": 5, "schema_version": 2, "solution": true}
# YOUR CODE HERE
# raise NotImplementedError()
