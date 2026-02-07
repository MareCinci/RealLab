# Linearni bias
# Ako Hb nije unet (x <= 0), koristimo Hb=1 kao osnovu
base_Hb = x if x > 0 else 1.0
percent_bias = a * base_Hb + b

# Preanalitički faktor
if room_temp and delay_over_8h:
    extra_bias = 0.60
elif room_temp or delay_over_8h:
    extra_bias = 0.40
else:
    extra_bias = 0.0

# Primena pravila:
if extra_bias > 0:
    if x <= 0:  # Hb nije unet
        percent_bias *= (1 + extra_bias)  # dodaj pun efekat
    elif x < 1:  # Hb < 1
        percent_bias *= (1 + extra_bias)  # puni efekat
    else:  # Hb >= 1
        percent_bias *= (1 + extra_bias * x)  # proporcionalno Hb
