import os
import dotenv

dotenv.load_dotenv()

PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASS = os.getenv("PASS")

mongo_url = f"mongodb+srv://{USER}:{PASS}@bdmlpt0521midproject.tgi9t.mongodb.net/"

