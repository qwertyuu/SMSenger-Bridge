class PipelineHandler:
    def __init__(self, callbacks=[]):
        self.callbacks = callbacks

    def send_callback(self, data):
        for callback in self.callbacks:
            if not data:
                break
            data = callback(data)
