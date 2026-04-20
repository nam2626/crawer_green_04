# ======================================================
# 실습 1 — list와 dict 다루기
# 교시: 2교시 (JS vs Python 비교)
# 제한시간: 5분
# ======================================================

students = [
    {"name": "김철수", "score": 85},
    {"name": "이영희", "score": 92},
    {"name": "박민준", "score": 78},
]

# 문제 1. 학생 수를 출력하세요.
# 기대 출력: 3
print(len(students)) # len ->(리스트, 문자열) 개수


# 문제 2. 두 번째 학생의 이름을 출력하세요.
# 기대 출력: 이영희
print(students[1]["name"])


# 문제 3. 모든 학생의 이름과 점수를 아래 형식으로 출력하세요.
# 기대 출력:
# 김철수: 85점
# 이영희: 92점
# 박민준: 78점
for student in students:
    print(f"{student['name']}: {student['score']}점")


# 문제 4. (도전) 평균 점수를 출력하세요.
# 힌트: sum([85, 92, 78]) / 3
# 기대 출력: 평균: 85.0점
# list comprehension: [표현식 for 변수 in 리스트] → 새 리스트 생성
# 풀어쓰면: for student in students: scores.append(student["score"])
scores = [student["score"] for student in students]
print(f"평균: {sum(scores) / len(scores)}점")
