import abc


class SongGenerationStrategy(abc.ABC):
    """
    Strategy Interface (Abstract Base Class) for song generation.
    Every concrete strategy MUST implement the generate() method.
    """

    @abc.abstractmethod
    def generate(self, request):
        """
        Generate a song based on the incoming Django HTTP request.

        Args:
            request: Django HttpRequest containing POST form data
                     (song_name, song_genre, song_mood, description, lyrics, keywords)

        Returns:
            HttpResponse / redirect — the Django response to return from the view.
        """
        raise NotImplementedError("Subclasses must implement generate(request)")
