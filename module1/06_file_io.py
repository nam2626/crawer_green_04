# 파일 쓰기
# 1. 파일 열기
f = open('output.txt', 'w', encoding='utf-8')
# 2. 파일에 문자열 내용 출력
f.write('안녕하세요\n')
f.writelines(['ㅋㅋㅋㅋ','AAA','\n'])
f.write('1234567')
# 3. 파일 닫기
f.close()