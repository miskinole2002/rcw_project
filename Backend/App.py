from fastapi import FastAPI,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware
import snowflake.connector as sc
import uvicorn
from dotenv import load_dotenv
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .Functions import password_hash,password_verify
from.Models import Recruteurs,Candidats,Offres,log_candidat,log_recruteur,OByIdR,OByIdC,Acandidats,Arecruteurs

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
             INSERT INTO Easy_Rec.easy.Offres (titre, recruteur_id,salaire,description,comptences)  
            VALUES (%s, %s, %s, %s,%s)
        """ 
        params=[U.titre,U.recruteur_id,U.salaire,U.description,U.competences]
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
    sql = "SELECT recruteur_id, nom_entreprise,password FROM Easy_Rec.easy.Recruteurs where email=%s"

    # sql ="""SELECT r.recruteur_id,o.titre,o.salaire,o.description,o.competences FROM Easy_Rec.easy.Recruteurs r 
    #   left join Easy_Rec.easy.offres o on r.recruteur_id =o.recruteur_id  
    #   left join Easy_Rec.easy.Candidatures c  on c.offre_id =o.offre_id
    #   left join Easy_Rec.easy.Candidats a  on a.candidat_id =c.candidat_id
    #   where r.email=%s"""
    
    params=[U.email]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    print(resultat)
    if resultat is None : 
        response="email introuvable"
        return{"message": response}
    else:
       
        pwd_veri=password_verify(U.password,resultat[2])
      
        if pwd_veri:
                
                result={
                    "recruteur_id" : resultat[0], 
                    "nom_entreprise":resultat[1],
                    }
                
                response=result
        else:
                response="password invalide "
        
        return{"message":response} 

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

#pour recuperer les offres et le candidature qui sont lies aux recruteurs
@app.post("/get_offre_by_idRecruteur")
async def get_offre_byId(U:OByIdR):
    sql ="""SELECT r.nom_entreprise,o.titre,o.salaire,o.description,o.competences ,a.cv,c.lettre_motivation FROM Easy_Rec.easy.Recruteurs r 
      left join Easy_Rec.easy.offres o on r.recruteur_id =o.recruteur_id  
      left join Easy_Rec.easy.Candidatures c  on c.offre_id =o.offre_id
      left join Easy_Rec.easy.Candidats a  on a.candidat_id =c.candidat_id
      where r.recruteur_id=%s"""
    params=[U.recruteur_id]
    cursor.execute(sql,params)
    resultat=cursor.fetchall()
    response=[]
    for row in resultat:
        result={
           
            "nom_entreprise":row[0],
            "titre":row[1],
            "salaire":row[2],
            "description":row[3],
            " competences":row[4],
            "cv":row[5]
        }
        response.append(result)
    return{"message":response}

#pour recuperer les offres aux quelles les candidats ont postustees 
@app.post("/get_offre_by_idcandidat")
async def get_offre_byIdC(U:OByIdC):
    sql ="""SELECT o.titre,o.salaire,o.description,0.competences FROM Easy_Rec.easy.candidutres c
     join offre o on c.offre_id=o.id
      where c.candidat_id=%s"""
    params=[U.candidat_id]
    cursor.execute(sql,params)
    resultat=cursor.fetchall()
    response=[]
    for row in resultat:
        result={
            "titre":row[0],
            "salaire":row[1],
            "description":row[2],
            " competences":row[3],
        }
        response.append(result)
    return{"message":response}

#pour ajouter un abonnement recruteurs

@app.post("./abonnement_recruteurs")
async def Abonnement_recruteur(U:Arecruteurs):
    current_time=datetime.now()
    future_tinme=current_time+ relativedelta(years=1)
    begin_date=current_time.strftime("%d-%m-%y")
    end_date=future_tinme.strftime("%d-%m-%y")
     

    sql = """
        INSERT INTO Easy_Rec.easy.abonnement_recruteurs (recruteur_id,date_debut,date_fin,forfait)  
        VALUES (%s, %s, %s, %s)
        """ 
    
    params=[U.recruteur_id,begin_date,end_date,U.forfait]
    cursor.execute(sql,params)
    return{"message":"Ok"}

#abonnement candidat

@app.post("./abonnement_candidats")
async def Abonnement_candidat(U:Acandidats):
    current_time=datetime.now()
    future_tinme=current_time+ relativedelta(years=1)
    begin_date=current_time.strftime("%d-%m-%y")
    end_date=future_tinme.strftime("%d-%m-%y")
     

    sql = """
        INSERT INTO Easy_Rec.easy.abonnement_candidats (recruteur_id,date_debut,date_fin,forfait)  
        VALUES (%s, %s, %s, %s)
        """ 
    
    params=[U.recruteur_id,begin_date,end_date,U.forfait]
    cursor.execute(sql,params)
    return{"message":"Ok"}

# recherche de l'abonnement en fonction de recruteur_id
@app.get("./get_abonnement_By_Rid")
async def get_AbonnementByIDdR(recruteur_id:str):

    sql = """SELECT forfait,date_debut,date_fin FROM Easy_Rec.easy.abonnement_recruteurs where recruteur_id=%s"""
    params=[recruteur_id]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    response={
        'forfait':resultat[0],
        'date_debut':resultat[1],
        'date_fin':resultat[2]
    }


    return{'message':response}

# recherche de l'abonnement en fonction de candidat_id
@app.get("./get_abonnement_By_Rid")
async def get_AbonnementByIDCan(candidat_id:str):

    sql = """SELECT forfait,date_debut,date_fin FROM Easy_Rec.easy.abonnement_candidats where candidat_id=%s"""
    params=[candidat_id]
    cursor.execute(sql,params)
    resultat=cursor.fetchone()
    response={
        'forfait':resultat[0],
        'date_debut':resultat[1],
        'date_fin':resultat[2]
    }


    return{'message':response}

    






        
    



if __name__=="__name__":
    uvicorn.run(app,host="0.0.0.0", port=8000,workers=1)