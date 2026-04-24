import os

from apps.prompt.strategy import MockSongGeneratorStrategy, SunoSongGeneratorStrategy


class SongGenerationContext:
    """
    Context class for the Strategy Pattern.

    Reads GENERATOR_STRATEGY from the .env file at construction time and
    wires up the correct concrete strategy automatically.

    Usage in a view:
        context = SongGenerationContext()
        return context.execute(request)
    """

    def __init__(self):
        chosen = os.getenv("GENERATOR_STRATEGY", "mock").lower()

        if chosen == "suno":
            self._strategy = SunoSongGeneratorStrategy()
        else:
            # Default / fallback to mock (safe for local dev)
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
