import os
import dotenv

dotenv.load_dotenv()

PORT = os.getenv("PORT")
ATLAS_USER = os.getenv("ATLAS_USER")
ATLAS_PASS = os.getenv("ATLAS_PASS")


mongo_url = f"mongodb+srv://{ATLAS_USER}:{ATLAS_PASS}@bdmlpt0521midproject.tgi9t.mongodb.net/"
