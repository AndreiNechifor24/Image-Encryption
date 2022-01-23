class EncryptionExceptions(Exception):
    """ Defines custom exceptions for encryption processes """

    method_argument = None
    reason = None
    message = None

    def __init__(self, method_argument, reason, message="Current argument value: %s has not been valid. \n Reason: %s"):
        self.method_argument = method_argument
        self.message = message
        self.reason = reason
        super().__init__(self.message % (str(method_argument), reason))


class BadArgumentException(EncryptionExceptions):
    """
        Raised when argument is null or in invalid format.

        @Attributes:
            -> @argument - Method given argument
            -> @reason - Invalid argument reason
            -> @message - Explain why the current argument is not valid.
    """

    def __init__(self, method_argument, reason):
        super().__init__(method_argument, reason)


class ArgumentOutOfRangeException(EncryptionExceptions):
    """
        Raised when argument is not in the expected range

        @Attributes:
            -> @argument - Method given argument
            -> @reason - Invalid argument reason
            -> @message - Explain why the current argument is not valid.
    """

    def __init__(self, method_argument, reason):
        super().__init__(method_argument, reason)







