# 엑셀로 내보내자
# {col : [~~~,~~~,~~~]} 형태로 만들어야한다고 함

import requests
from bs4 import BeautifulSoup
import datetime
import time
import pandas as pd
import xlsxwriter


start = time.time()

# 체인사이트 호텔코드
GLOBAL = ["global"]
STAR6s = ["seoul-signiel", "busan-signiel"]
STAR5s = ["seoul-hotel", "world-hotel", "busan-hotel", "jeju-hotel", "ulsan-hotel"]
STAR4s = ["mapo-city", "gimpo-city", "guro-city", "myeongdong-city", "jeju-city", "ulsan-city", "daejeon-city"]
L7s = ["myeongdong-l7", "gangnam-l7", "hongdae-l7"]
USA = ["seattle-hotel", "guam-hotel"]
RUSSIA = ["moscow-hotel", "stpetersburg-hotel", "vladivostok-hotel"]
VIETNAM = ["saigon-hotel", "hanoi-hotel"]
JAPAN = ["arai-resort"]
MYANMAR = ["yangon-hotel"]

KOREA = STAR6s + STAR5s + STAR4s + L7s
OVERSEAS = USA + RUSSIA + VIETNAM + JAPAN + MYANMAR
TOTAL_CHAINS = GLOBAL + KOREA + OVERSEAS


# LANGUAGE = ["ko","en","ja","zh","ru","vi","my"]
def get_site_language(chain):
    lan = ""
    if (chain in GLOBAL):
        lan = ["ko", "en", "ja", "zh", "ru", "vi", "my"]
    elif (chain in KOREA or chain in USA or chain in JAPAN):
        lan = ["ko", "en", "ja", "zh"]
    elif (chain in RUSSIA):
        lan = ["ko", "en", "ja", "zh", "ru"]
    elif (chain in VIETNAM):
        lan = ["ko", "en", "ja", "zh", "vi"]
    elif (chain in MYANMAR):
        lan = ["ko", "en", "ja", "zh", "my"]
    else:
        lan = "error"
    return lan


# print(get_site_language('arai-resort'))

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
# url = "https://www.lottehotel.com/global/ko.html"
WEBSITE = "https://www.lottehotel.com/"


# 체인의 url을 언어별로 구하는 함수
def get_site_urls(chain):
    hotel_code = str(chain)
    languages = get_site_language(chain)

    urls = []
    for lan_code in languages:
        urls.append(WEBSITE + hotel_code + "/" + lan_code + ".html")

    return urls


# 구분, 지역 정보 추출하는 함수
def get_where_stars(chain):
    where = ''
    stars = ''

    if (chain in GLOBAL):
        where = '글로벌'
        stars = '---'
    elif (chain in KOREA):
        where = '국내'
        if (chain in STAR6s):
            stars = '6성'
        elif (chain in STAR5s):
            stars = '5성'
        elif (chain in STAR4s):
            stars = '시티'
        else:
            stars = '엘세븐'
    else:
        where = '해외'
        if (chain in USA):
            stars = '미국'
        elif (chain in RUSSIA):
            stars = '러시아'
        elif (chain in VIETNAM):
            stars = '베트남'
        elif (chain in JAPAN):
            stars = '일본'
        else:
            stars = '미얀마'

    where_stars_list = []
    where_stars_list = [where, stars]
    return where_stars_list


# 호텔이름을 검색바에서 가져오기
# hotel 코드까지만 있으면, 국문 사이트만으로도 호텔정보는 나오잖아?
def get_hotelname(chain):
    if (chain == 'global'):
        hotel_name = '글로벌'
    else:
        urls = get_site_urls(chain)

        result = requests.get(urls[0], headers)
        bs_obj = BeautifulSoup(result.content, "html.parser")

        hotel_name = bs_obj.find("h1", {"class": "hotel__name"}).text

    return [hotel_name]


# 넘겨받은 url에서 프로덕트가 몇개있는지 세는 함수
def count_promotion(url):
    result = requests.get(url, headers)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    tagged_carousel = bs_obj.find("div", {"class": "s004__carousel"})
    if (tagged_carousel != None):
        carousel = bs_obj.find("div", {"class": "s004__carousel"})
        promotion_inside = carousel.findAll("div", {"class": "promotion__inside"})
    else:
        promotion_inside = ''

    return len(promotion_inside)


# print(count_promotion('https://www.lottehotel.com/mapo-city/ko.html'))

# 무조건 언어7개는 다 돌아야된다
# chain이 각 언어에서 몇개의 프로덕트를 가지고있는지 세라
LANGUAGE = ["ko", "en", "ja", "zh", "ru", "vi", "my"]


def get_language_count(chain):
    # 1. 호텔이 가진 언어를 구함
    url_lan = []
    url_lan = get_site_language(chain)

    # 2. 그 언어별 url에서 프로모션이 몇개 있는지 구함
    count_list = []
    for url in get_site_urls(chain):
        count_list.append(count_promotion(url))

    # 3. 최대 7개까지 언어를 가질 수 있음 (LANGUAGE)

    # 4. 7개언어와 호텔이가진언어를 비교함
    i = 0
    lan_count = [7, 7, 7, 7, 7, 7, 7]

    for lan in url_lan:
        j = 0
        for LAN in LANGUAGE:
            if (lan == LAN):
                lan_count[j] = (count_list[i])
            j += 1
        i += 1

    # 5. 만약 7(기본값)이라면, '-'으로 치환
    for n in range(7):
        if (lan_count[n] == 7):
            lan_count[n] = '-'

    return lan_count


# 호텔정보와 프로모션현황을 합치는 함수
def hotelinfo_add_count(chain):
    return get_where_stars(chain) + get_hotelname(chain) + get_language_count(chain)


# print('----1----')
# print(get_hotel_info('mapo-city'))
# print('-----2---')
# print(get_language_count('guro-city'))
# print('----3----')
# print(hotelinfo_add_count('yangon-hotel'))

# 전체 돌리기
# print("--------------------------------------")
# for chain in TOTAL_CHAINS:
#     print(hotelinfo_add_count(chain))
#     print("--------------------------------------")

###----출력부분------
#시작시간
start_Datetime = datetime.datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')
print("조회시간 :",start_Datetime)  # 2015-04-19 12:11:32

# 데이터프레임 만들기
data = []
for chain in TOTAL_CHAINS:
    print("/")
    data.append(hotelinfo_add_count(chain))

col_name = ['지역','구분','호텔명','KO','EN','JP','ZH','RU','VI','MI']
df = pd.DataFrame.from_records(data, columns = col_name)



#데이터프레임 출력
print(df)

#종료시간
end_Datetime = datetime.datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')
print("완료시간 :",end_Datetime)  # 2015-04-19 12:11:32


#엑셀로 저장
print("엑셀저장시작")

path = r"C:\python_study\LOTTE_DIMA\EXCEL\main_promotion.xlsx"
writer = pd.ExcelWriter(path, engine='xlsxwriter', options={'encoding':'utf-8'})

filename_date = datetime.datetime.now().strftime('%Y%m%d')
df.to_excel(path.split('.xlsx')[0] + '_' + filename_date + '.xlsx', sheet_name='Sheet1')

writer.save()
# writer.close()


print("엑셀완료",filename_date)
sec = time.time() - start
crawling_times = str(datetime.timedelta(seconds=sec)).split(".")
print("소요시간 :",crawling_times[0])  # 2015-04-19 12:11:32

