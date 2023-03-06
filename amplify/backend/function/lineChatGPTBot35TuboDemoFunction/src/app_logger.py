import logging

logger = None


def init(name='gpt3.chatbot'):
    """
    Initialize the logger object

    Parameters:
        name (str): name of the logger

    Returns:
        logger object if it exists else create and return logger
    """
    global logger
    if logger is None:
        # Create logger object with given name and set logging level to INFO
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
    else:
        return logger
