from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import snowflake.connector as sc
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
 
app.add_middleware ( CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# connexion a la base de donnee 



conn= sc.connect(
    user=os.getenv('snowflake_user'),
    password=os.getenv('snowflake_password'),
    account =os.getenv('snowflake_account'),
    database=os.getenv('snowflake_database'),
   
)

if conn :
    print('connection reussie')




if __name__=="__name__":
    uvicorn.run(app,host="0.0.0.0", port=8000,workers=1)