def create_ptrace(filename, bit, mux_power, use_flip):
    number_of_input_bits = bit
    number_of_power_entries = 5
    mux_power = "%08d" % mux_power  # in μW
    mux_power = mux_power[:5] + "." + mux_power[5:]

    flip_power = 0.01  # in mW

    ptrace_file = open(filename, "w")
    first_line = ""
    temp = ["Mux0" + str(i) + "  Mux1" + str(i) + "  " for i in range(number_of_input_bits)]
    for entry in temp:
        first_line += entry
    if use_flip:
        first_line += "flip"
    ptrace_file.write(first_line + "\n")

    for i in range(number_of_power_entries):
        line = ""
        temp = [str(mux_power) + " " for _ in range(number_of_input_bits * 2)]
        for entry in temp:
            line += entry
        if use_flip:
            line += str(flip_power)
        ptrace_file.write(line + "\n")
    ptrace_file.close()
