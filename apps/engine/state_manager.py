class PipelineState:
    def __init__(self, keyword):
        self.keyword = keyword
        self.article = None
        self.score = 0
        self.logs = []

    def log(self, message):
        self.logs.append(message)