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