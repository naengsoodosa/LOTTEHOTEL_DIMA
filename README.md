
# LOTTEHOTEL_DIMA
크롤링배워서 일에다 써먹음;


## 1. check_main_promotion.py [2020.10.16]
- 현재 노출되고 있는 메인프로모션이 몇개인지 (6개인지) 체크하는 프로그램
- 총 27개 체인 : 글로벌(1), 국내(17), 해외(9)
- 글로벌은 7개 언어 / 국내 체인은 4개 언어 / 해외체인은 5개 언어 
- 프로모션 게시 : 3개, 6개는 ○ / 2개, 5개는 위험 / 1개, 4개는 긴급 / 컴포넌트가 없어도 긴급
- 조회한 날짜와 완료시간, 소요시간도 출력
- **표 형태로 만들자**


## 2. excel_promotion_list.py [2020.10.21]
- 호텔의 언어별 프로모션 등록현황을 뽑음
- 데이터프레임으로 구현
- 해당날짜의 파일명으로 엑셀파일로 저장

## 3. img_save_PDF.py [2020.12.13] //파이썬자동화책 발췌
- 카드뉴스(TTnews)에서 연속된 이미지를 자동으로 저장함
- 해당 이미지를 모아서 pdf로 변환함

## 4. eBook_scroll_save_PDF.py [2020.12.13] //파이썬자동화책 발췌
- 교보문고에서 e북 미리보기를 스크롤하여 3장 저장함
- 해당 이미지를 모아서 pdf로 변환함

## 5. naver_news_top4 [2020.12.15]
- 네이버 실시간 검색 후, 상위뉴스 4개의 타이틀/링크 가져옴
