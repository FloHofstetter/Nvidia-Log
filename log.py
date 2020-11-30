import signal
from nvidia_logger import smi_logger

from datetime import datetime
from time import sleep


class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

def main():
    datetime_now = datetime.now()
    date_now = datetime_now.strftime("%d.%m.%Y")
    time_now = datetime_now.strftime("%H-%M-%S")
    timstamp_name = f"{date_now}_{time_now}"

    first_run: bool = True

    killer = GracefulKiller()
    while not killer.kill_now:
        gpu_dicts = smi_logger.get_gpu_dicts()
        for gpu_dict in gpu_dicts:
            with open(f"{gpu_dict['id']}_" + timstamp_name + ".csv", "a") as csvfile:
                smi_logger.gpu_dicts_to_csv(gpu_dict, csvfile, first_run)
        first_run = False
        sleep(1)

    print("\nLogging terminated...")

if __name__ == "__main__":
    main()