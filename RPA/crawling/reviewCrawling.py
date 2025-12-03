#requests: 웹페이지의 HTML 문서를 가져오는 라이브러리
#BeautifulSoup: HTML 문서를 파싱하고 원하는 데이터를 추출하는 라이브러리
#pandas: 데이터 분석 및 조작을 위한 라이브러리(추출한 리뷰 데이터를 저장하고 CSV 파일로 내보내기 위해 사용)
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_reviews(url):
    # 웹페이지 요청 및 HTML 문서 가져오기:
    response = requests.get(url)
    # HTML 문서 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    # 리뷰 데이터 추출
    review_titles = soup.select('ul.reviewItems_list_review__q726A > li em.reviewItems_title__AwHcz')
    review_contents = soup.select('ul.reviewItems_list_review__q726A > li p.reviewItems_text_XrSSf')
    # 추출한 리뷰 데이터를 저장할 리스트 초기화
    reviews = []
    # 리뷰 제목과 내용을 리스트에 저장
    for title, content in zip(review_titles, review_contents):
        reviews.append({
            '제목': title.text.strip(),
            '내용': content.text.strip()
        })
    return reviews

# 추출한 리뷰 데이터를 CSV 파일로 저장
def save_to_excel(reviews, filename, sheet_name):
    #추출한 리뷰 데이터를 데이터프레임으로 변환
    df = pd.DataFrame(reviews)
    # 데이터프레임을 엑셀 파일로 저장
    df.to_excel(filename, index=False, sheet_name=sheet_name)

if __name__ == "__main__":
    url = "https://search.shopping.naver.com/catalog/26529080523?query=%EB%85%B8%ED%8A%B8%EB%B6%81&NaPm=ct%3DIkijeiog%7Cci%3Df5c5bd02303e2533690d2e629d8db564c788044d%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D953da896c3b8385391a53c6c3fc7f6e8cfb9898b"
    reviews = extract_reviews(url)
    save_to_excel(reviews, "notebook_reviews.xlsx", "노트북 리뷰 수집")
    print("저장되었습니다.")