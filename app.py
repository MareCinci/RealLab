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
st.title("Krvni parametri – % bias i korekcija vrednosti")

# =====================
# UNOS PODATAKA
# =====================
param = st.selectbox("Izaberi krvni parametar", list(parameters.keys()))
x = st.number_input("Hb koncentracija (g/L)", value=1.0, step=0.1)
measured_value = st.number_input(
    f"Izmerena vrednost {param}", value=0.0, step=0.01
)

st.markdown("### Preanalitički uslovi")

transport_answer = st.radio(
    "Da li je transport i čuvanje uzorka bilo na sobnoj temperaturi?",
    ["NE", "DA"],
    index=0
)

time_answer = st.radio(
    "Da li je od uzorkovanja do obrade u laboratoriji prošlo više od 8 sati?",
    ["NE", "DA"],
    index=0
)

room_temp = transport_answer == "DA"
delay_over_8h = time_answer == "DA"

# =====================
# IZRAČUNAVANJE % BIAS
# =====================
a = parameters[param]["a"]
b = parameters[param]["b"]
R2 = parameters[param]["R2"]

# Linearni bias
percent_bias = a * x + b

# Interna korekcija zbog preanalitičkih faktora
if room_temp and delay_over_8h:
    percent_bias *= 1.60   # +100%
elif room_temp or delay_over_8h:
    percent_bias *= 1.40   # +60%

# 95% CI
SE = abs(percent_bias) * math.sqrt(1 - R2)
ci_low = percent_bias - 1.96 * SE
ci_high = percent_bias + 1.96 * SE

# =====================
# KOREKCIJA VREDNOSTI
# =====================
corrected_value = measured_value / (1 + percent_bias / 100)
corrected_ci_low = measured_value / (1 + ci_high / 100)
corrected_ci_high = measured_value / (1 + ci_low / 100)

# =====================
# PRIKAZ REZULTATA
# =====================
st.markdown("### Rezultati")
st.write(f"**% bias:** {percent_bias:.2f}")
st.write(f"**95% CI % bias:** [{ci_low:.2f}, {ci_high:.2f}]")
st.write(f"**Korigovana vrednost {param}:** {corrected_value:.2f}")
st.write(
    f"**95% CI korigovane vrednosti:** "
    f"[{corrected_ci_low:.2f}, {corrected_ci_high:.2f}]"
)

# =====================
# GRAF 1: % bias vs Hb
# =====================
x_range = np.linspace(0, 10, 200)
bias_range = a * x_range + b

if room_temp and delay_over_8h:
    bias_range *= 1.60
elif room_temp or delay_over_8h:
    bias_range *= 1.40

ci_lower_range = bias_range - 1.96 * abs(bias_range) * math.sqrt(1 - R2)
ci_upper_range = bias_range + 1.96 * abs(bias_range) * math.sqrt(1 - R2)

fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(x_range, bias_range, label="% bias")
ax1.fill_between(x_range, ci_lower_range, ci_upper_range, alpha=0.3, label="95% CI")
ax1.scatter(x, percent_bias, color="red", s=50, label="Unos")
ax1.set_xlabel("Hb koncentracija (g/L)")
ax1.set_ylabel("% bias")
ax1.set_title(f"{param} – % bias vs Hb")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# =====================
# GRAF 2: Korigovana vs Izmerena vrednost
# =====================
measured_range = np.linspace(
    max(0.01, 0.5 * measured_value),
    1.5 * measured_value + 0.01,
    100
)

corrected_range = measured_range / (1 + percent_bias / 100)
corrected_ci_lower = measured_range / (1 + ci_high / 100)
corrected_ci_upper = measured_range / (1 + ci_low / 100)

fig2, ax2 = plt.subplots(figsize=(6, 6))
ax2.plot(measured_range, corrected_range, label="Korigovana vrednost")
ax2.fill_between(
    measured_range,
    corrected_ci_lower,
    corrected_ci_upper,
    alpha=0.3,
    label="95% CI"
)
ax2.scatter(measured_value, corrected_value, color="red", s=50, label="Unos")
ax2.set_xlabel("Izmerena vrednost")
ax2.set_ylabel("Korigovana vrednost")
ax2.set_title(f"{param} – Korigovana vs Izmerena vrednost")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)
