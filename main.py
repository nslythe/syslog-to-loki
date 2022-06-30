import logging
import multiprocessing
import lokihandler
import socketserver
import re
import os

LISTEN_ADDRESS = os.getenv("LISTEN_ADDRESS", "0.0.0.0:514")
CONSOLE_LOG = os.getenv("CONSOLE_LOG", "1")
if CONSOLE_LOG == "1":
    CONSOLE_LOG = True
else:
    CONSOLE_LOG = False
MESSAGE_REGEX = os.getenv("MESSAGE_REGEX", None)
LOKI_URL = os.getenv("LOKI_URL", None)

def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    loki_handler = lokihandler.LokiHandler(
        url=LOKI_URL
    )
    loki_handler.setLevel(logging.INFO)
    logger.addHandler(loki_handler)

    if CONSOLE_LOG:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
    return logger

logger = create_logger()
queue = multiprocessing.Queue(-1)
sys_log_format_regex = re.compile("\<(?P<priority>\d+)\>(?P<version>\d+) (?P<time>\S*) (?P<host>\S*) (?P<application>\S*) (?P<process_id>\S*) (?P<message_id>\S*) ((?P<structure_data>\[.*\])+|-) (?P<msg>.*)")        
custom_regex = None
if not MESSAGE_REGEX is None:
    custom_regex = re.compile(MESSAGE_REGEX)

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        queue.put(data, block = True)

def process_queue(queue):
    stop = False
    while not stop:
        try:
            data = queue.get(block=True)

            match = sys_log_format_regex.match(data)

            tag_dict = match.groupdict()
            msg = tag_dict["msg"]
            del tag_dict["msg"]

            if not custom_regex is None:
                msg_match = custom_regex.match(msg)
                if not msg_match is None:
                    custom_tag_dict = msg_match.groupdict()
                    tag_dict.update(custom_tag_dict)
                else:
                    logger.error("MESSAGE_REGEX does not match")
                
            logger.info(
                data,
                extra={"tags" : tag_dict}
            )
        except ValueError: # Queue closed
            stop = True
        except KeyboardInterrupt:
            stop = True

def main():
    try:
        ip = LISTEN_ADDRESS.split(":")[0]
        try:
            port = LISTEN_ADDRESS.split(":")[1]
        except:
            port = "514"

        p = multiprocessing.Process(target=process_queue, args=(queue,))
        p.start()
        server = socketserver.UDPServer((ip, int(port)), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)

    except (IOError, SystemExit):
        raise

    except KeyboardInterrupt:
        p.join()

if __name__ == "__main__":
    main()
