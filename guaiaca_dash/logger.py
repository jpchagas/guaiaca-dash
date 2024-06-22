import logging

class ColoredLogger:
    COLORS = {
        logging.DEBUG: "\033[94m",   # Blue
        logging.INFO: "\033[92m",    # Green
        logging.WARNING: "\033[93m", # Yellow
        logging.ERROR: "\033[91m",   # Red
        logging.CRITICAL: "\033[41m" # Red background
    }

    RESET = "\033[0m"

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Change as needed

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_colored_formatter())
        self.logger.addHandler(console_handler)

        # Create a FileHandler for file output if log_file is provided
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)


    def _get_colored_formatter(self):
        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                log_level_color = ColoredLogger.COLORS.get(record.levelno, ColoredLogger.RESET)
                log_msg = super().format(record)
                return f"{log_level_color}{log_msg}{ColoredLogger.RESET}"

        return ColoredFormatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)