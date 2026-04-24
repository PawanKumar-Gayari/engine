from apps.generator.generator import generate_article
from apps.plugins.base.registry import registry
from apps.plugins.seo.seo_plugin import load_seo_plugins


class Pipeline:

    def __init__(self, state):
        self.state = state
        self.max_attempts = 3   # 🔥 retry control

    def run(self):

        # 🔥 load plugins once
        load_seo_plugins()

        for attempt in range(self.max_attempts):

            self.state.log(f"Attempt {attempt + 1}")

            self.generate()
            self.verify()

            # ✅ PASS CONDITION
            if self.state.score >= 80:
                self.state.log("Article passed verification")
                break

            # 🔁 FAIL → rewrite
            self.state.log("Article failed, rewriting...")
            self.rewrite()

        # 🔥 APPLY SEO (after final content ready)
        self.apply_plugins()

        return self.state

    # 🔥 STEP 1: GENERATE
    def generate(self):
        self.state.log("Generating article")

        article = generate_article(self.state.keyword)
        self.state.article = article

    # 🔍 STEP 2: VERIFY
    def verify(self):
        self.state.log("Verifying article")

        content = self.state.article["content"]

        if len(content) < 100:
            self.state.score = 50
            self.state.log("Content too short ❌")
        else:
            self.state.score = 90
            self.state.log("Content verified ✅")

    # 🔁 STEP 3: REWRITE
    def rewrite(self):
        self.state.log("Rewriting article")

        improved_content = (
            self.state.article["content"] +
            "\n\nAdditional details added."
        )

        self.state.article["content"] = improved_content

    # 🔥 STEP 4: APPLY PLUGINS (SEO etc.)
    def apply_plugins(self):
        self.state.log("Applying SEO plugins")

        self.state.article = registry.apply_all(self.state.article)

        self.state.log("SEO plugins applied")