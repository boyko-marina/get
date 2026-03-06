import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):

    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage, marker='o', linestyle='-', markersize=3)
    plt.title("Зависимость напряжения на входе АЦП от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.ylim(0, max_voltage)
    plt.grid(True)
    plt.show()
