import os

from apps.prompt.MockSongGeneratorStrategy import MockSongGeneratorStrategy
from apps.prompt.SunoSongGeneratorStrategy import SunoSongGeneratorStrategy


class SongGenerationContext:
    @classmethod
    def resolve(cls, user_choice: str) -> tuple:
        """Returns (strategy_name, is_env_forced) for passing context to templates."""
        env_strategy = os.getenv("GENERATOR_STRATEGY", "").strip().lower()
        if env_strategy in {"mock", "suno"}:
            return env_strategy, True
        return (user_choice or "mock").lower(), False

    def __init__(self, strategy: str = None):
        # .env takes priority; fall back to the caller's choice when .env is blank
        env_strategy = os.getenv("GENERATOR_STRATEGY", "").strip()
        chosen = (env_strategy if env_strategy else (strategy or "mock")).lower()

        if chosen == "suno":
            self._strategy = SunoSongGeneratorStrategy()
        else:
            self._strategy = MockSongGeneratorStrategy()

    def execute(self, request):
        """
        Delegate the generate(request) call to whichever strategy was selected.

        Args:
            request: Django HttpRequest

        Returns:
            HttpResponse from the active strategy
        """
        return self._strategy.generate(request)
