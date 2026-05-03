import time


class PipelineState:
    """
    🧠 AI Pipeline State Manager (v2)

    Features:
    - context management
    - article tracking
    - scoring layers
    - plugin metrics
    - execution logs
    """

    def __init__(self, keyword):

        # =========================
        # 🔑 INPUT
        # =========================
        self.keyword = keyword
        self.intent = "informational"
        self.context = {}

        # =========================
        # 📝 ARTICLE
        # =========================
        self.article = None
        self.original_article = None

        # =========================
        # 📊 SCORING
        # =========================
        self.score = 0
        self.final_score = 0

        # =========================
        # 🔁 HISTORY
        # =========================
        self.history = []

        # =========================
        # 🔌 PLUGIN DATA
        # =========================
        self.plugin_metrics = []
        self.plugin_summary = {}

        # =========================
        # ⏱ EXECUTION
        # =========================
        self.start_time = time.time()
        self.execution_time = 0

        # =========================
        # 🧾 LOGGING
        # =========================
        self.logs = []

    # =========================
    # 🧾 LOG SYSTEM
    # =========================
    def log(self, message):

        timestamp = time.strftime("%H:%M:%S")

        log_entry = f"[{timestamp}] {message}"

        self.logs.append(log_entry)

    # =========================
    # 📦 SET ARTICLE
    # =========================
    def set_article(self, article):

        if not self.original_article:
            self.original_article = article

        self.article = article

    # =========================
    # 📊 UPDATE SCORE
    # =========================
    def update_score(self, score):
        self.score = score

    # =========================
    # 🧠 FINALIZE
    # =========================
    def finalize(self):

        self.execution_time = round(time.time() - self.start_time, 2)

    # =========================
    # 📊 SUMMARY
    # =========================
    def summary(self):

        return {
            "keyword": self.keyword,
            "score": self.score,
            "final_score": self.final_score,
            "execution_time": self.execution_time,
            "attempts": len(self.history),
        }

    # =========================
    # 🔍 DEBUG VIEW
    # =========================
    def debug(self):

        return {
            "keyword": self.keyword,
            "logs": self.logs,
            "history": self.history,
            "plugin_metrics": self.plugin_metrics,
            "context": self.context,
        }