# Bare minimum for Telegram Bot

## 📋 Opportunities:

- **Start** + **Support** (to tg channel) + **Help**
- **Logging**
- **Database** (SQLite)
- **Admin panel:**
  - user search by ID or username;
  - ability to ban and unban a user;
  - the ability to write to a specific user from a bot or make a mailing list;
  - view active bans;
  - view the latest logs directly in the bot
---
## 🚀 Quick start:

### Prerequisites
- Python 3.12+
- Poetry (`pip install poetry`)
###
```
git clone https://github.com/vankaspr/bare-minimun-for-tg-bot.git
cd bare-minimun-for-tg-bot
cp .env.example .env
# Edit .env with your values
poetry install
```
_Environment variables (.env)_
```
# Токен можно получить в ТГ-боте @BotFather
BOT_TOKEN=<your-bot-token>

# Канал, куда будут направляться сообщения с /support хендлера
SUPPORT_GROUP_ID=<your-support-channel-id>

# ID админа
ADMIN=<your-admin-id>

# URL Базы данных
DATABASE_URL=<your--asyncio-bd-url>
```
_Alembic (alembic.ini)_
```
# URL Базы данных
sqlalchemy.url = <your--asyncio-bd-url>
```
```
poetry run python src/main.py
```

---
## 📁 Project structure:
###
```
bare-minimun-for-tg-bot/
├── data/                           # Файлики с БД и логами
    ├── bd/                         # data/ создаётся при первом запуске
        ├── bot.db                  
    ├── logs/
        ├── bot.log 
├── src/
    ├── alembic/                    
    ├── core/                  
        ├── filters/                # Бан-чек и админ-чек
        ├── handlers/
            ├── admin/              # Хендлеры для админ-панели
            ├── user/               # Хендлеры для юзера
        ├── keyboards/
        ├── middlewares/            # Мидлвары для банов, логов и БД
        ├── services/
        ├──utilities/               
    ├── database/                   # настройка БД, модели, CRUD
    ├── settings/                    
        ├── loader.py          
    ├── confih.py                   # Пути к папкам + загрузка из env
    ├── main.py                     # Настройка бота (точка входа)  
├── Dockerfile
├── docker-compose.yml
├── .env.example       
├── alembic.ini             
...    
└── pyproject.toml                  # Конфигурация Poetry
```


