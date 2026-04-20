import csv

data = [
    {"name": "김철수", "score": 85, "grade": "B"},
    {"name": "이영희", "score": 92, "grade": "A"},
    {"name": "박민준", "score": 78, "grade": "C"},
]
# csv 파일로 저장하기
with open('student.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.DictWriter(f,fieldnames=['name','score','grade'])
    writer.writeheader(); # 첫 줄에 컬럼명을 파일에 쓰기
    writer.writerows(data)
print('csv 저장 완료')

# csv 파일 읽어오기
list = []
with open('student.csv','r',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
        list.append(row)
print(list)