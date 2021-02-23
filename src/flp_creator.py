number_of_input_bits = 1

mux_x = 0.002   # in m
mux_y = 0.0012  # in m

for i in range(number_of_input_bits):
    positionx = 0.0 + mux_x * i

    line = "Mux1" + str(i) + "\t" + str(mux_x) + "\t" + str(mux_y) + "\t"
    line += str(round(positionx, 8)) + "\t"
    positiony = 0.0
    line += str(round(positiony, 8))
    print(line)

    line = "Mux0" + str(i) + "\t" + str(mux_x) + "\t" + str(mux_y) + "\t"
    line += str(round(positionx, 8)) + "\t"
    positiony = mux_y
    line += str(round(positiony, 8))
    print(line)

print("flip\t0.01\t0.013\t" + str(number_of_input_bits * mux_x) + "\t0.0")
