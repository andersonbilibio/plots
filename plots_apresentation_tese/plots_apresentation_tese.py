# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 21:04:31 2023
###---> Plots figuras Apresentation tese...
@author: Anderson Bilibio
"""

import numpy as np # For creating some fake data

# Use some notebook magic - forget the next line in normal scripted code
%matplotlib inline

import matplotlib.pyplot as plt # Gives access to basic plotting functions
import matplotlib.gridspec as gridspec # GRIDSPEC !
from matplotlib.colorbar import Colorbar # For dealing with Colorbars the proper way - TBD in a separate PyCoffee ?







# Ok, let us start by creating some fake data
x = np.random.randn(1000)
y = np.random.randn(1000)
z = np.sqrt(x**2+y**2)








fig = plt.figure(1, figsize=(28,15))


# Now, create the gridspec structure, as required
gs = gridspec.GridSpec(3,4, height_ratios=[0.5,1,0.2], width_ratios=[1,0.2,0.2,1])

gs.update(left=0.05, right=0.95, bottom=0.08, top=0.93, wspace=0.02, hspace=0.03)







# First, the scatter plot
# Use the gridspec magic to place it
# --------------------------------------------------------
ax1 = plt.subplot(gs[1,0]) # place it where it should be.
# --------------------------------------------------------

# The plot itself
#plt1 = ax1.scatter(x, y, c = z, 
                   # marker = 's', s=20, edgecolor = 'none',alpha =1,
                   # cmap = 'magma_r', vmin =0 , vmax = 4)


# Define the limits, labels, ticks as required
# ax1.grid(True)
# ax1.set_xlim([-4,4])
# ax1.set_ylim([-4,4])
# ax1.set_xlabel(r' ') # Force this empty !
# ax1.set_xticks(np.linspace(-4,4,9)) # Force this to what I want - for consistency with histogram below !
# ax1.set_xticklabels([]) # Force this empty !
# ax1.set_ylabel(r'My y label')





#################################################--->PLOT al lado de Y
# And now the histogram
# Use the gridspec magic to place it
# --------------------------------------------------------
ax1v = plt.subplot(gs[1,1])
# --------------------------------------------------------


# Plot the data
# bins = np.arange(-4,4,0.1)
# ax1v.hist(y,bins=bins, orientation='horizontal', color='k', edgecolor='w')
#ax1v.scatter(x, y, c = z, 
                   # marker = 's', s=20, edgecolor = 'none',alpha =1,
                   # cmap = 'magma_r', vmin =0 , vmax = 4)


# Define the limits, labels, ticks as required
# ax1v.set_yticks(np.linspace(-4,4,9)) # Ensures we have the same ticks as the scatter plot !
# ax1v.set_xticklabels([])
# ax1v.set_yticklabels([])
# ax1v.set_ylim([-4,4])
# ax1v.grid(True)



#################################################--->PLOT em baixo de X
# And now another histogram
# Use the gridspec magic to place it
# --------------------------------------------------------
ax1h = plt.subplot(gs[2,0])
# --------------------------------------------------------



# Plot the data
# bins = np.arange(-4,4,0.1)
# ax1h.hist(x, bins=bins, orientation='vertical', color='k', edgecolor='w')
#ax1h.scatter(x, y, c = z, 
                   # marker = 's', s=20, edgecolor = 'none',alpha =1,
                   # cmap = 'magma_r', vmin =0 , vmax = 4)

# Define the limits, labels, ticks as required
# ax1h.set_xticks(np.linspace(-4,4,9)) # Ensures we have the same ticks as the scatter plot !
# ax1h.set_yticklabels([])
# ax1h.set_xlim([-4,4])
# ax1h.set_xlabel(r'My x label')
# ax1h.grid(True)



#################################################--->PLOT 2 em baixo de X
ax2h = plt.subplot(gs[2,1])
#ax2h.plot(x,z)



#################################################
# # Finally, show some 'spectra' in the right panel
# # Use the gridspec magic to place it
# # --------------------------------------------------------
# ax2 = plt.subplot(gs[0:2,3]) # Make it span the entire height of the figure (3 rows)
# # --------------------------------------------------------

# # Plot the data
# plt.plot(x[::20], ls = '-', color='darkviolet', lw=2)
# plt.plot(y[::20], ls = '-', color ='tomato', lw=2)

# # Define the limits, labels, ticks as required
# ax2.set_xlabel('My other x label')
# ax2.set_ylabel('My other y label')
# ax2.set_ylim([-4,4])
# ax2.grid(True)