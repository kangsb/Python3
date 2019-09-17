from bs4 import BeautifulSoup
import re
import time
from urllib.request import urlopen

def func_get_movie_list(URL, BBS_CATEGORY, Gijun) :
    print("<<<<<<<<<<<<<<<<<<<<<<<" + BBS_CATEGORY +">>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    pages = set()
    try:
        soup = BeautifulSoup(urlopen(URL), "html.parser", from_encoding='utf-8')
    except:
        print("[ERROR] soup 실행 실패")
        return
    LinkListRAW = soup.findAll(class_="yt-lockup-content")
    for LINK_RAW in LinkListRAW:
       parseLink=LINK_RAW.find("a")
       Link="https://www.youtube.com"+parseLink.get("href").replace("..","").replace("./", "", 1)
       Title=parseLink.get("title")
       RAW_Thumbnail="https://i.ytimg.com/vi/"+parseLink.get("href").replace("/watch?v=","")+"/hqdefault.jpg"
       MovieCode=parseLink.get("href").replace("/watch?v=","")
       ReadCountRaw=(LINK_RAW.find("ul").text)
       ReadCountRawPoint=(LINK_RAW.find("ul").text).find("수")+1
       ReadCount=(ReadCountRaw[ReadCountRawPoint:]).replace(" ","").replace(",","").replace("회","")
       print("[영상링크]" + Link)
       print("[제목]" + Title)
       print("[조회수]" + ReadCount)
       print("[썸네일주소]" + RAW_Thumbnail)
       print("[영상코드]" + MovieCode)
       try:
           Count=int(ReadCount)
       except:
           print("[ERROR] 게시물 리딩 갯수 조회 불가")
           Count=0
       if Count > Gijun:
           print("[INFO] 조회수"+str(Gijun)+" 넘으므로 업로드 대상")
           print(MovieCode, Title, BBS_CATEGORY)
#           UploadBBS(MovieCode, Title, RAW_Thumbnail, BBS_CATEGORY)
       else:
           print("[INFO] 처리 불가(조회수 적음) =>"+str(Count))


BBS_CATEGORY="BBS_ARMY"
ARMY=[ '군대', '해병', '해군', '특전사', '육군', '공군', '공수부대' ] # 해당 문자열 패턴이 있는 영상만 검색

Limit=len(ARMY)
Gijun=400000 # 월간 40만건 이상 조회수 기록한 글만 크롤링
count=0

while count < Limit:
   KEY=str(str(ARMY[count]).encode('utf8')).replace("\\x","%").replace("b'","")
   URL="https://www.youtube.com/results?search_query="+KEY+"&sp=CAMSBAgEEAE%253D" # 월간
   func_get_movie_list(URL, BBS_CATEGORY, Gijun)
   time.sleep(7)
   count+=1
