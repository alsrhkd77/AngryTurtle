"""
AngryTurtle
2018. 10. 23
동의대학교 컴퓨터 소프트웨어 공학과
20153308 송민광

이미지 출처
병아리 - https://m.blog.naver.com/lovedesign01/150168487961
토끼 - http://m.inven.co.kr/board/powerbbs.php?come_idx=4538&l=3232417&iskin=overwatch
박스 - https://social.lge.co.kr/product/795_/
"""

import turtle
import random
import math

turtle.title("Angry Turtle")

IMGList = ["box.gif","bird.gif","rabbit.gif","chick1.gif","chick2.gif","chick3.gif","chick4.gif"]
Box = []
Enemy = []



##############    적, 박스 이미지가 없을 때 대체할 함수
##############  주석풀고 아래쪽 함수 두개 주석 후 사용가능
"""
#박스 생성
for x in range(5):
    t = turtle.Turtle()                 
    Box.append(t)                       #리스트에 터틀 객체를 넣어준다
    Box[x].shape("square")
    Box[x].shapesize(2,2,1)
    Box[x].up()
    Box[x].hideturtle()
    Box[x].setposition(0,-260)
    t = None                            #객체를 삭제한다

#적 생성
for x in range(5):
    temp = random.randrange(1,7)
    t = turtle.Turtle()
    Enemy.append(t)
    Enemy[x].shape("circle")
    Enemy[x].shapesize(2,2,1)
    Enemy[x].up()
    Enemy[x].hideturtle()
    Enemy[x].setposition(0,-260)
    t = None
"""
################################################################



#박스 생성
for x in range(5):
    turtle.register_shape(IMGList[0])   #터틀모양을 이미지로 대체한다
    t = turtle.Turtle()                 
    Box.append(t)                       #리스트에 터틀 객체를 넣어준다
    Box[x].shape(IMGList[0])
    Box[x].up()
    Box[x].hideturtle()
    Box[x].setposition(0,-260)
    t = None                            #객체를 삭제한다

#적 생성
for x in range(5):
    temp = random.randrange(1,7)
    turtle.register_shape(IMGList[temp])    #터틀모양을 이미지로 대체한다
    t = turtle.Turtle()
    Enemy.append(t)
    Enemy[x].shape(IMGList[temp])
    Enemy[x].up()
    Enemy[x].hideturtle()
    Enemy[x].setposition(0,-260)
    t = None

