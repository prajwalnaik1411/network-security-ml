import sys  # Used to get error details (traceback info)
from networksecurity.logging import logger  # Custom logging (better than print)


class NetworkSecurityException(Exception):  # Custom exception class (inherits from Exception)
    def __init__(self, error_message, error_details: sys):
                                                        # error_message → actual error (e.g., division by zero)
                                                        # error_details → sys module (used to extract traceback)

        self.error_message = error_message              # Store original error message

        _, _, exc_tb = error_details.exc_info()     # (type, value, traceback)
                                                    # _ → ignore type and value
                                                    # exc_tb → traceback object (contains line number and file info)

        self.lineno = exc_tb.tb_lineno  # Line number where error occurred
        self.file_name = exc_tb.tb_frame.f_code.co_filename  # File where error occurred

    def __str__(self):
        # Custom message when exception is printed
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )


if __name__ == "__main__":  # Run only when executed directly
    try:
        logger.logging.info("Enter the try block")

        a = 1 / 0  # Raises ZeroDivisionError
        print("This will not be printed", a)

    except Exception as e:
        # Wrap original error into custom exception with file & line info
        raise NetworkSecurityException(e, sys)