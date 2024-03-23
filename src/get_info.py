from PIL import Image
from io import BytesIO
import pathlib
from datetime import datetime

import book_spider
import movie_spider

current_dictionary = pathlib.Path(__file__).parent.resolve()


class DoubanInfo:
    def __init__(self, url):
        self.url = url
        self.image_path = None
        self.title = None
        self.rate = None
        self.category = None 
        self.is_movie = True  

def format_date(date_str):
    # Parse the date string into a datetime object
    date_str = date_str.split("(")[0]
    try: 
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except: 
        date_obj = datetime.strptime(date_str, '%Y-%m')
    # Format the datetime object to the desired format
    formatted_date = date_obj.strftime('%Y年%m月')
    return formatted_date

def get_info_from_url(url, download_image_from_douban=False):
    info = DoubanInfo(url)

    if "movie" in url:
        doubaninfo = movie_spider.MovieInfo(url, download_image=download_image_from_douban)
    else:
        doubaninfo = book_spider.BookInfo(url, download_image=download_image_from_douban)
        info.is_movie = False 

    output_path = current_dictionary / "../assets/bgimage.png"
    if download_image_from_douban:
        image = Image.open(BytesIO(doubaninfo.bgimg_content))
        image.save(output_path)

    if info.is_movie: 
        info.date = doubaninfo.describe['date'][0]
        info.date = "上映时间 | " + format_date(info.date) 
        info.category = "类型 | " + " / ".join(doubaninfo.describe['type'])
    else: 
        info.date = doubaninfo.describe['date']
        info.date = "出版时间 | " + format_date(info.date) 
        info.category = "作者 | " + doubaninfo.describe['type'] 

    info.title = doubaninfo.title_name

    info.rate = doubaninfo.rate if len(doubaninfo.rate) > 0 else None  

    return info


if __name__ == "__main__":
    url = "https://book.douban.com/subject/36480672/"
    get_info_from_url(url)
