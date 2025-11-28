import os
import logging
from typing import Dict, Any

try:
    import openai
except Exception:  # pragma: no cover - runtime dependency
    openai = None

logger = logging.getLogger(__name__)


class OpenAIService:
    """Minimal wrapper around OpenAI to generate user-friendly explanations

    Reads API key from `OPENAI_API_KEY` environment variable. Keeps calls small
    and focused on producing concise, privacy-preserving explanations for
    recommendation reasons.
    """

    @staticmethod
    def is_available() -> bool:
        return openai is not None and bool(os.environ.get('OPENAI_API_KEY'))

    @staticmethod
    def generate_explanation(recommendation: Dict[str, Any], user_context: Dict[str, Any] = None) -> str:
        """Generate a short, user-friendly explanation for a recommendation.

        recommendation: dict with keys like `title`, `reason`, `factors`, `confidence`.
        user_context: optional dict with non-sensitive context (learning style, recent scores).
        Returns a short text explanation.
        """
        if not OpenAIService.is_available():
            # Fallback to the existing reason_text or a simple template
            return recommendation.get('reason_text') or f"Recommended because: {recommendation.get('reason', 'matching your profile')}"

        try:
            openai.api_key = os.environ.get('OPENAI_API_KEY')

            # Build a concise prompt emphasizing explainability and privacy
            prompt_lines = [
                "You are an assistant that writes concise, user-friendly explanations for content recommendations.",
                "Do not include sensitive personal data. Keep it under 40 words.",
                "Recommendation information:",
                f"Title: {recommendation.get('title')}",
                f"Reason: {recommendation.get('reason')}",
                f"Confidence: {round(recommendation.get('score', 0) * 100)}%",
            ]

            factors = recommendation.get('factors') or []
            if factors:
                prompt_lines.append('Top factors:')
                for f in (factors if isinstance(factors, list) else [factors]):
                    # Each factor expected to be {'name','weight','explanation'}
                    name = f.get('name') if isinstance(f, dict) else str(f)
                    explanation = (f.get('explanation') if isinstance(f, dict) else '')
                    prompt_lines.append(f"- {name}: {explanation}")

            if user_context:
                # Only non-sensitive context
                prompt_lines.append('User context:')
                if 'learning_style' in user_context:
                    prompt_lines.append(f"- learning_style: {user_context.get('learning_style')}")
                if 'recent_average' in user_context:
                    prompt_lines.append(f"- recent_average: {user_context.get('recent_average')}")

            prompt_lines.append('Return a single concise explanation in French.')
            prompt = "\n".join(prompt_lines)

            # Use chat completion to generate the explanation
            response = openai.ChatCompletion.create(
                model=os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "You generate brief explanations for users about why content is recommended."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=80,
                temperature=0.2,
                n=1,
            )

            text = response.choices[0].message.content.strip()
            # Ensure short length
            if len(text.split()) > 60:
                text = ' '.join(text.split()[:60]) + '...'

            return text
        except Exception as e:
            logger.exception('OpenAI explanation generation failed')
            return recommendation.get('reason_text') or recommendation.get('reason', '')


openai_service = OpenAIService()
