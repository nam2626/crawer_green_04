from bs4 import BeautifulSoup

# HTML 샘플 데이터 (실제 크롤링에서는 requests.get()으로 가져옴)
html = """
<html>
<body>
  <h1 class="page-title">공지사항</h1>
  <ul id="notice-list">
    <li class="notice-item">
      <a href="/notice/1">첫 번째 공지</a>
      <span class="date">2026-04-19</span>
    </li>
    <li class="notice-item">
      <a href="/notice/2">두 번째 공지</a>
      <span class="date">2026-04-18</span>
    </li>
    <li class="notice-item important">
      <a href="/notice/3">중요 공지</a>
      <span class="date">2026-04-17</span>
    </li>
  </ul>
</body>
</html>
"""

# BeautifulSoup로 HTML을 파싱합니다.
# "html.parser"는 Python 표준 파서입니다.
soup = BeautifulSoup(html, "html.parser")

# ── find / find_all ──────────────────────────────────────────
# find()   : 첫 번째 일치 요소 반환
# find_all(): 모든 일치 요소를 리스트로 반환

h1 = soup.find("h1")
print("제목:", h1.text)                      # 요소의 텍스트 내용
print("클래스:", h1["class"])                # 속성 접근

# 모든 <li> 요소를 찾습니다.
items = soup.find_all("li")
print(f"\n공지 수: {len(items)}")
for item in items:
    # find()로 자식 요소 찾기
    print(" -", item.find("a").text, "-", item.find("span", class_="date").text)

# id나 class 같은 속성으로 찾을 수 있습니다.
ul = soup.find("ul", id="notice-list")
print("\n목록 id:", ul["id"])

# class_="중첩된" (이스케이프): class는 Python 예약어이므로 class_ 사용
important = soup.find("li", class_="important")
print("중요 공지:", important.find("a").text if important else "없음")


# ── select / select_one (CSS 선택자) ─────────────────────────
# CSS 선택자는 jQuery나 JavaScript의 문법과 같습니다.
# select_one(): 첫 번째 일치 반환
# select()   : 모든 일치를 리스트로 반환

# h1.page-title : <h1 class="page-title">
title = soup.select_one("h1.page-title")
print("\n[CSS] 제목:", title.get_text(strip=True))  # strip=True: 공백 제거

# ul#notice-list li a : <ul id="notice-list"> 안의 모든 <li> > <a>
all_links = soup.select("ul#notice-list li a")
print("[CSS] 링크 목록:")
for a in all_links:
    print(f"  {a.text} → {a['href']}")

# .date : class="date"인 모든 요소
dates = soup.select(".date")
print("[CSS] 날짜:", [d.text for d in dates])