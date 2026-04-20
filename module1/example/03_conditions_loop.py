# -- 조건문 --
# if, elif, else
age = 16

if age >= 18:
    print("성인")
elif age >= 13:     # JavaScript의 else if → Python은 elif
    print("청소년")
    if age >= 16:
        print("운전 가능")
        print("술 구매 가능")
else:
    print("어린이")

# 삼항 연산자
# JavaScript: const status = age >= 18 ? '성인' : '미성년자';
status = '성인' if age >= 18 else '미성년자'
print(status)

# -- 반복문 --
# for, while
i = 1
result = ''
while i <= 10:
    result += f'{i} ' # 자바스크립트처럼 문자열 + 숫자 이런 형태 연산 지원하지 않음
    i += 1; 
print(result)

# ── for 반복문 ───────────────────────────────────────────────
# range(n)      → 0 이상 n 미만의 정수 시퀀스
# range(a, b)   → a 이상 b 미만
# range(a, b, step) → step 간격으로 증가

for i in range(5):          # 0, 1, 2, 3, 4
    print(i, end=" ")       # end=" " → 줄바꿈 대신 공백으로 구분
print()                     # 줄바꿈

for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(i, end=" ")
print()

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8 (2씩 증가)
    print(i, end=" ")
print()

# 리스트 요소를 직접 순회합니다. JavaScript의 for...of 와 같습니다.
fruits = ["사과", "바나나", "딸기"]
for fruit in fruits:
    print(fruit)

# ── break / continue ─────────────────────────────────────────
# continue : 현재 반복을 건너뛰고 다음 반복으로 이동
# break    : 반복문 전체를 즉시 종료

for i in range(10):
    if i == 3:
        continue    # 3은 출력 건너뜀
    if i == 7:
        break       # 7에서 반복 종료
    print(i, end=" ")
print()