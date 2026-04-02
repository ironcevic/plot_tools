import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.size'] = 14
colours = {
  "green": "#00B828",
  "yellow": "#FFD900",
  "purple": "#800FF2",
  "blue": "#0073FF",
  "orange": "#FF5000",
  "grey": "#B3B3B3",
}
nm_ticks = np.array((400, 500, 600, 800, 1000, 1500, 3000))

def broaden(singlet_name, triplet_name, energy="eV", broadening=0.2,
            e_min=0.0, e_max=3.5, n_points=1000,
            nm_ticks=nm_ticks, visible=False):
  """
  Broadens a stick spectrum.
  Input:
  - singlet_name: stick spectrum file with two columns
  - triplet_name: stick spectrum file with two columns
  - energy: units for both files, either "eV" or "nm"
  - broadening: broadening in eV
  - e_min: minimum energy in eV on plot
  - e_max: maximum energy in eV on plot
  - nm_list: list of wavelengths in nm
  - n_points: number of points between e_min and e_max
  Output:A
  - broadened spectrum as a pdf
  """

  # check for correct syntax
  if energy != "eV" and energy != "nm":
    print("Energy must either eV or nm, in quotes.")
    return

  # check for files
  singlet = 0
  triplet = 0
  if os.path.exists(singlet_name):
    singlet = 1
    print("Singlet file found.")
  if os.path.exists(triplet_name):
    triplet = 1
    print("Triplet file found.")
  if singlet == 0 and triplet == 0:
    print("No files found, exiting.")
    return

  # create points array, in eV
  points = np.linspace(e_min, e_max, n_points)

  # create figure, axes etc
  fig, ax_ev = plt.subplots(figsize=(6, 4))
  ax_ev.set_xlim(e_min, e_max)
  ax_ev.set_xlabel("energy (eV)")
  ax_ev.set_ylabel("intensity (arb. units)")
  ax_ev.xaxis.set_ticks_position("bottom")
  ax_ev.xaxis.set_label_position("bottom")

  ax_nm = ax_ev.twiny()
  ax_nm.set_xlim(e_min, e_max) # ensure twin axis has the same limits
  ax_nm.set_xlabel("wavelength (nm)")
  ax_nm.xaxis.set_ticks_position("top")
  ax_nm.xaxis.set_label_position("top")
  energy_ticks_for_nm = 1239.84193 / nm_ticks
  ax_nm.set_xticks(energy_ticks_for_nm)
  ax_nm.set_xticklabels(nm_ticks)

  singlet_broad = []
  triplet_broad = []
              
  # main bit
  if singlet == 1:
    # load data
    data = np.genfromtxt(singlet_name)
    singlet_e = data[:, 0]
    singlet_i = data[:, 1]
    # create intensities array
    singlet_broad = np.zeros(n_points)
    # change to energy axis if needed
    if energy == "nm":
      singlet_e = 1239.84193 / singlet_e
    for signal_idx in range(len(singlet_e)):
      singlet_broad += singlet_i[signal_idx] * \
      np.exp(-(points - singlet_e[signal_idx])**2 / (2 * broadening**2))

  if triplet == 1:
    # load data
    data = np.genfromtxt(triplet_name)
    triplet_e = data[:, 0]
    triplet_i = data[:, 1]
    # create intensities array
    triplet_broad = np.zeros(n_points)
    # change to energy axis if needed
    if energy == "nm":
      triplet_e = 1239.84193 / triplet_e
    for triplet_idx in range(len(triplet_e)): # Corrected loop variable
      triplet_broad += triplet_i[triplet_idx] * \
      np.exp(-(points - triplet_e[triplet_idx])**2 / (2 * broadening**2))
    # plot
    triplet_broad = triplet_broad / np.max([singlet_broad, triplet_broad])
    singlet_broad = singlet_broad / np.max([singlet_broad, triplet_broad])
    ax_ev.plot(points, triplet_broad, label="triplet", color=colours['orange'])
    ax_ev.bar(triplet_e, -0.1, color=colours['orange'], width=0.05, alpha=0.5)
  else:
    singlet_broad = singlet_broad / np.max(singlet_broad)
  
  ax_ev.axhline(0, color="black", linestyle="--")
  if visible == True:
    ax_ev.axvline(3.2627419210526316, color="black", linestyle="--")
    ax_ev.axvline(1.6531225733333335, color="black", linestyle="--")
  ax_ev.legend(frameon=False)
  plt.tight_layout()
  plt.savefig("figure.pdf")
  plt.show()
