from passlib.context import CryptContext


SECRET_KEY = "91443c1960849a7c8684368e3720b3a81a394a8b6c4ad18ae89b03ed84a2b152"
ALGORITHM = "HS256"  # 算法

# 加密用户的密码
abc = CryptContext(['bcrypt']).encrypt('secret')
print(abc)