#거북이 속성
class BulletInfo:
    def __init__(self, inturtle):   #생성자
        self.bullet = inturtle #터틀객체 삽입
        self.bullet.shape("turtle")
        self.bullet.color("green")
        self.bullet.up()
        self.speed = 0  #속도
        self.accel = 1  ###########느릴경우 이거 올리기
        self.head = 0   #방향
        self.live = True    #생사여부
        self.hit = False    #적중여부

    def __del__(self):
        self.bullet = None  #객체 삭제

    def SetStage(self, Stage, Enemy):   #Stage값과 Enemy리스트 가져오기
        self.Enemy = Enemy
        self.Stage = Stage

    def CrushJudgment(self):        #충돌 계산
        for x in Enemy:
            if(self.bullet.distance(x.position())<30): #적 적중 성공 시(hit True로 바꾸고 True리턴)
                x.up()
                x.setposition(0,-250)
                x.hideturtle()
                self.hit = True
                self.bullet.hideturtle()
                return True
                break   #필요한가?
            #상자 충돌 판단(hit는 그대로 놔두고 True리턴)
            elif(self.Stage != 1 and self.bullet.xcor()<-90 and self.bullet.xcor()>-125 and self.bullet.ycor()>-210 and self.bullet.ycor()<(-210 + ((self.Stage//2) * 40))):
                self.bullet.hideturtle()
                return True
                break   #필요한가?
            else:
                pass
        return False    #충돌 없을 시 False리턴

    #마우스로 거북이 당겼을 때
    def PullBullet(self,x,y):
        if(x>-440 and x< -300 and y>-220 and y<-120):
            self.bullet.goto(x,y)   #마우스 좌표로 거북이 이동
        self.head = math.degrees(math.atan((-(self.bullet.ycor()+130))/(-(self.bullet.xcor()+290))))    #거북이 방향 계산
        self.bullet.setheading(self.head)   #거북이 방향 설정
        self.speed=(self.bullet.distance(-290,-130)/10) #속도 설정

    #마우스 버튼 뗏을 떄
    def ShootBullet(self,x,y):
        
        while(self.bullet.ycor()>-250): #바닥보다 큰 동안만 반복
            if(self.speed>10):  #속도가 10보다 커지지않도록 제한
                self.bullet.speed(10)
            else:
                self.bullet.speed(int(self.speed))
                
            self.bullet.forward(self.speed * 1 * self.accel)    #앞으로 진행
            
            #유사 중력
            if(self.speed < 5.0):   #속도가 작을 때 더 많이 하강
                self.bullet.right(3 * self.accel)
            else:
                self.bullet.right(1 * self.accel)
                
            #속도 조절
            if(self.bullet.heading()>270 and self.bullet.heading()<360):    #떨어질때 가속
                self.speed = self.speed + (0.1 * self.accel)
            else:                                                           #올라갈때 감속
                self.speed = self.speed - (0.1 * self.accel)
            if(self.speed < 3.0):
                self.speed = 3.0
            if self.CrushJudgment():        #충돌 판정
                break
            if(self.bullet.ycor()<=-250):
                break
                
        if self.hit == False:
            self.bullet.color("red")    #바닥에 충돌한 애는 빨강
        self.live = False   

#땅 만들기 클래스
class MakeGround:
    Creator = turtle.Turtle()
    def __init__(self):
        #터틀 속성 설정
        self.Creator.shape("turtle")
        self.Creator.speed(0)
        self.Creator.up()
        
    def __del__(self):
        self.Creator = None

    #바닥 그리기
    def DrawGround(self):
        self.Creator.showturtle()   #갈색배경
        self.Creator.setposition(480,-250)
        self.Creator.down()
        self.Creator.begin_fill()
        self.Creator.color("#8E4E32")
        self.Creator.setposition(480,-400)
        self.Creator.setposition(-480,-400)
        self.Creator.setposition(-480,-250)
        self.Creator.end_fill()

        self.Creator.up()           #초록색 배경
        self.Creator.setposition(480,-250)
        self.Creator.down()
        self.Creator.setposition(-480,-250)
        self.Creator.begin_fill()
        self.Creator.color("green")
        self.Creator.setposition(-480,-280)
        while(self.Creator.xcor()<=480):
            angle=random.randrange(0,90)
            if(self.Creator.ycor()>-290):
                self.Creator.setheading(300)
                self.Creator.forward(random.randrange(1,10))
                self.Creator.setheading(0)
            elif(self.Creator.ycor()<-350):
                self.Creator.setheading(60)
                self.Creator.forward(random.randrange(1,10))
                self.Creator.setheading(0)
            else:
                self.Creator.setheading(-(angle-45))
                self.Creator.forward(50)
                self.Creator.setheading(0)
        self.Creator.setheading(90)
        self.Creator.setposition(480,-250)
        self.Creator.setheading(0)
        self.Creator.end_fill()
        self.Creator.hideturtle()
        self.Creator.up()

    #새총그리기
    def DrawShooter(self):
        self.Creator.showturtle()
        self.Creator.color("#8E6E61")
        self.Creator.down()
        self.Creator.begin_fill()
        self.Creator.setposition(-300,-250)
        self.Creator.setposition(-280,-250)
        self.Creator.setposition(-280,-200)
        self.Creator.setheading(0)
        for x in range(0,90):
            self.Creator.left(1)
            self.Creator.forward(1)
        self.Creator.forward(25)
        self.Creator.setheading(180)
        self.Creator.forward(20)
        self.Creator.left(90)
        self.Creator.forward(25)
        for x in range(0,90):
            self.Creator.right(1)
            self.Creator.forward(0.5)
        self.Creator.forward(40)
        for x in range(0,90):
            self.Creator.right(1)
            self.Creator.forward(0.5)
        self.Creator.forward(25)
        self.Creator.setheading(180)
        self.Creator.forward(20)
        self.Creator.left(90)
        self.Creator.forward(25)
        for x in range(0,90):
            self.Creator.left(1)
            self.Creator.forward(1)
        self.Creator.setposition(-300,-200)
        self.Creator.setposition(-300,-250)
        self.Creator.end_fill()
        self.Creator.hideturtle()


#박스 위치 지정
def SetBox(Stage, Box):
    for x in range(0, (Stage)//2):
        Box[x].showturtle()
        Box[x].up()
        Box[x].setposition(-100,-230+(40*x))
        

#타겟 위치 지정
def SetEnemy(Stage, Enemy):
    poslist = []
    poslist.append(random.randrange(0,440))
    for x in range(1, ((Stage+1)//2)):
        while(True):
            temp = random.randrange(0,440)
            for y in poslist:
                if( y<temp+40 and y>temp-40):
                    temp = -1
                    break;
            if(temp != -1):
                poslist.append(temp)
                break
    ind = 0
    for z in poslist:
        Enemy[ind].showturtle()
        Enemy[ind].up()
        Enemy[ind].setposition(poslist[ind],-230)
        ind = ind+1
    #메모리 반환
    del poslist
    

#Stage 출력
def WriteStage(Stage):
    turtle.up()
    turtle.setposition(0,260)
    turtle.write("Stage:", True, align="Center", font=("Arial", 15, "normal"))
    turtle.setposition(50,260)
    turtle.color("white")
    turtle.begin_fill()
    turtle.circle(10)
    turtle.end_fill()
    turtle.color("black")
    turtle.write(Stage, True, align="Center", font=("Arial", 15, "normal"))
    turtle.hideturtle()


def GameInfo():
    print("20153308 송민광")
    print("주의사항 : 1. 시작 시 초반 이미지 로딩 및 위치 설정때문에 시간이 조금 걸립니다.")
    print("              조금만 기다려 주세요")
    print("           2. 드래그 시 거북이가 가만히 있을때 까지 기다렸다가 마우스를 떼 주세요")
    print()
    print("게임방법: 1. 시작 할 스테이지를 입력해주세요.")
    print("              (1~10까지 입력가능)")
    print("          2. 거북이를 마우스 왼쪽버튼으로 드래그 후 떼면 발사")
    print("          3. 상자를 피해 캐릭터를 모두 맞추면 다음스테이지로 넘어갑니다")
    

######################main
GameInfo()

Stage = 1
NowB = 0

#빨리그려지게하기
turtle.delay(0)

#배경 그리기 호출
backGround = MakeGround()
backGround.DrawGround()
backGround.DrawShooter()

del backGround  #객체삭제 = 메모리 반환

turtle.delay(2)

#시작할 스테이지 팝업 띄우기(int로 받는다)
Stage = int(turtle.numinput("스테이지 설정","시작 할 스테이지를 입력하세요(1 ~ 10)", default=1, minval = 1, maxval = 10))

StartStage = True
hitCount = 0

###############################################게임시작
while(NowB < 10):   #무한루프(NowB가 10까지 안올라가고 올라가서는 안됨)
    hitCount = 0

    #초기화
    if StartStage:
        StartStage = False
        WriteStage(Stage)   #스테이지 출력
        for e in (Enemy):   #적 위치 초기화
            e.setposition(0,-260)
        for b in (Box):     #상자위치 초기화
            b.setposition(0,-260)
        SetBox(Stage, Box)  #스테이지에 맞는 상자위치 설정
        SetEnemy(Stage, Enemy)  #스테이지에 맞는 적 위치 설정
        Bullet = [] #리스트 선언
        for x in range (0,5):
            t = turtle.Turtle()
            Bullet.append(BulletInfo(t))    #리스트에 객체 삽입
            Bullet[x].SetStage(Stage, Enemy)    #객체에 스테이지, 적 리스트 삽입
            del t
    
    NowB = 0
    for c in Bullet:    #사용할 탄환 탐색
        if c.live:      #탄환 살아있으면 탈출
            break
        else:
            NowB = NowB + 1 #다음번호로

    if(NowB==5 and StartStage == False):    #end flag
        break
    
    check = 0
    for x in range (NowB, 5):   #탄환 위치 설정
        if(check==0):
            Bullet[x].bullet.setposition(-290,-130)
            check = check + 1
        elif(check==1):
            Bullet[x].bullet.setposition(-370,-240)
            check = check + 1
        elif(check==2):
            Bullet[x].bullet.setposition(-410,-240)
            check = check + 1
        elif(check==3):
            Bullet[x].bullet.setposition(-370,-220)
            check = check + 1
        elif(check==4):
            Bullet[x].bullet.setposition(-410,-220)
            check = check + 1
        else:
            pass

    NowBullet = Bullet[NowB]    #사용할 터틀 객체 설정
    
    #마우스 입력
    NowBullet.bullet.ondrag(NowBullet.PullBullet)
    NowBullet.bullet.onrelease(NowBullet.ShootBullet)

    for c in Bullet:    #적중 카운트
        if c.hit:
            hitCount = hitCount + 1
            
    if hitCount == ((Stage+1)//2):  #success flag
        Stage = Stage + 1
        for t in range(5):
            Bullet[t].bullet.hideturtle()
            Bullet[t] = None
        del Bullet
        StartStage = True
        
############################################게임 종료

turtle.up()
turtle.setposition(0,150)
turtle.color("red")
turtle.write("Fail", True, align="Center", font=("Arial", 30, "normal"))
