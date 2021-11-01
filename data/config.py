from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("bot_token")  # Забираем значение типа str
ADMINS = env.list("admins")  # Тут у нас будет список из админов

# База данных
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
HOST_PASS = env.str("host_pass")  # Забираем значение Пароля БД типа str
HOST_USER = env.str("host_user")  # Забираем значение Пользователя типа str
DB_NAME = env.str("db_name")  # Забираем значение имя БД типа str
