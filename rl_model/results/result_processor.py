def process_heuristic_results():
    import pickle
    results = {'improved': {0: 0, 1: 0, 2: 0, 3: 0}, 'called': {0: 0, 1: 0, 2: 0, 3: 0}}
    for i in range(10):
        file_io = open("rd_heuristic_report"+str(i)+".pkl", 'rb')
        dict_ = pickle.load(file_io)
        for i in range(4):
            results["improved"][i] += dict_["improved"][i]
            results["called"][i] += dict_["called"][i]
        file_io.close()
    results ["percentage"] = dict(zip(range(4),["%.3f"%(100*results["improved"][i]/results["called"][i])for i in range(4) ]))
    for i in range(4):
        print("LLH %i"%(i+1), end=" & ")
        print(results["called"][i], end=" & ")
        print(results["improved"][i], end=" & ")
        print(results["percentage"][i], end="\\\\\n")
    print(results)

def process_runtimes_rd():
    import pandas as pd
    import numpy as np
    arr = np.empty((0,5))

    for i in range(10):
        dataframe = pd.read_csv("rd_runtime" + str(i) + ".csv")
        last_row = dataframe.tail(1).as_matrix()
        arr = np.vstack((arr, last_row))
    print(list(dataframe))
    arr = arr[arr[:,1].argsort()]
    best = arr[0]
    mean = arr.mean(axis=0)
    std = arr.var(axis=0)**.5
    for i in range(1,5):
        print("& %.2f & %.2f & %.2f" % (best[i], mean[i], std[i]) , end=" ")
    print("\\\\")

def process_runtimes_ga():
    import pandas as pd
    import numpy as np
    arr = np.empty((0,5))

    for i in range(10):
        dataframe = pd.read_csv("../ga_results/ga_results" + str(i) + ".csv")[1:]
        dataframe = dataframe.sort_values(by=["duration"])
        print(dataframe.head(1))
        last_row = dataframe.head(1).as_matrix()
        arr = np.vstack((arr, last_row))
    print(list(dataframe))
    print(arr[:,1].argsort())
    arr = arr[arr[:,1].argsort()]
    best = arr[0]
    mean = arr.mean(axis=0)
    std = arr.var(axis=0)**.5
    for i in range(1,5):
        print("& %.2f & %.2f & %.2f" % (best[i], mean[i], std[i]) , end=" ")
    print("\\\\")

def runtime_ga_best_so_far():
    import numpy as np
    import matplotlib.pyplot as plt
    filepath = "../ga_results/ga_results8.csv"
    a = np.genfromtxt(filepath, delimiter=",")
    file_io = open(filepath)
    print(file_io.readline())
    file_io.close()
    a = a[2:, 1:]
    best_so_far_array = np.empty((0,4))
    best_row_so_far = a[0]
    for i in range(a.shape[0]):
        if a[i][0] < best_row_so_far[0]:
            best_row_so_far = a[i]
        best_so_far_array = np.vstack((best_so_far_array, best_row_so_far))
    return best_so_far_array

def generate_objective_function_plot():
    import matplotlib.pyplot as plt
    import numpy as np
    ga_data = runtime_ga_best_so_far()
    filepath = "rd_runtime1.csv"
    rd_data = np.genfromtxt(filepath, delimiter=",")[2:,1:]
    print("duration,mean_speed,time_loss,waiting_time")
    plt.plot(ga_data[:,3], "-", linewidth=2, color="r",label="Genetic Algorithm")
    plt.plot(rd_data[:,3], "--", linewidth=2, color="g",label="Random Descent")
    plt.xlabel("Iteration")
    plt.ylabel("Mean Waiting Time $seconds$")
    plt.legend()
    plt.grid(linestyle=":")
    plt.show()
    
generate_objective_function_plot()