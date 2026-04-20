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