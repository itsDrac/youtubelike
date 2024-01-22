from beanie import Document, Link


class Video(Document):
    videofile: str  # clodinary url
    thumbnail: str  # clodinary url
    # owner: Link[User]
    title: str
    description: str | None = None
    duration: int
    views: int = 0
    ispublished: bool = True
