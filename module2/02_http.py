import requests

BASE_URL = "https://jsonplaceholder.typicode.com"  # 무료 테스트용 REST API

# ======================================================
# GET — 데이터 조회
# ======================================================

# 단일 리소스 조회 (게시글 1번)
response = requests.get(f"{BASE_URL}/posts/1")
print(str(response))
# status_code: HTTP 응답 코드 (200 성공, 404 없음, 500 서버오류 등)
print(response.status_code)

# .json(): 응답 body를 파이썬 딕셔너리로 변환
# 응답한 body 기본적으로는 텍스트
post = response.json()
print(post)
print(post["title"])

# 목록 조회 — params로 쿼리스트링 전달 (?userId=1)
response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
posts = response.json()
print('--------------------------------')
print(posts)
print('--------------------------------')
print(f"게시글 수: {len(posts)}")
print('--------------------------------')


# ======================================================
# POST — 데이터 생성
# ======================================================
print('--------------------------------')

new_post = {"title": "테스트 제목", "body": "내용입니다", "userId": 1}

# json=new_post: 딕셔너리를 JSON으로 직렬화 + Content-Type 자동 설정
response = requests.post(f"{BASE_URL}/posts", json=new_post)

# 201: 생성 성공을 나타내는 HTTP 상태코드

print('생성 : ',response.status_code)
print(response.json())
print('--------------------------------')


# ======================================================
# headers & timeout — 실전에서 자주 쓰는 옵션
# ======================================================

headers = {
    "User-Agent": "MyCrawler/1.0",   # 봇 차단 우회용 브라우저 식별 헤더
    "Accept": "application/json",
}

# timeout: 초 단위, 지정 시간 초과 시 requests.Timeout 예외 발생
response = requests.get(f"{BASE_URL}/posts/1", headers=headers, timeout=5)
print(response.status_code)


# ======================================================
# 예외 처리 — 네트워크 오류 대비
# ======================================================

try:
    response = requests.get(f"{BASE_URL}/posts/1", timeout=5)
    response.raise_for_status()  # 4xx, 5xx 응답이면 HTTPError 예외 발생
    print(response.json())
except requests.exceptions.Timeout:
    print("요청 시간 초과")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 오류: {e}")
except requests.exceptions.ConnectionError:
    print("네트워크 연결 실패")
