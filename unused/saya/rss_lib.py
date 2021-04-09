from pydantic import BaseModel
import feedparser as fd

class Entrie(BaseModel):
    '''表达entries'''
    title: str
    id: str
    published: str
    summary: str


class Feed(BaseModel):
    '''表达feed'''
    title: str
    link: str
    subtitle: str



class Rss():
    '''传入Feed Url'''
    def __init__(self,url) -> None:
        self.parser = fd.parse(url)
    
    def get_entries(self,post: int = 0) -> Entrie:
        return Entrie(**self.parser['entries'][post])
    
    def get_feed(self) -> Feed:
        return Feed(**self.parser['feed'])