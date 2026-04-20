name = '홍길동'
age = 20
is_student = True
score = None

print(name,age,is_student,score)

# type()으로 변수 타입을 확인 가능
print(type(name))
print(type(age))
print(type(is_student))
print(type(score))

# -- 문자열 기본적인 조작 --
# 문자열 메서드는 원본을 바꾸지 않고 새 문자열로 반환
greetring = '   안녕하세요 Hello   '
print(greetring.strip()) # 앞뒤 공백 제거
print(greetring.strip().upper()) # 알파벳 대문자 변환
print(greetring.strip().lower()) # 알파벳 소문자 변환
print(len(greetring)) # 문자열 길이(공백 포함)
print(len(greetring.strip()))

url = 'https://example.com/board?page=1'
print(url.split('?')) # ?를 기준으로 분리 -> 리스트로 반환
print(url.split('?')[1])
arr = url.split('?')
print(arr[len(arr)-1])
print(url.replace('https','http')) # https -> http로 변환

# in을 이용해서 특정 문자열 포함 여부를 확인 가능
print('example' in url)
print('example1' in url)
