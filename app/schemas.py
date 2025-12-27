from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        from_attributes = True


class UserReadWithPosts(BaseModel):
    id: int
    name: str
    age: int
    posts: list[PostRead]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str
    age: int


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: str
    content: str


class LoginRequest(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
