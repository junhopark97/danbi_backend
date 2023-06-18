# danbi_backend


## 기술 스택
* python == 3.10.4
* django == 4.2.2
* djangorestframework == 3.14.0
* djangorestframework-simplejwt == 5.2.2
* pytest==7.3.2
* pytest-django==4.5.2

<hr />

# API Document

## USER
|기능|Http Method| API |
|---|---|----------------|
|회원가입|POST| /users/register|
|로그인|POST|/users/login|


## TASK
|기능|Http Method| API |
|---|---|----------------|
|업무 조회|GET|/tasks|
|업무 생성|POST| /tasks |
|업무 수정|PUT|/tasks/ <int: task.id>|

## SUBTASK
|기능|Http Method| API |
|---|---|----------------|
|하위 업무 완료 처리|PATCH|/subtasks/<int: subtask.id>|
|하위 업무 삭제|DELETE|/subtasks/<int: subtask.id>|
