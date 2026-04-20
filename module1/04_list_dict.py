# -- list(자바스크립트에서 배열) --
# 인덱스 번호로 사용
# []로 만듬, 인덱스 번호는 0부터 시작

fruits = ["사과", "바나나", "딸기"]
fruits.append("수박")
fruits.insert(1,"메론") # 1번 인덱스에 메론 삽입
print(fruits)

fruits.remove('사과')
print(fruits) # 리스트에 있는 사과 삭제

#        -10-9-8-7-6-5-4-3-2-1
#          0 1 2 3 4 5 6 7 8 9 
numbers = [1,2,3,4,5,6,7,8,9,10]
print(numbers[0],numbers[3])
# 리스트 마지막에 있는 값 출력
print(numbers[-1],numbers[-7])

print(numbers[0:5]) # 0 이상 5 미만 인덱스 범위의 요소 출력
print(numbers[5:]) # 5 이상 인덱스 범위의 요소 출력
print(numbers[:5]) # 0 이상 5 미만 인덱스 범위의 요소 출력
print(numbers[-1:]) # 마지막 요소 출력
print(numbers[-3:]) # 마지막 3개 요소 출력
print(numbers[::2]) # 0부터 끝까지 2씩 증가하는 인덱스의 요소 출력

# 특정 값이 리스트에 있는지 확인
print(5 in numbers) # True
print(11 in numbers) # False

# dict (자바스크립트 객체랑 동일)
# 키-값 쌍으로 데이터를 저장하는 자료구조(자바스크립트 객체, 맵,...)
# {}로 만들고, 키는 문자열로 이용

person = {"name": "홍길동", "age": 25, "city": "서울"}

print(person["name"],person["age"],person["city"])

del person["city"]
# 해당 키값이 없으면 에러처리
# print(person["name"],person["age"],person["city"])

person["email"] = "test@abc.com"
print(person)

print(person.keys())
print(person.values())
# dict 순회 방법
for key, value in person.items():
    print(key,'-',value)

# ── list of dict — 크롤링 결과 형태 ─────────────────────────
# 실제 크롤링에서 수집한 데이터는 대부분 이 형태로 저장됩니다.
# 하나의 dict = 한 건의 데이터, list = 전체 수집 결과

posts = {
    'query':'python',
    'date' : '2026-04-20 14:30:33',
    'resultCount' : 3,
    'items':[
        {"title": "Python 입문", "views": 1500, "date": "2026-04-19"},
        {"title": "크롤링 기초", "views": 3200, "date": "2026-04-18"},
        {"title": "DB 연동하기", "views": 870,  "date": "2026-04-17"},
    ]
}
print(posts)

for key in posts:
    if key == 'items':
        for item in posts[key]:
            print(item['title'],item['views'],item['date'])
    else:
        print(key,'-',posts[key])