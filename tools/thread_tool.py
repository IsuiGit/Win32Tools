import threading

class ReturnableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            return f'{type(exc).__name__}: {exc}'

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result

def runThread(func, args=None):
    th = ReturnableThread(target=func, args=args, daemon=True)
    th.start()
    response = th.join()
    return response
