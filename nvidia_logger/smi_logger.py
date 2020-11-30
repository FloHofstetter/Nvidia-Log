from typing import Tuple, Generator, TextIO, Iterable, List
import nvsmi
import csv
from datetime import datetime
from time import sleep


def get_gpu_dicts() -> List[dict]:
    """
    Return Tuple with dicts of all information about available GPUs.
    """
    gpus: Generator
    gpus = nvsmi.get_gpus()
    gpu_dicts: List[dict] = []
    gpu: nvsmi.GPU
    datetime_now: datetime = datetime.now()
    date_now: str = datetime_now.strftime("%d.%m.%Y")
    time_now: str = datetime_now.strftime("%H:%M:%S")
    for gpu in gpus:
        gpu_dict: dict = gpu.__dict__
        gpu_dict["date"] = date_now
        gpu_dict["time"] = time_now
        gpu_dicts.append(gpu_dict)
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
    pass


if __name__ == "__main__":
    main()
