import strawberry
from medias.models import Video, Photo
from strawberry import auto

@strawberry.django.type(Photo)
class PhotoType:
    id: auto
    file: str
    description: str

@strawberry.django.type(Video)
class VideoType:
    id: auto
    file: str
    description: str



