'''
여러 이미지를 합쳐서 하나의 이미지로 만들어주는 프로그램 제작 프로젝트

[사용자 시나리오]
1. 사용자는 합치려는 이미지를 1개 이상 선택한다.
2. 합쳐진 이미지가 저장될 경로를 지정한다.
3. 가로넓이, 간격, 포맷 옵션을 지정한다.
4. 시작 버튼을 통해 이미지를 합친다.
5. 닫기 버튼을 통해 프로그램을 종료한다.

[기능 명세]
1. 파일추가 : 리스트 박스에 파일 추가
2. 선택삭제 : 리스트 박스에서 선택된 항목 삭제
3. 찾아보기 : 저장할 폴더를 선택하면 텍스트 위젯에 입력
4. 가로넓이 : 이미지 넓이 지정(원본유지, 1024, 800, 640)
5. 간격 : 이미지 간의 간격 지정(없음, 좁게, 보통, 넓게)
6. 포맷 : 저장 이미지 포맷 지정(PNG, JPG, BMP)
7. 시작 : 이미지 합치기 작업 실행
8. 진행상황 : 현재 진행중인 파일 순서에 맞게 반영
9. 닫기 : 프로그램 종료
'''


from tkinter import *

root = Tk()
root.title("Combine Image Program") # 조건 1 - OK

# 파일 프레임(파일 추가, 선택 삭제 영역)
file_frame = Frame(root)
file_frame.pack()

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="파일추가")
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="선택삭제")
btn_del_file.pack(side="right")

root.resizable(False, False)
root.mainloop()