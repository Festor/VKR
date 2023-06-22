import random
import string
import logging
import subprocess
import os
from tqdm import tqdm
from datetime import datetime

MAX_ITERS = 5
# DINAMORIO_PATH = "C:/D/Apps/2023.06_EreminFuzzingBackdoors/DynamoRIO-Windows-9.93.19503/bin64"
DINAMORIO_PATH = "C:\\ProjectA\\DynamoRIO-Windows-9.0.1\\bin64"
# DINAMORIO_PATH = "C:\D\Apps\2023.06_EreminFuzzingBackdoors\DynamoRIO-Windows-9.93.19503\bin64"
MAX_CASE_LENGTH = 6
TARGET_NAME = "C:\\ProjectA\\Harness\\debug\\Harness.exe"
TMP_LOG_DIR = "./drcov_tmp"
COV_LOG_DIR = "./drcov"
fuzz_alphabet = string.ascii_lowercase # алфавит фаззинга

logging.basicConfig(level=logging.INFO,
                    filename="fuzzig_log.log",
                    filemode="w",
                    format="%(asctime)s %(message)s")

def fuzzing():
    logging.info("Start fuzzing")
    for i in tqdm(range(MAX_ITERS)):
        logging.info(f"Case {i}")
        
        # задать случайную длину строки-аргумента
        case_length = random.randint(1, MAX_CASE_LENGTH)
        if i == 0: # если запуск первый - то параметр пустой
            arg = ''
        else:
            arg = ''.join(random.choice(fuzz_alphabet) for i in range(case_length))
        logging.info(f"arg={arg}")
        
        # запуск оснастки с тестируемым приложением в DinamoRIO и сбор покрытия
        args = [f"{DINAMORIO_PATH}\\drrun.exe",
                "-t", "drcov", # утилита
                "-dump_text", # формат записи
                "-logdir", TMP_LOG_DIR, # каталог для сохранения логов покрытия
                "--", # разделитель
                TARGET_NAME, arg # запускаемая программа
                ]
        # process = subprocess.Popen(args, stdout=subprocess.PIPE)
        # terminal_output = process.communicate()
        terminal_output = subprocess.run(args, capture_output=True, text=True)
        logging.info(f"stdout={terminal_output.stdout.strip()}")
        logging.info(f"stderr={terminal_output.stderr.strip()}")
        
        # имена полученных файлов покрытия
        generated_files = []    
        for path in os.listdir(TMP_LOG_DIR):
            if os.path.isfile(os.path.join(TMP_LOG_DIR, path)):
                generated_files.append(path)
                
        for old_filename in generated_files:
            datetime_now = datetime.now()
            # сгенерировать новое имя для файлов покрытия
            newFilename = (datetime_now.strftime("%Y-%m-%d %H_%M_%S.")
                + "{:06d}".format(datetime_now.microsecond)[:3] + " "
                + old_filename)
            # переместить из временного каталога в финальный
            os.rename(os.path.join(TMP_LOG_DIR, old_filename),
                    os.path.join(COV_LOG_DIR, newFilename))
            # если файл покрытия относится к исследуемому модулю - записать в лог
            if "TestApp.exe" in newFilename:
                logging.info(f"covfile={newFilename}")
        
if __name__ == "__main__":
    fuzzing()
