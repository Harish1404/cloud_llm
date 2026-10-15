from app.ai.models import models


def _is_quota_or_rate_limit_error(error: Exception) -> bool:
    message = str(error).lower()
    status_code = getattr(error, "status_code", None)

    return any(
        keyword in message
        for keyword in (
            "quota",
            "resource exhausted",
            "rate limit",
            "too many requests",
            "exhausted",
        )
    ) or status_code in {429, 403}


def llm_with_retry_and_fallback(prompt: str, max_attempts: int = 3) -> str:
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return models.gemini_llm(prompt)
        except Exception as error:
            last_error = error
            if _is_quota_or_rate_limit_error(error):
                break
            if attempt == max_attempts:
                break

    try:
        return models.groq_llm(prompt)
    except Exception as fallback_error:
        if last_error is not None:
            raise RuntimeError(
                "Gemini failed after retries and Groq fallback also failed."
            ) from fallback_error
        raise fallback_error
