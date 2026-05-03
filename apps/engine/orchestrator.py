from .state_manager import PipelineState
from .pipeline import Pipeline

import uuid
import time
import logging

logger = logging.getLogger(__name__)


def run_pipeline(
    keyword,
    intent="informational",
    extra_context=None,
    job_id=None
):
    """
    🚀 Orchestrator Entry Point (API SAFE VERSION)

    Fixes:
    - JSON serialization safe
    - no raw objects returned
    - frontend compatible
    """

    start_time = time.time()
    job_id = job_id or str(uuid.uuid4())

    logger.info(f"🚀 Start | job_id={job_id} | keyword={keyword}")

    try:
        # =========================
        # 🧠 INIT STATE
        # =========================
        state = PipelineState(keyword)

        state.context = {
            "keyword": keyword,
            "intent": intent,
            "job_id": job_id,
            **(extra_context or {})
        }

        # =========================
        # 🚀 RUN PIPELINE
        # =========================
        pipeline = Pipeline(state)
        article, summary = pipeline.run()

        duration = round(time.time() - start_time, 3)

        logger.info(f"✅ Success | job_id={job_id} | {duration}s")

        # =========================
        # 🔥 SAFE RESPONSE (IMPORTANT FIX)
        # =========================
        safe_article = article or {}

        return {
            "status": "success",
            "job_id": job_id,
            "duration": duration,

            # 🔥 frontend friendly fields
            "title": safe_article.get("title"),
            "meta": safe_article.get("meta_description"),
            "content": safe_article.get("content"),

            # 🔥 safe extras
            "score": int(safe_article.get("seo_score", 0)),
            "final_score": int(summary.get("final_score", 0)) if summary else 0,
            "attempts": int(summary.get("attempts", 0)) if summary else 0
        }

    except Exception as e:
        duration = round(time.time() - start_time, 3)

        logger.error(f"❌ Failed | job_id={job_id} | error={e}")

        return {
            "status": "error",
            "job_id": job_id,
            "duration": duration,
            "error": str(e)
        }