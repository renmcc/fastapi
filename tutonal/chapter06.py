from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

app06 = APIRouter()
"""OAuth2 密码模式和 FastAPI 的 OAuth2PasswordBearer"""
"""
OAuth2PasswordBearer是接收URL作为参数的一个类： 客户端会向该URL发送useranme和password参数，然后得到一个Token值
OAuth2PasswordBearer并不会创建相应的URL路径操作，只是指明客户端用来请求Token的URL地址
当请求到来的时候，FastAPI会检查请求的Authorization头信息，如果没有找到Authorization头信息，或者头信息的内容不是Bearer token，它会返回401状态码（UNAUTHORIZED）
"""

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/chapter06/token")


@app06.get("/oauth2_password_bearer")
async def oauth2_password_bearer(token: str = Depends(oauth2_schema)):
    return {"token": token}


"""基于 Password 和 Bearer token 的 OAuth2 认证"""

fake_users_db = {
    "john snow": {
        "username": "john snow",
        "full_name": "John Snow",
        "email": "johnsnow@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


@app06.post("/token")
async def login(form_data=Depends(OAuth2PasswordRequestForm)):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="无效的用户名或密码")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="无效的用户名或密码")
    return {"access_token": user.username, "token_type": "bearer"}


async def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def fake_decode_token(token: str):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")
    return current_user


"""OAuth2 with Password (and hashing), Bearer with JWT token 开发基于JSON Web Tokens的认证"""

fake_users_db.update({
    "john snow": {
        "username": "john snow",
        "full_name": "John Snow",
        "email": "johnsnow@example.com",
        "hashed_password":
        "$2b$12$4SF/lVF5fXCXiVblyD4g4uzQmb6Z702/iT1CQLeDualSCqSgwdEzC",
        "disabled": False
    }
})

# 生成密钥 openssl rand -hex 32
SECRET_KEY = "91443c1960849a7c8684368e3720b3a81a394a8b6c4ad18ae89b03ed84a2b152"
ALGORITHM = "HS256"  # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期分钟


class Token(BaseModel):
    """返回给用户的Token"""
    access_token: str
    token_type: str


# 加密用户的密码

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 创建提交用户名和密码的ui
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/chapter06/jwt/token")


def verity_password(plain_password: str, hashed_password: str):
    """
    对密码进行校验
    return: true | false
    """
    return pwd_context.verify(plain_password, hashed_password)


def jwt_get_user(db, username: str):
    """
    获取用户
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return False


def jwt_authenticate_user(db, username: str, password: str):
    """
    校验用户
    """
    user = jwt_get_user(db=db, username=username)
    if not user:
        return False
    if not verity_password(plain_password=password,
                           hashed_password=user.hashed_password):
        return False
    return user


def created_access_token(data: dict,
                         expires_delta: Optional[timedelta] = None):
    """
    创建token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # 加密的数据，混淆key，算法
    encoded_jwt = jwt.encode(claims=to_encode,
                             key=SECRET_KEY,
                             algorithm=ALGORITHM)
    return encoded_jwt


@app06.post("/jwt/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = jwt_authenticate_user(db=fake_users_db,
                                 username=form_data.username,
                                 password=form_data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="无效的用户名或密码",
                            headers={"WWW-Authenticate": "Bearer"})
    assess_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = created_access_token(data={"sub": user.username},
                                        expires_delta=assess_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


async def jwt_get_current_user(token: str = Depends(oauth2_schema)):
    """
    解析token获取用户
    """
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="证书校验失败",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token=token,
                             key=SECRET_KEY,
                             algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = jwt_get_user(db=fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def jwt_get_current_active_user(
        current_user: User = Depends(jwt_get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="不活跃的用户")
    return current_user


@app06.get("/jwt/users/me")
async def jwt_read_users_me(
        current_user: User = Depends(jwt_get_current_active_user)):
    return current_user
