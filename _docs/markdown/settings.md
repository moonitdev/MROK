# Python

## install python[miniconda]


# Visual Studio Code

## install vsc

## install extensions

## set preferences


# Google Drive



# Git

## github 회원 가입
- [Github Home](https://github.com/)
- Sign Up

## Git 설치
- 
-

## MATS 저장소 설치

### remote
- Create a new (private) repository
  * [hopelife/MATS](https://github.com/hopelife/MROK.git)
- [More Detail Tutorial]()

### local

- clone remote repository
```
C:\> cd C:\dev\projects
C:\dev\projects\> git clone https://github.com/hopelife/MROK.git
```

# 가상 환경 설치(python)

## 리눅스, osx
### 가상환경 모듈 설치
$ pip install virtualenv

### 가상환경 만들기
$ virtualenv vrok

### 가상환경 
$ source vrok/bin/activate
(venv) $ pip list


## 윈도우 환경

> pip install virtualenv
> virtualenv vrok
이제 activate해야 하는데, 여기서는 source 대신 call


C:\Dev\docMoon\projects\MROK> call venv/scripts/activate
(venv) > pip list


# Python Packages


# mongoDB

## 설치

## admin 계정 만들기

- [MongoDB 에서 admin 만들기](https://ijeee.tistory.com/12)
- [MongoDB 관리자 계정 추가/삭제하기](http://blog.freezner.com/archives/1040)

```
> use admin

db.createUser(
  {
    user: "trader",
    pwd: "Trader1",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
```

# googleDrive

## gspread
- [gspread를 이용하여 Python에서 구글 시트 연동하기](https://yurimkoo.github.io/python/2019/07/20/link-with-googlesheets-for-Python.html)
- [구글 계정 접속 권한 얻기](https://newsight.tistory.com/288)


# Slack



# Others

## [Slack](https://slack.com/intl/en-kr/)

## [Advanced REST Client](https://advancedrestclient.com/)


MROK> virtualenv venv
MROK> call venv/scripts/activate




### python 패키지 설치
 
#### pyautogui
 
- GUI 
```
pip3 install pyautogui
```
 
 
#### opencv
 
 
```
pip uninstall opencv-contrib-python
pip uninstall opencv-python
 
# 가상환경인 경우
pip3 install opencv-contrib-python==3.4.2.16
 
# 가상환경이 아닌 경우
pip install --user opencv-contrib-python==3.4.2.16
```
 
#### gspread / oauth2client
```
# 가상환경인 경우
pip3 install gspread
pip3 install --upgrade oauth2client
 
# 가상환경이 아닌 경우
pip install --user gspread
pip install --user --upgrade oauth2client
```
 
#### pytesseract
 
- https://github.com/UB-Mannheim/tesseract/wiki

##### osx

```


brew install tesseract


sudo chown -R macmini /usr/local/share/Library/Caches/Yarn/v4


brew install tesseract-lang

brew list tesseract



/usr/local/Cellar/tesseract/4.1.1/bin/tesseract
/usr/local/Cellar/tesseract-lang/4.0.0/share/tessdata/

```


```
pip install matplotlib

pip install pyautogui
pip install pynput
pip install pytesseract




```


#### 
 
## Visual Studio Code