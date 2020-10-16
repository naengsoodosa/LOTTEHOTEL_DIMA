# 현재 노출되고 있는 메인프로모션이 몇개인지 (6개인지) 체크하는 프로그램
# 글로벌은 7개 언어 / 국내 체인은 4개 언어 / 해외체인은 5개 언어
# 3개, 6개는 ○ / 2개, 5개는 위험 / 1개, 4개는 긴급
# 조회한 날짜와 시간도 출력
# 표 형태로 만들자


import requests
from bs4 import BeautifulSoup
import datetime
import time
import pandas as pd

start = time.time()

#체인사이트 호텔코드
GLOBAL = ["global"]
STAR6s = ["seoul-signiel","busan-signiel"]
STAR5s = ["seoul-hotel","world-hotel","busan-hotel","jeju-hotel","ulsan-hotel"]
STAR4s = ["mapo-city","gimpo-city","guro-city","myeongdong-city","jeju-city","ulsan-city","daejeon-city"]
L7s = ["myeongdong-l7","gangnam-l7","hongdae-l7"]
USA = ["seattle-hotel", "guam-hotel"]
RUSSIA = ["moscow-hotel","stpetersburg-hotel","vladivostok-hotel"]
VIETNAM = ["saigon-hotel","hanoi-hotel"]
JAPAN = ["arai-resort"]
MYANMAR = ["yangon-hotel"]

KOREA = STAR6s + STAR5s + STAR4s + L7s
OVERSEAS = USA + RUSSIA + VIETNAM + JAPAN + MYANMAR
TOTAL_CHAINS = GLOBAL + KOREA + OVERSEAS


# LANGUAGE = ["ko","en","ja","zh","ru","vi","my"]
def get_site_language(chain):
    lan = ""
    if (chain in GLOBAL):
        lan = ["ko","en","ja","zh","ru","vi","my"]
    elif (chain in KOREA or chain in USA or chain in JAPAN):
        lan = ["ko", "en", "ja", "zh"]
    elif (chain in RUSSIA) :
        lan = ["ko", "en", "ja", "zh", "ru"]
    elif (chain in VIETNAM) :
        lan = ["ko", "en", "ja", "zh", "vi"]
    elif (chain in MYANMAR) :
        lan = ["ko", "en", "ja", "zh", "my"]
    else :
        lan = "error"
    return lan

# print(get_site_language('arai-resort'))


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
# url = "https://www.lottehotel.com/global/ko.html"
WEBSITE = "https://www.lottehotel.com/"

def get_site_urls(chain):
    hotel_code = str(chain)
    languages = get_site_language(chain)

    urls = []
    for lan_code in languages:
        urls.append(WEBSITE + hotel_code + "/" + lan_code + ".html")

    return urls

# print(get_site_urls('mapo-city'))




def get_product_info(product, bs_obj):
    # number = 0
    # for product in promotion_inside:
    #     number += 1

    title = product.find("a", {"class": "promotion__title"})


    tagged_hotel = product.find("p", {"class": "promotion__hotel"})
    if (tagged_hotel != None):
        hotel = tagged_hotel
    else:
        hotel = bs_obj.find("h1", {"class": "hotel__name"})

    # Global이면 상품명에서 호텔명을 추출하고
        # if (chain in GLOBAL):
    # hotel = product.find("p", {"class": "promotion__hotel"})
        # else:
        # # global이 아니면, 다른 호텔명태그에서 호텔명 추출한다
        #     hotel = bs_obj.find("h1", {"class": "hotel__name"})



    return {"hotel":hotel.text, "title":title.text, "URL":title['href']}




def get_promotion_list(chain):
    print("체인 코드 :",chain)

    for url in get_site_urls(chain):
        print(url)

        result = requests.get(url, headers)
        bs_obj = BeautifulSoup(result.content, "html.parser")

        # 캐로셀 컴포넌트 자체가 없는 경우 (상트...)
        tagged_carousel = bs_obj.find("div", {"class": "s004__carousel"})
        if (tagged_carousel != None):
            carousel = bs_obj.find("div", {"class": "s004__carousel"})
            promotion_inside = carousel.findAll("div", {"class": "promotion__inside"})

            # 체인의 언어별 사이트에서 상품의 정보를 리스트로 받아온다
            check_numbers = 0
            for product in promotion_inside:
                product_info_list = [get_product_info(product, bs_obj)]
                print(product_info_list)
                check_numbers += 1

            # 체인의 언어별 사이트의 프로모션 상태에 대한 경고
            signal = ""
            if (check_numbers == 6 or check_numbers == 3):
                signal = "OK"
            elif (check_numbers == 5 or check_numbers == 2):
                signal = "HURRY UP"
            else:
                signal = "EMERGENCY"

        else:
            check_numbers = 0
            signal = "CAROUSEL COMPONENT DELETED, EMERGENCY"





        print("프로모션 숫자 : ", check_numbers, "   "+signal)

    return





start_Datetime = datetime.datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')
print("조회시간 :",start_Datetime)  # 2015-04-19 12:11:32

for chain in TOTAL_CHAINS:
    print(get_promotion_list(chain))
    print("--------------------------------------")


end_Datatime = datetime.datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')
print("완료시간 :",end_Datatime)  # 2015-04-19 12:11:32

sec = time.time() - start
crawling_times = str(datetime.timedelta(seconds=sec)).split(".")
print("소요시간 :",sec)  # 2015-04-19 12:11:32

# # print(get_promotion('global'))
# print(get_product_info('mapo-city'))
# print(get_product_info('global'))
