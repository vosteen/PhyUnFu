import matplotlib.pyplot as plt
import numpy as np
import os

path_result_dir = "../res/"
plot_path = "../fig/"
cut_off_temperature = 800  # in Kelvin

# find all files in directory and write names to list; extract used metadata
res_file_list = []
temperature_list = []
name_list = []
mux_power_list = []

for file in os.listdir(path_result_dir):
    if file.endswith(".txt"):
        res_file_list.append(file)
        name_list.append(file.split("_")[0] + "_" + file.split("_")[1])
        temperature_list.append(float(file.split("_")[2]))
        mux_power_list.append(file.split("_")[3][:-4])
temperature_list = [str(int(x)) for x in np.unique(sorted(temperature_list))]
name_list = [x for x in np.unique(sorted(name_list))]
mux_power_list = [x for x in np.unique(sorted(mux_power_list))]

print(name_list)
print(temperature_list)
print(mux_power_list)

results = np.zeros([len(name_list), len(temperature_list), len(mux_power_list)])

for res in res_file_list:
    # get max temp and save in 3D-list(name, ambient temp, mux-power) results
    file = open(path_result_dir + res)
    content = file.readlines()
    if content[0][0:4] == "Unit":
        temp = []
        for line in content[1:]:
            if line[0:5] != "iface":
                line_seperated = line.split("\t")
                temp.append(line_seperated[-1])
            else:
                break
        hottest_mux_temp = max(temp)

        name_index = name_list.index(res.split("_")[0] + "_" + res.split("_")[1])
        temperature_index = temperature_list.index(res.split("_")[2])
        mux_power_index = mux_power_list.index(res.split("_")[3][:-4])

        results[name_index][temperature_index][mux_power_index] = hottest_mux_temp
    else:
        raise Exception("faulty result in " + res)

for i in range(len(results)):
    for j in range(len(results[0])):
        for k in range(len(results[0][0])):
            if results[i][j][k] < 1 or results[i][j][k] > cut_off_temperature:
                results[i][j][k] = None
            if abs(results[i][j][k]-285) < 0.01 or abs(results[i][j][k]-335) < 0.01 or abs(results[i][j][k]-385) < 0.01:
                results[i][j][k] = None

mux_power_list = [int(x) for x in mux_power_list]

for i in range(len(name_list)):
    if name_list[i] == "a_001":
        name_list[i] = "an Arbiter PUF with 1 bit input"
    if name_list[i] == "a_032":
        name_list[i] = "an Arbiter PUF with 32 bits input"
    if name_list[i] == "a_064":
        name_list[i] = "an Arbiter PUF with 64 bits input"
    if name_list[i] == "c_002":
        name_list[i] = "an circular PUF with 2 bits input"

# plot results
for name_index in range(len(name_list)):
    plt.clf()
    data = results[name_index]
    plt.title('Temperature in Kelvin for ' + name_list[name_index])
    show_every_nth_x = 19  # show every nth label on horizontal axis
    plt.xticks(range(0, len(mux_power_list), show_every_nth_x), mux_power_list[::show_every_nth_x])
    plt.xlabel('Power/μW')
    show_every_nth_y = 15  # show every nth label on vertical axis
    plt.yticks(range(0, len(temperature_list), show_every_nth_y), temperature_list[::show_every_nth_y])
    plt.ylabel('ambient Temperature/K')
    plt.colorbar(plt.imshow(data, origin='lower', cmap='inferno', aspect='auto', interpolation='none'))
    plt.savefig(plot_path + name_list[name_index] + ".svg")
    plt.savefig(plot_path + name_list[name_index] + ".png")
    plt.show()
