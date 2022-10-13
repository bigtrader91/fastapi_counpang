## :rocket: Subject
쿠팡API를 활용한 간단한 쇼핑몰 구축

## :bell: Purpose

- Fastapi를 활용한 웹사이트 구축에 대한 이해

## 💾 Data
- 쿠팡API


## 📚 Tech Stacks
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python3.9.7](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Nginx](https://img.shields.io/badge/Nginx-%23DD0031.svg?style=for-the-badge&logo=Nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


## 🎬 프로젝트 기간 (2022.07.2 - 2022.07.15)

### Process

<img width="814" alt="image" src="https://user-images.githubusercontent.com/88607278/195484021-5f413cd2-ca69-4aea-9657-3b8a34dd7044.png">


### 1. 개발환경 세팅
- python 3.8
- gcp를 통해서 unbuntu20.04 서버생성(ssh접속)
- 

### 2. DB 구축(PostgreSQL & Docker)
- 선정이유 :간단한 프로젝트라 mysql로 구현하려고 했으나 이후 추천서비스나 별도의 복잡한 기능을 추가할 수 있으며, 
상품정보를 지속적으로 수집할 경우 데이터의 양의 방대해질 경우 대비)

#### Table
- search_table : 상품ID, 상품명, 이미지URL, 가격, 키워드
- category_table : 상품ID, 상품명, 이미지URL, 가격, 카테고리


### 3. 프론트엔드(Bootstrap)
- 기본적인 html,css를 통해서도 원하는 구조를 만들기 쉬움 

### 4. 백엔드(Fastapi와 Nginx)
- 선정이유 : Fastapi(Starlette)의 경우에 Django나 Flask 보다 속도 면에서 빠르기 때문에 선택하였으며
  Nginx의 경우 proxy서버를 통해서 보안상의 이점을 위해 선택



### 5. 배치작업(Crontab)
- 선정이유 : airflow의 경우 좀더 세밀한 작업이 가능하나, 사용중인 클라우드서버의 성능문제로 인해 제한적이며 
현재 서비스 자체가 매우 단순하여 선택함. 
- crontab을 통해서 지속적으로 데이터 적재(search_api 의 경우 시간당 요청수 제한)
- search_api의 경우 매일 8분 간격으로 검색키워드 바탕으로 데이터 수집후 DB에 적재함
- category_api의 경우 매월 1회 수집

### 6. 기타
- http -> https (Certbot을 통한 무료 SSL인증서 적용)
- robots.txt  & sitemap.xml 라우터 추가
- 애널리틱스 연결 통한 유저 데이터 수집
- 도메인 구매 및 웹사이트 등록

