from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Prompt, Generation
from apps.song.models import Status
from apps.library.models import Library
from apps.song.serializers import SongSerializerSave
from .serializers import PromptSerializer
import os
import requests as req
import hashlib

class SunoStatusViewController(APIView):
    def get(self, request, tid, uid=None):
        suno_key = os.getenv("SUNO_API_KEY")
        resp = req.get(f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={tid}", headers={"Authorization": f"Bearer {suno_key}"})
        json = resp.json()
        # print("notif")
        if json["code"] == 200:
            # update prompt
            try:
                user_id = uid or request.user.id
                print(user_id)
                library = Library.objects.filter(user=user_id).first()
                lastest_prompt = Prompt.objects.filter(task_id=tid).first()
                print(library)
                if library and lastest_prompt:
                    print("library and lastest_prompt exist")
                    if json["data"]["status"] == "SUCCESS":
                        print('json["data"]["status"] == "SUCCESS"')
                        prompt_serializer = PromptSerializer(lastest_prompt, data={"generation_status": Generation.SUCCESS}, partial=True)
                        if prompt_serializer.is_valid():
                            print('prompt_serializer.is_valid()')
                            saved_prompt = prompt_serializer.save()
                            hash_code = hashlib.sha256(
                                f"prompt-{saved_prompt.id}".encode()
                            ).hexdigest()[:12]

                            suno_data = json["data"]["response"]["sunoData"][0]
                            lyrics = self._resolve_lyrics(
                                user_lyrics=saved_prompt.lyrics,
                                suno_prompt=suno_data.get("prompt", ""),
                                task_id=tid,
                                suno_key=suno_key,
                            )

                            song_serializer = SongSerializerSave(data = {
                                "prompt": saved_prompt.id,
                                "library": library.id,
                                "song_name": lastest_prompt.song_name,
                                "image_link": suno_data.get("imageUrl") or "https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=2070&auto=format&fit=crop",
                                "song_url": suno_data["audioUrl"],
                                "shared_code": hash_code,
                                "sharing_status": Status.PRIVATE,
                                "description": saved_prompt.description,
                                "lyrics": lyrics,
                                "length": suno_data["duration"]
                            })
                            if song_serializer.is_valid():
                                print('song_serializer.is_valid()')
                                saved_song = song_serializer.save()
                                #
                            else:
                                print(song_serializer.errors)
            except Prompt.DoesNotExist:
                print("not even try")
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            
            return Response(json, status=status.HTTP_200_OK)
        else:
            print('else')
            return Response(json, status=status.HTTP_400_BAD_REQUEST)

    def _resolve_lyrics(self, user_lyrics: str, suno_prompt: str, task_id: str, suno_key: str) -> str:
        # Priority 1: user typed lyrics in the form
        if user_lyrics and user_lyrics.strip():
            return user_lyrics

        # Priority 2: Suno returned lyrics in the generate response prompt field
        if suno_prompt and suno_prompt.strip():
            return suno_prompt

        # Priority 3: call the dedicated lyrics endpoint as a last resort
        try:
            resp = req.get(
                f"https://api.sunoapi.org/api/v1/lyrics/record-info?taskId={task_id}",
                headers={"Authorization": f"Bearer {suno_key}"},
            )
            data = resp.json()
            if data.get("code") == 200:
                return data.get("data", {}).get("lyrics", "") or ""
        except Exception:
            pass

        return ""