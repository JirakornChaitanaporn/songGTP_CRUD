import os

from apps.prompt.strategy import MockSongGeneratorStrategy, SunoSongGeneratorStrategy


class SongGenerationContext:
    """
    Context class for the Strategy Pattern.

    Accepts an explicit strategy name ("mock" or "suno").
    If no name is passed, falls back to reading GENERATOR_STRATEGY from .env.

    Usage in a view (explicit — recommended):
        context = SongGenerationContext("mock")
        context = SongGenerationContext("suno")
        return context.execute(request)

    Usage with .env fallback:
        context = SongGenerationContext()
        return context.execute(request)
    """

    def __init__(self, strategy: str = None):
        # Use the explicitly passed strategy name, or fall back to .env
        chosen = (strategy or os.getenv("GENERATOR_STRATEGY", "mock")).lower()

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
