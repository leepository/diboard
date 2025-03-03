# FastAPI Board with dependency injector

FastAPI framework에 dependency injector를 적용한 간단한 게시판. 지원되는 기능은 다음과 같다.

 - JWT를 이용한 회원 로그인, 로그 아웃 기능
 - 회원 추가 및 삭제 (수정 기능은 미구현)
 - 간단한 글쓰기
 - 첨부파일 추가 기능 (갯수 무제한)
 - Tag 추가 기능 (갯수 무제한)
 - 대댓글 기능 (Depth=1까지만 지원함)

## Requirements

해당 게시판 코드를 사용하기 위해서는 다음과 같은 AWS Resource 설정이 필요하다.

 - AWS Secrets manager : 다음과 같은 Application 설정값을 저장한다.
	 - diboard/db/cache : Redis 접속 정보
	 - diboard/db/mariadb : MariaDB 접속 정보
	 - diboard/test-user : 테스트 유저 로그인 정보
 - AWS S3 : 첨부 파일을 저장한다.
	 - Bucket name : diboard-uploaded-files

게시판에 사용된 DB는 Docker container를 local에서 실행되며 다음과 같이 구성되어 있다.

 - MariaDB : 회원 정보 저장, 게시판 정보 저장
 - Redis : 회원 로그인 정보 저장

## Packages

게시판 구현에 사용된 python version은 3.11이며 python package는 다음과 같다.

 
	boto3==1.35.90   
	dependency-injector==4.44.0  
	fastapi==0.115.6  
	fastapi-pagination==0.12.34   
	pycryptodome==3.21.0  
	pydantic==2.10.4  
	PyMySQL==1.1.1  
	pytest==8.3.4   
	python-jose==3.3.0  
	python-multipart==0.0.20  
	redis==5.2.1  
	SQLAlchemy==2.0.36  
	ujson==5.10.0  

## Run application

Application은 다음과 같이 구동한다. 

    $ source .venv/bin/activate
    $(.venv) python run.py

## Pytest

Application에 대한 pytest는 API단 테스트로 구성되어 있으며 다음과 같이 구동한다.

    $ pytest ./app/tests

