from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from db.db import session
from model.model import UserTable, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 전체 리스트
@router.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    context={}
    users = session.query(UserTable).all()

    context["request"] = request
    context["users"] = users

    return templates.TemplateResponse("user_list.html", context)



# 특정 인원 보기
@router.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(request: Request, user_id: int):
    context={}
    user = session.query(UserTable).filter(UserTable.id == user_id).first()

    context["request"] = request
    context["name"] = user.name
    context["age"] = user.age

    return templates.TemplateResponse("user_list.html", context)

# 인원 생성
@router.post("/user")
async def create_user(
        name: str = Form(...),
        age:int = Form(...)):

    print(name, age)
    user = UserTable()
    user.name = name
    user.age = age

    session.add(user)
    session.commit()

    return RedirectResponse(url="/users", status_code=302)

# 인원 수정
@router.post("/users", response_class=HTMLResponse)
async def update_user(
        user_id: int = Form(...),
        n_name: str = Form(...),
        n_age: int = Form(...)):

    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    user.name = n_name
    user.age = n_age
    print(n_name, n_age)
    session.commit()

    return RedirectResponse(url="/users", status_code=302)


# 인원 삭제
@router.post("/delete/{user_id}", response_class=HTMLResponse)
async def delete_users(request: Request, user_id: int):

    print('delete', user_id)
    session.query(UserTable).filter(UserTable.id == user_id).delete()
    session.commit()

    return RedirectResponse(url="/users", status_code=302)

    