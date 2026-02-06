import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

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
st.title("Krvni parametri – korekcija % bias i 95% CI")

# =====================
# UNOS PODATAKA
# =====================
param = st.selectbox("Izaberi krvni parametar", list(parameters.keys()))
x = st.number_input("Hb koncentracija (g/L)", value=1.0, step=0.1)
original_value = st.number_input(f"Originalna izmerena vrednost {param}", value=0.0, step=0.01)

# =====================
# IZRAČUNAVANJE
# =====================
a = parameters[param]["a"]
b = parameters[param]["b"]
R2 = parameters[param]["R2"]

# % bias prema formuli
percent_bias = a * x + b
SE = abs(percent_bias) * math.sqrt(1 - R2)
ci_low = percent_bias - 1.96 * SE
ci_high = percent_bias + 1.96 * SE

# Korekcija originalne vrednosti
if percent_bias != -100:
    real_value = original_value / (1 + percent_bias / 100)
else:
    real_value = float('nan')

# =====================
# PRIKAZ REZULTATA
# =====================
st.markdown("### Rezultati")
st.write(f"**% bias:** {percent_bias:.2f}")
st.write(f"**95% CI:** [{ci_low:.2f}, {ci_high:.2f}]")
st.write(f"**Korigovana realna vrednost {param}:** {real_value:.2f}")

# =====================
# GRAFIK
# =====================
x_range = np.linspace(0, 10, 200)  # Hb od 0 do 10 g/L
y_range = a * x_range + b
ci_l = y_range - 1.96 * SE
ci_h = y_range + 1.96 * SE

fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x_range, y_range, label="Regresija")
ax.fill_between(x_range, ci_l, ci_h, alpha=0.3, label="95% CI")
ax.scatter(x, percent_bias, color="red", label="Unos", zorder=5)
ax.set_xlabel("Hb koncentracija (g/L)")
ax.set_ylabel("% bias")
ax.set_xlim(0, 10)
ax.set_title(f"{param} – % bias vs Hb")
ax.legend()
ax.grid(True)

st.pyplot(fig)
