import logging
import threading
import lokihandler
import socketserver
import re
import os
import queue

LISTEN_PORT = os.getenv("LISTEN_PORT", "514")
CONSOLE_LOG = os.getenv("DISABLE_CONSOLE_LOG") is None
MESSAGE_REGEX = os.getenv("MESSAGE_REGEX", None)
LOKI_URL = os.getenv("LOKI_URL", None)

def create_logger():
    logger = logging.getLogger("syslog-to-loki")
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

queue = queue.Queue(-1)

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.getLogger().debug(f"Received packet")
        data = bytes.decode(self.request[0].strip())
        queue.put(data, block = True)

class QueueProcessor(threading.Thread):
    def __init__(self, queue, logger):
        threading.Thread.__init__(self)
        self.queue = queue
        self.logger = logger
        self.sys_log_format_regex = re.compile("\<(?P<priority>\d+)\>(?P<version>\d+) (?P<time>\S*) (?P<host>\S*) (?P<application>\S*) (?P<process_id>\S*) (?P<message_id>\S*) ((?P<structure_data>\[.*\])+|-) (?P<msg>.*)")        
        self.custom_regex = None
        if not MESSAGE_REGEX is None:
            self.custom_regex = re.compile(MESSAGE_REGEX)
        self.do_stop = False

    def stop(self):
        self.do_stop = True

    def run(self):
        while not self.do_stop:
            try:
                data = self.queue.get(block=True, timeout=1)
                if data is None:
                    continue

                self.queue.task_done()

                match = self.sys_log_format_regex.match(data)

                tag_dict = match.groupdict()
                msg = tag_dict["msg"]
                del tag_dict["msg"]

                if not self.custom_regex is None:
                    msg_match = self.custom_regex.match(msg)
                    if not msg_match is None:
                        custom_tag_dict = msg_match.groupdict()
                        tag_dict.update(custom_tag_dict)
                    else:
                        self.logger.error("MESSAGE_REGEX does not match")
                
                self.logger.info(
                    data,
                    extra={"tags" : tag_dict}
                )
            except:
                pass

def main():
    if LOKI_URL is None:
        logging.getLogger().error(f"LOKI_URL not defined")
        return

    logger = create_logger()

    ip = "0.0.0.0"
    port = int(LISTEN_PORT)

    try:
        logging.getLogger().debug(f"Create queue processor")
        queue_processor = QueueProcessor(queue, logger)
        queue_processor.start()

        logging.getLogger().debug(f"Create UDP server")
        server = socketserver.UDPServer((ip, port), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise

    except KeyboardInterrupt:
        server.shutdown()
        queue.join()
        queue_processor.stop()
        queue_processor.join()

if __name__ == "__main__":
    main()
