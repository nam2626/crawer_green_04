# 함수 정의 및 호출
# 함수 및 if, 반복문 영역을 {} 쓰지않고, 들여쓰기 블록으로 구분
def greet(name):
    return f'안녕하세요, {name}님!' # js -> `안녕하세요 ${name}`

print(greet('홍길동'))

# 매개변수 기본값
def introduce(name,age,job='미정'):
    return f'이름: {name}, 나이: {age}, 직업: {job}'

print(introduce('홍길동',25))
print(introduce('김철수',30,'공무원'))

# 리턴 값을 여러개로 반환(tuple)
def get_min_max(numbers):
    return min(numbers), max(numbers)

print(get_min_max([1,2,3,4,5]))
print(get_min_max([1,2,3,4,5])[0],get_min_max([1,2,3,4,5])[1])
low, high = get_min_max([1,2,3,4,5])
print(low, high)

# 람다(lamda)
# 자바스크립트에서는 화살표함수
n = lambda x: x * 2 # const f = (x) => x * 2
print(n(3))

students = [
    {'name':'홍길동', 'score' : 90},
    {'name':'김철수', 'score' : 87},
    {'name':'박영희', 'score' : 77},
]

sorted_students = sorted(students, key=lambda s:s['score'], reverse=False)
print(sorted_students)