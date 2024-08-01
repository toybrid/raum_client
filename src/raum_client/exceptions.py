class RaumServerError(Exception):
    def __init__(self, message):
        """
        Initialize the RaumServerError instance with a custom error message.

        Parameters:
        message (str): The error message to be associated with the exception.

        Returns:
        None
        """
        super().__init__(message)


class RaumAuthenticationError(Exception):
    def __init__(self, message):
        """
        Initialize the RaumAuthenticationError instance with a custom error message.

        Parameters:
        message (str): The error message to be associated with the exception.

        Returns:
        None
        """
        super().__init__(message)