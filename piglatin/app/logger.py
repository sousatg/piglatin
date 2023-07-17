import logging
import logging.config

logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)

logger.addHandler(c_handler)
