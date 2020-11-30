from logg_plotter import smi_plotter
import sys

LOGFILE = "GPU-a40c5b91-47af-e186-4c54-9563ffb2a8a330.11.2020_19:41:44"
PLOTFILE = "plot"


def main():
    logfiles = sys.argv[1:]
    gpu_log_dicts = []

    for logfile in logfiles:
        with open(logfile, "r") as csvfile:
            gpu_log_dicts.append(smi_plotter.file_to_gpu_dict(csvfile))

    with open("GPUs" + logfile[5:-4] + ".png", "wb") as plotfile:
        smi_plotter.plot_gpu_stats(gpu_log_dicts, plotfile)


if __name__ == "__main__":
    main()
