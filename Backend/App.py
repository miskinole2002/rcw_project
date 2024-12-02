from fastapi import FastAPI,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware
import snowflake.connector as sc
import uvicorn
from dotenv import load_dotenv
import os
from .Functions import password_hash,password_verify
from.Models import Recruteurs,Candidats,Offres,log_candidat,log_recruteur

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
cursor=conn.cursor()

@app.post("/register_recruteur")

async def Recruteur_register(U:Recruteurs):

    sql = "SELECT * FROM Easy_Rec.easy.Recruteurs where email=%s"
    params=[U.email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone() 
    if resultat:
        return{"message":" email deja existant "}
    else:
        cursor.execute(sql,params)
        pwd_hash=password_hash(U.password)
        sql = """
        INSERT INTO Easy_Rec.easy.Recruteurs (nom_entreprise, email, password)
        VALUES (%s, %s, %s)
        """ 
        params=[U.nom_entreprise,U.email,pwd_hash]
        cursor.execute(sql,params)
        return{"message":"utilisateur bien  ajoute"}

@app.post("/register_candidat")
async def Candidat_register(U:Candidats):

    sql = "SELECT * FROM Easy_Rec.easy.Candidats where email=%s"
    params=[U.email]
    print(params)
    cursor.execute(sql,params)
    resultat=cursor.fetchone() 
    print(resultat)
    if resultat:
        return{"message":" email deja existant "}
    else:
        pwd_hash=password_hash(U.password)
        sql = """
        INSERT INTO Easy_Rec.easy.Candidats (nom, prenom, email, password, cv)
        VALUES (%s, %s, %s, %s, %s)
        """ 
        params=[U.nom,U.prenom,U.email,pwd_hash,None]
        x=cursor.execute(sql,params)
        
        return {"message":"utilisateur bien ajouter"}

@app.post("/offres")
async def Offre_add(U:Offres):
    
        sql = """
             INSERT INTO Easy_Rec.easy.Offres (titre, recruteur_id,salaire,description)
            VALUES (%s, %s, %s, %s, %s)
        """ 
        params=[U.titre,U.recruteur_id,U.salaire,U.description]
        x=cursor.execute(sql,params)
        return{"message":"offres bien ajoutes"}

@app.get("/")
async def Get_offre():
    sql = "SELECT * FROM Easy_Rec.easy.Offres"
    cursor.execute(sql)
    resultat=cursor.fetchall() 
    return{"response":resultat}

@app.post("/log_recruteur")
async def Recruteur_login(U:log_recruteur):
    sql = "SELECT * FROM Easy_Rec.easy.Recruteurs where email=%s"
    params=[U.email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    if resultat==None:
        response="email invalide"
        return{"message": response}
    else:
        pwd_veri=password_verify(U.password,resultat[3])
    
        if pwd_veri:
            response=resultat
        else:
            response="password invalide "

    return{"message": response}

@app.post("/log_candidat")
async def Recruteur_login(U:log_candidat):
    sql = "SELECT * FROM Easy_Rec.easy.Candidats where email=%s"
    params=[U.email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    if resultat==None:
        response="email invalide"
        return{"message": response}
    else:
        pwd_veri=password_verify(U.password,resultat[3])
        print(pwd_veri)
        if pwd_veri:
            response=resultat
        else:
            response="password invalide "
    
    
   
    return{"message":response}

@app.post("/upload_cv")
async def Upload_cv(file:UploadFile=File(...)):
    
    content_Type = {"application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
    if file.content_type not in content_Type:
        response='format de fichier non valide'
    else:
        path_dir="Backend\Cvs"
        path=rf"{os.path.join(path_dir,file.filename)}"
        
        candidat_id=201
        sql = """
             update Easy_Rec.easy.Candidats set cv =%s where candidat_id =%s
        """ 
        params=[path,candidat_id] 
        cursor.execute(sql,params)

        with open(path,"wb")as f:

            content= await file.read()
            f.write(content)
            response=file.filename

    return{'response':response}



        
    



if __name__=="__name__":
    uvicorn.run(app,host="0.0.0.0", port=8000,workers=1)