import os
import random
import logging

logger = logging.getLogger(__name__)


class ModelRouter:
    """
    🚀 PRO MODEL ROUTER (MULTI-MODEL ORCHESTRATION)

    Features:
    - stage-based model selection
    - fallback system
    - cost-aware routing
    - dynamic switching
    - provider abstraction
    """

    def __init__(self):

        # 🔥 Available providers
        self.providers = {
            "openrouter": {
                "draft": "meta-llama/llama-3-8b-instruct",
                "rewrite": "mistralai/mistral-7b-instruct",
                "seo": "google/gemma-7b-it",
            },
            "openai": {
                "draft": "gpt-4o-mini",
                "rewrite": "gpt-4o",
                "seo": "gpt-4o",
            },
            "gemini": {
                "draft": "gemini-1.5-flash",
                "rewrite": "gemini-1.5-pro",
                "seo": "gemini-1.5-pro",
            }
        }

        # 🔥 Default provider
        self.default_provider = os.getenv("AI_PROVIDER", "openrouter")

        # 🔥 fallback priority
        self.fallback_order = ["openrouter", "openai", "gemini"]

    # =========================
    # 🚀 MAIN ROUTER
    # =========================
    def get_model(self, stage="draft", prefer=None):
        """
        stage: draft / rewrite / seo
        prefer: optional provider override
        """

        provider = prefer or self.default_provider

        try:
            model = self.providers[provider][stage]

            logger.info(f"[MODEL ROUTER] {stage} → {provider}:{model}")

            return {
                "provider": provider,
                "model": model
            }

        except Exception as e:
            logger.warning(f"[ROUTER ERROR] {provider}:{stage} → {e}")

            return self._fallback(stage)

    # =========================
    # 🔁 FALLBACK SYSTEM
    # =========================
    def _fallback(self, stage):

        for provider in self.fallback_order:
            try:
                model = self.providers[provider][stage]

                logger.warning(f"[FALLBACK] Using {provider}:{model}")

                return {
                    "provider": provider,
                    "model": model
                }

            except:
                continue

        raise Exception(f"No model available for stage: {stage}")

    # =========================
    # 💰 COST-AWARE ROUTING
    # =========================
    def get_cheapest_model(self, stage="draft"):

        # 🔥 prefer lightweight models
        priority = ["openrouter", "gemini", "openai"]

        for provider in priority:
            if provider in self.providers:
                return {
                    "provider": provider,
                    "model": self.providers[provider][stage]
                }

        return self.get_model(stage)

    # =========================
    # ⚡ RANDOM LOAD BALANCING
    # =========================
    def get_random_model(self, stage="draft"):

        provider = random.choice(list(self.providers.keys()))

        return {
            "provider": provider,
            "model": self.providers[provider][stage]
        }

    # =========================
    # 🔍 DEBUG
    # =========================
    def list_models(self):

        return self.providers

    def __repr__(self):
        return f"<ModelRouter default={self.default_provider}>"