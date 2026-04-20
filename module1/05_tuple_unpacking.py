# ── tuple 기본 ───────────────────────────────────────────────
# tuple은 순서가 있는 불변(immutable) 컬렉션입니다.
# 소괄호 ()로 만들며, 한 번 생성하면 요소를 변경할 수 없습니다.

point = (10, 20)
print(point[0])     # 10
print(point[1])     # 20

# tuple은 수정 불가 — 아래 줄을 실행하면 TypeError가 발생합니다.
# point[0] = 99

# 소괄호를 생략해도 tuple로 인식됩니다.
rgb = 255, 128, 0
print(type(rgb))    # <class 'tuple'>


# ── unpacking ────────────────────────────────────────────────
# tuple의 각 요소를 여러 변수에 한 번에 할당하는 문법입니다.
# JavaScript의 구조 분해 할당 const [x, y] = point 와 같습니다.

x, y = point
print(f"x={x}, y={y}")

# 함수가 여러 값을 반환할 때 언패킹으로 각 변수에 바로 받습니다.
def get_user_info():
    return "홍길동", 25, "서울"     # tuple로 반환

name, age, city = get_user_info()   # 세 값을 한 번에 받기
print(f"{name} / {age}세 / {city}")

# 필요 없는 값은 _ 변수에 할당해 무시하는 관례가 있습니다.
name, _, city = get_user_info()     # 나이(age)는 필요 없어 _ 로 버림
print(f"{name} ({city})")


# ── enumerate — 인덱스 + 값 동시에 ──────────────────────────
# enumerate()는 반복할 때 (인덱스, 값) tuple을 반환합니다.
# JavaScript의 forEach((item, index) => ...) 와 같습니다.

fruits = ["사과", "바나나", "딸기"]

for i, fruit in enumerate(fruits):     # tuple 언패킹으로 바로 분리
    print(f"{i + 1}번: {fruit}")

# enumerate 자체가 어떤 값을 반환하는지 확인
for item in enumerate(fruits):
    print(item)   # (0, '사과'), (1, '바나나'), (2, '딸기')


# ── dict.items() — key + value 동시에 ────────────────────────
# .items()는 (key, value) tuple의 시퀀스를 반환합니다.
# for key, value in ... 로 언패킹해서 받는 것이 일반적입니다.

person = {"name": "홍길동", "age": 25, "city": "서울"}

for key, value in person.items():
    print(f"{key} → {value}")


# ── zip — 두 list를 묶어서 반복 ──────────────────────────────
# zip()은 여러 리스트를 같은 인덱스끼리 묶어 tuple로 반환합니다.
# 두 리스트의 길이가 다르면 짧은 쪽에 맞춰 종료됩니다.

names  = ["홍길동", "이영희", "박민준"]
scores = [85, 92, 78]

for name, score in zip(names, scores):  # 같은 위치 요소끼리 묶임
    print(f"{name}: {score}점")

# dict()와 zip()을 함께 쓰면 두 리스트로 dict를 만들 수 있습니다.
# 크롤링에서 컬럼명과 값 리스트를 합칠 때 유용합니다.
keys   = ["title", "url", "date"]
values = ["Python 강의", "https://example.com/1", "2026-04-19"]

record = dict(zip(keys, values))    # 키-값 쌍으로 dict 생성
print(record)
