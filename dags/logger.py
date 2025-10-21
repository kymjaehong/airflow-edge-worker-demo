import logging
import sys
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "loggerName": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }
        return json.dumps(log_data, ensure_ascii=False)


def set_logger(level=logging.INFO):
    # 기존 핸들러 제거
    for handler in logging.root.handlers[:]:  # 얕은 복사를 통해 독립된 객체 순회, 참조는 같음
        print("root handler: ", handler)
        logging.root.removeHandler(handler)

    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 파일 핸들러
    file_handler = logging.FileHandler("logs/mylogging.log", encoding='utf-8')
    file_handler.setFormatter(JsonFormatter())
    file_handler.setLevel(level)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # 루트 로거 핸들러
    logging.root.setLevel(level)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)

def get_logger(name=None, level=logging.INFO):
    if not logging.root.handlers:
        print("No Handlers !!!!!")
        set_logger()

    return logging.getLogger(name)


# if __name__ == "__main__":
#     from pathlib import Path
#     print("python execution location: ", Path.home())
    
#     logging.root.handlers = []

#     log = get_logger('auto set')
#     log.info("auto set handler !!!!!!!!")


#     logging.root.handlers = []
#     set_logger()
#     log = get_logger('command set')
#     log.info("logging afet set_logger !!!!!!!")