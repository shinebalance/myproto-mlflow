# 環境変数を参照
import os
# .env ファイルをロードして環境変数へ反映
# https://maku77.github.io/python/env/dotenv.html
from dotenv import load_dotenv


load_dotenv()
TARGET_URL = os.getenv('TARGET_URL')
CSV_SAVEPATH = os.getenv('CSV_SAVEPATH')
