import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =====================
# KRVI PARAMETRI
# =====================
parameters = {
    "BHB": {"a": 5.3201, "b": 0.957, "R2": 0.9913},
    "NEFA": {"a": 9.8218, "b": 2.5353, "R2": 0.9972},
    "GLU": {"a": -2.9538, "b": -1.401, "R2": 0.9794},
    "ALB": {"a": 1.0954, "b": 0.9147, "R2": 0.9762},
    "TPROT": {"a": 1.0849, "b": 0.426, "R2": 0.9893},
    "UREA": {"a": 0.8905, "b": 0.1979, "R2": 0.9892},
    "TBIL": {"a": -5.3246, "b": -1.6739, "R2": 0.9861},
    "AST": {"a": 15.678, "b": 5.0673, "R2": 0.9935},
    "GGT": {"a": -3.2805, "b": 0.3675, "R2": 0.9874},
    "LDH": {"a": 21.27, "b": 16.265, "R2": 0.9843},
    "ALP": {"a": -2.557, "b": -2.5083, "R2": 0.9801},
    "TGC": {"a": 1.8558, "b": 0.4124, "R2": 0.9936},
    "CHOL": {"a": 2.3468, "b": 0.1215, "R2": 0.9932},
    "Ca": {"a": 0.1944, "b": 0.0217, "R2": 0.8343},
    "P": {"a": 1.2163, "b": 0.4661, "R2": 0.9919},
    "Mg": {"a": 0.9866, "b": 0.1498, "R2": 0.9709},
    "INS": {"a": -5.5017, "b": -3.7803, "R2": 0.9875},
    "T3": {"a": -1.0701, "b": -0.4693, "R2": 0.9816},
    "T4": {"a": -0.9452, "b": -0.8947, "R2": 0.9797},
    "CORT": {"a": -2.4264, "b": -2.5357, "R2": 0.9434}
}

# =====================
# NASLOV
# =====================
st.title("Krvni parametri – 3D prikaz izmerene i korigovane vrednosti")

# =====================
# UNOS PODATAKA
# =====================
param = st.selectbox("Izaberi krvni parametar", list(parameters.keys()))
x = st.number_input("Hb koncentracija (g/L)", value=1.0, step=0.1)
original_value = st.number_input(f"Originalna izmerena vrednost {param}", value=0.0, step=0.01)

# =====================
# IZRAČUNAVANJE % BIAS
# =====================
a = parameters[param]["a"]
b = parameters[param]["b"]
R2 = parameters[param]["R2"]

percent_bias = a * x + b
SE = abs(percent_bias) * math.sqrt(1 - R2)
ci_low = percent_bias - 1.96 * SE
ci_high = percent_bias + 1.96 * SE

# =====================
# KOREKCIJA REALNE VREDNOSTI
# =====================
real_value = original_value / (1 + percent_bias / 100)
real_ci_low = original_value / (1 + ci_high / 100)
real_ci_high = original_value / (1 + ci_low / 100)

# =====================
# PRIKAZ REZULTATA
# =====================
st.markdown("### Rezultati")
st.write(f"**% bias:** {percent_bias:.2f}")
st.write(f"**Korigovana realna vrednost {param}:** {real_value:.2f}")
st.write(f"**95% CI realne vrednosti:** [{real_ci_low:.2f}, {real_ci_high:.2f}]")

# =====================
# GRAF 3: 3D – Hb, % bias, vrednosti parametra
# =====================
fig3 = plt.figure(figsize=(8,6))
ax3 = fig3.add_subplot(111, projection='3d')

# tačke: izmerena i korigovana vrednost
# X = Hb
# Y = % bias
# Z = vrednost parametra

# izmerena vrednost
ax3.scatter(x, percent_bias, original_value, color='red', s=60, label='Izmerena vrednost')
# korigovana vrednost
ax3.scatter(x, percent_bias, real_value, color='blue', s=60, label='Korigovana vrednost')
# linija koja spaja dve tačke
ax3.plot([x, x], [percent_bias, percent_bias], [original_value, real_value], color='black', linestyle='--')

ax3.set_xlabel("Hb koncentracija (g/L)")
ax3.set_ylabel("% bias")
ax3.set_zlabel(f"{param} (vrednost)")
ax3.set_title(f"{param} – 3D prikaz izmerene i korigovane vrednosti")
ax3.legend()
ax3.grid(True)

st.pyplot(fig3)
