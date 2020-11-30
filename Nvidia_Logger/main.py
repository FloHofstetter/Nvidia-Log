from typing import Tuple, Generator, TextIO, Iterable
import nvsmi
import csv
from datetime import datetime
from time import sleep


def get_gpu_dicts() -> Tuple[dict]:
    """
    Return Tuple with dicts of all information about available GPUs.
    """
    handle: Generator
    handle = nvsmi.get_gpus()
    gpu_dicts = []
    i: nvsmi.GPU
    for i in handle:
        gpu_dicts: dict
        gpu_dicts.append(i.__dict__)
    return gpu_dicts


def gpu_dicts_to_csv(gpu_dict: dict, filehandle: TextIO, header: bool) -> None:
    """
    Take dict of GPU information, date, time. Create CSV logfile with name of
    GPUs uuid and datetime stamp.
    """
    fieldnames: Iterable
    fieldnames = gpu_dict.keys()
    logwriter: csv.DictWriter
    logwriter = csv.DictWriter(filehandle, fieldnames)
    if header:
        logwriter.writeheader()
    logwriter.writerow(gpu_dict)


def main() -> None:
    datetime_now = datetime.now()
    date_now = datetime_now.strftime("%d.%m.%Y")
    time_now = datetime_now.strftime("%H:%M:%S")
    first_run: bool = True
    while True:
        gpu_dicts = get_gpu_dicts()
        for gpu_dict in gpu_dicts:
            with open(f"{gpu_dict['uuid']}_{date_now}_{time_now}.csv", "a") as csvfile:
                gpu_dicts_to_csv(gpu_dict, csvfile, first_run)
        first_run = False
        sleep(1)


if __name__ == "__main__":
    main()
