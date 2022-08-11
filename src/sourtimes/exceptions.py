"""
Sourtimes exception classes.

"""

class SourtimesException(Exception):
    """
    The base Sourtimes Exception that all other exception classes extend.
    
    """

class ChannelException(SourtimesException):
    """
    Raised when the called channel is not available.
    
    """
    def __init__(self):
        super().__init__(
            "Provided channel does not exist."
        )