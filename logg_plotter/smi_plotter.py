import csv
from typing import List, TextIO, BinaryIO
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime


def file_to_gpu_dict(filedescriptor: TextIO) -> dict:
    """
    Get file of GPU logs. Return a dict of GPU logs.
    """
    gpu_dict: dict = dict()
    gpu_util: List[float] = []
    mem_util: List[float] = []
    mem_used: List[float] = []
    temperature: List[float] = []

    csvreader: csv.DictReader
    csvreader = csv.DictReader(filedescriptor)

    for row in csvreader:
        gpu_util.append(float(row["gpu_util"]))
        mem_util.append(float(row["mem_util"]))
        mem_used.append(float(row["mem_used"]))
        temperature.append(float(row["temperature"]))

    gpu_dict["gpu_util"] = gpu_util
    gpu_dict["mem_util"] = mem_util
    gpu_dict["mem_used"] = mem_used
    gpu_dict["temperature"] = temperature
    gpu_dict["id"] = int(row["id"])
    gpu_dict["uuid"] = row["uuid"]
    gpu_dict["mem_total"] = float(row["mem_total"])
    gpu_dict["display_mode"] = row["display_mode"]
    gpu_dict["display_active"] = row["display_active"]
    return gpu_dict


def plot_gpu_stats(gpu_dicts: List[dict], filedescriptor: BinaryIO):
    """
    Get List of dicts with GPU log information.
    Safe plot GPU log information to png image.
    """

    mpl.rcParams.update({"font.size": 22})

    fig: plt.Figure
    ax0: plt.Axes
    ax1: plt.Axes
    ax2: plt.Axes
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=[30, 15])
    ax0 = fig.add_subplot(axs[0, 0])  # GPU utilisation
    ax1 = fig.add_subplot(axs[0, 1])  # GPU Memory usage relative
    ax2 = fig.add_subplot(axs[1, 0])  # GPU Memory usage absolute
    ax3 = fig.add_subplot(axs[1, 1])  # GPU Temperature

    # Axis 0 - GPU utilisation
    min_util: List[float] = []
    max_util: List[float] = []
    avg_util: List[float] = []
    for gpu_dict in gpu_dicts:
        ax0.plot(gpu_dict["gpu_util"], label=f"GPU {gpu_dict['id']}")
        min_util.append(min(gpu_dict["gpu_util"]))
        max_util.append(max(gpu_dict["gpu_util"]))
        avg_util.append(sum(gpu_dict["gpu_util"]) / len(gpu_dict["gpu_util"]))

    # ax0.set_xlim(0.0, 100.0)
    ax0.set_ylim(0.0, 50.0)

    ax0.set_title(
        f"All GPUs utilisation\nmin {sum(min_util):.2f} | max: {sum(max_util):.2f}"
        + " | avg: {sum(avg_util):.2f}"
    )
    ax0.set_xlabel("Time in s")
    ax0.set_ylabel("GPU utilisation in %")

    ax0.grid(True, which="major")
    ax0.grid(True, which="minor", axis="x")
    ax0.minorticks_on()
    ax0.legend()

    # Axis 1 - GPU Memory usage relative
    min_mem_util: List[float] = []
    max_mem_util: List[float] = []
    avg_mem_util: List[float] = []
    for gpu_dict in gpu_dicts:
        ax1.plot(gpu_dict["mem_util"], label=f"GPU {gpu_dict['id']}")
        min_mem_util.append(min(gpu_dict["mem_util"]))
        max_mem_util.append(max(gpu_dict["mem_util"]))
        avg_mem_util.append(sum(gpu_dict["mem_util"]) / len(gpu_dict["mem_util"]))
    # ax0.set_xlim(0.0, 100.0)
    ax1.set_ylim(0.0, 100.0)

    ax1.set_title(
        f"All GPUs Memory usage relative\nmin {sum(min_mem_util):.2f} | "
        + f"max: {sum(max_mem_util):.2f} | avg: {sum(avg_mem_util):.2f}"
    )
    ax1.set_xlabel("Time in s")
    ax1.set_ylabel("GPU Memory usage in %")

    ax1.grid(True, which="major")
    ax1.grid(True, which="minor", axis="x")
    ax1.minorticks_on()

    ax1.legend()

    # Axis 2 - GPU Memory usage absolute
    min_mem_used: List[float] = []
    max_mem_used: List[float] = []
    avg_mem_used: List[float] = []
    for gpu_dict in gpu_dicts:
        ax2.plot(gpu_dict["mem_used"], label=f"GPU {gpu_dict['id']}")
        min_mem_used.append(min(gpu_dict["mem_used"]))
        max_mem_used.append(max(gpu_dict["mem_used"]))
        avg_mem_used.append(sum(gpu_dict["mem_used"]) / len(gpu_dict["mem_used"]))

    # ax0.set_xlim(0.0, 100.0)
    ax2.set_ylim(bottom=0.0)

    ax2.set_title(
        f"All GPUs Memory usage absolute\nmin {sum(min_mem_used):.2f} | "
        + f"max: {sum(max_mem_used):.2f} | avg: {sum(avg_mem_used):.2f}"
    )
    ax2.set_xlabel("Time in s")
    ax2.set_ylabel("GPU Memory usage in MB")

    ax2.grid(True, which="major")
    ax2.grid(True, which="minor", axis="x")
    ax2.minorticks_on()

    ax2.legend()

    # Axis 3 - GPU Temperature
    min_temperature: List[float] = []
    max_temperature: List[float] = []
    avg_temperature: List[float] = []
    for gpu_dict in gpu_dicts:
        ax3.plot(gpu_dict["temperature"], label=f"GPU {gpu_dict['id']}")
        min_temperature.append(min(gpu_dict["temperature"]))
        max_temperature.append(max(gpu_dict["temperature"]))
        avg_temperature.append(
            sum(gpu_dict["temperature"]) / len(gpu_dict["temperature"])
        )
    # ax0.set_xlim(0.0, 100.0)
    ax3.set_ylim(0.0, 50.0)

    ax3.set_title(
        f"All GPUs Temperature\nmin {sum(min_temperature):.2f} | "
        + f"max: {sum(max_temperature):.2f} | avg: {sum(avg_temperature):.2f}"
    )
    ax3.set_xlabel("Time in s")
    ax3.set_ylabel("GPU Temperature in °C")

    ax3.grid(True, which="major")
    ax3.grid(True, which="minor", axis="x")
    ax3.minorticks_on()

    ax3.legend()

    left = None  # 0.125  # the left side of the subplots of the figure
    right = None  # 0.9    # the right side of the subplots of the figure
    bottom = None  # 0.1   # the bottom of the subplots of the figure
    top = None  # 0.9      # the top of the subplots of the figure
    # the amount of width reserved for blank space between subplots
    wspace = None
    # 0.2   # the amount of height reserved for white space between subplots
    hspace = 0.5
    fig.subplots_adjust(
        left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace
    )
    plt.savefig(filedescriptor, format="png")


def main():
    pass


if __name__ == "__main__":
    main()
