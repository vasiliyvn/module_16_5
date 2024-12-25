from fastapi import FastAPI, Path, status, HTTPException, Request, Body
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates

app = FastAPI()
# users = {'1': 'Имя: Example, возраст: 18'}
users = []
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
async def get_main_page(request: Request) -> HTMLResponse:
        return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}')
async def get_users(request: Request, user_id: Annotated[int, Path(ge=1, le=1000,
                                                    description='Enter userId', example='1')]) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='user was not found')


@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                                    description='Enter username', example='Vasya_User')],
                      age: int = Path(ge=18, le=120, description='Enter age', example=36)) -> List[User]:
    if len(users) == 0:
        User.id = 1
    else:
        User.id = users[len(users) - 1].id + 1
    users.append(User(id=User.id, username=username, age=age))
    return users


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: int,
                       username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age')]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_users(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail='User was not found')
#  python -m uvicorn module_16_5:app
