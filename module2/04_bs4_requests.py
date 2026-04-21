import sys
import requests
from bs4 import BeautifulSoup

# Windows 터미널에서 특수문자(£ 등) 출력 시 인코딩 오류 방지
sys.stdout.reconfigure(encoding="utf-8")

# 크롤링 대상 URL
URL = "https://books.toscrape.com"

# HTTP GET 요청 보내기
response = requests.get(URL)

# 응답 인코딩을 UTF-8로 명시 (£ 기호 이중 인코딩 방지)
response.encoding = "utf-8"

# 응답 상태 코드 확인 (200이면 정상)
print(f"상태 코드: {response.status_code}")
# print(response.text)
# 응답 HTML을 BeautifulSoup으로 파싱
# html.parser: 파이썬 내장 HTML 파서
soup = BeautifulSoup(response.text, "html.parser")

# 모든 책 항목 찾기
# 각 책은 <article class="product_pod"> 태그 안에 있음
books = soup.select("article.product_pod")

print(f"총 책 수: {len(books)}권\n")

for i, book in enumerate(books, start=1):
    # 책 제목: <h3> 안의 <a> 태그의 title 속성값
    # title = book.select_one("h3 a")["title"]
    title = book.select_one("h3").text.strip()  # title 속성 대신 텍스트로도 가능

    # 책 가격: <p class="price_color"> 태그의 텍스트
    price = book.select_one("p.price_color").text.strip()

    # 재고 여부: <p class="instock availability"> 태그의 텍스트
    availability = book.select_one("p.availability").text.strip()

    # 별점: <p class="star-rating"> 태그의 두 번째 클래스값 (One, Two, Three, Four, Five)
    rating_class = book.select_one("p.star-rating")["class"]
    rating = rating_class[1]  # 예: ['star-rating', 'Three'] → 'Three'

    print(f"[{i:2d}] {title}")
    print(f"      가격: {price} | 재고: {availability} | 별점: {rating}")
