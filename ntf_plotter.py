import numpy as np
import matplotlib.pyplot as plt

# --- 1. SYSTEM PARAMETERS ---
F_OUT = 3.36e9
F_REF = 160e6
N = F_OUT / F_REF
KVCO_HZ_V = 90e6
KVCO_RAD = KVCO_HZ_V * 2 * np.pi
ICP = 300e-6
KPD = ICP / (2 * np.pi)  # Phase Detector Gain [A/rad]
PM_DEG = 60
FU = 2.5e6  # Target Unity Gain Frequency

# --- 2. COMPONENT DERIVATION (Stability locked to PM) ---
omega_u = 2 * np.pi * FU
PM_RAD = np.radians(PM_DEG)
tan_pm = np.tan(PM_RAD)
sec_pm = 1 / np.cos(PM_RAD) # Equivalent to sqrt(tan^2(x) + 1)

# Capacitor ratio Kc = C1 / C2 
kc = 2 * (tan_pm**2 + tan_pm * sec_pm)
# Spread Factor S = wu/wz = wp3/wu = sqrt(1+Kc) 
spread = np.sqrt(1 + kc)

mag_corr = np.sqrt((1 + (1/spread)**2) / (1 + spread**2))
c2 = (ICP * KVCO_HZ_V * mag_corr) / (N * (omega_u**2))
c1 = c2 * kc
r1 = spread / (omega_u * c1)

# --- 3. TRANSFER FUNCTION DEFINITIONS ---
f = np.logspace(1, 10, 2000) # 10Hz to 10GHz
s = 2 * np.pi * 1j * f

# Loop Filter Z(s)
Z_s = (s*r1*c1 + 1) / (s**2*r1*c1*c2 + s*(c1 + c2))

# Forward Gain G(s) = Kpd * Z(s) * Kvco/s
G_s = KPD * Z_s * (KVCO_RAD / s)

# Open Loop Gain LG(s) = G(s)/N
LG_s = G_s / N

# --- Noise Transfer Functions---
# 1. Input/Reference NTF: (N * LG) / (1 + LG)
NTF_IN = (N * LG_s) / (1 + LG_s)

# 2. Charge Pump NTF: (N / Kpd) * LG / (1 + LG)
NTF_CP = (N / KPD) * (LG_s / (1 + LG_s))

# 3. Loop Filter Resistor (R1) NTF: (Kvco/s) / (1 + LG)
# Note: This uses the noise voltage at the filter node
NTF_R = (KVCO_RAD / s) / (1 + LG_s)

# 4. VCO NTF: 1 / (1 + LG)
NTF_VCO = 1 / (1 + LG_s)

# --- 4. PLOTTING ---
plt.figure(figsize=(12, 8))

plt.semilogx(f, 20*np.log10(np.abs(NTF_IN)), label='Reference ($NTF_{IN}$)', color='blue', linewidth=2)
plt.semilogx(f, 20*np.log10(np.abs(NTF_CP)), label='Charge Pump ($NTF_{CP}$)', color='red', linewidth=2)
plt.semilogx(f, 20*np.log10(np.abs(NTF_R)), label='Loop Filter R ($NTF_{R}$)', color='lime', linewidth=2)
plt.semilogx(f, 20*np.log10(np.abs(NTF_VCO)), label='VCO ($NTF_{VCO}$)', color='magenta', linewidth=2)

# Formatting to match the provided image
plt.title('Phase Noise Transfer Functions (NTFs)', fontsize=14)
plt.xlabel('Frequency (Hz)', fontsize=12)
plt.ylabel('|NTF| (dB)', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True, shadow=True)
plt.xlim([10, 1e10])
plt.ylim([-200, 160]) # Adjusting Y-axis to see the high CP gain

plt.tight_layout()
plt.show()
