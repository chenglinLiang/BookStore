from datetime import timedelta
import os

DEBUG = True

# session随机密钥(盐)
SECRET_KEY = os.urandom(24)

# session过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=7)