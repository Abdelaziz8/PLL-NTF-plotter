# PLL Noise Transfer Function (NTF) Plotter

This repository contains a Python script designed to analytically derive and visualize the Noise Transfer Functions (NTFs) of a Charge Pump Phase-Locked Loop (CP-PLL). Understanding these transfer functions is a critical step in mixed-signal design to predict how noise from individual subsystems (Reference, VCO, Charge Pump, and Loop Filter) propagates to the final output.

## Features
* **Automated Loop Filter Sizing:** Derives the precise values for the loop filter components ($R_1$, $C_1$, $C_2$) based on a target unity-gain frequency ($F_U$) and phase margin ($\Phi_M$) using geometric mean optimization.
* **Analytical Transfer Functions:** Constructs the exact continuous-time complex variable ($s$-domain) mathematical models for the Loop Filter impedance $Z(s)$, forward gain $G(s)$, and open-loop gain $LG(s)$.
* **NTF Generation:** Calculates the specific high-pass, low-pass, and band-pass transfer responses for:
  * Reference / Divider Noise ($NTF_{IN}$)
  * Charge Pump Noise ($NTF_{CP}$)
  * VCO Noise ($NTF_{VCO}$)
  * Loop Filter Resistor Thermal Noise ($NTF_R$)
* **Bode Plot Visualization:** Generates a clean, highly readable semilog plot of all transfer functions in dB across a wide frequency sweep.

## Prerequisites
To run this script, ensure you have Python installed along with the following libraries:
* `numpy`
* `matplotlib`

```bash
pip install numpy matplotlib
