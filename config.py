from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = getenv("BOT_TOKEN")
STORAGE_PATH: str = getenv("STORAGE_PATH")
UPDATE_TIME: int = int(getenv("UPDATE_TIME", default=5))
MONGO_URI: str = getenv("ME_CONFIG_MONGODB_URL", default="mongodb://mongo:27017")
