class BrowserError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UnauthenticatedUserError(BrowserError):
    pass

class RequestWithoutDefaultParamsError(BrowserError):
    pass

class UninitializedWorkerError(BrowserError):
    pass