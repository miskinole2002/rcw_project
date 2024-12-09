from pydantic import BaseModel


class Recruteurs(BaseModel):    
    nom_entreprise:str 
    email:str
    password:str 

class Candidats(BaseModel):
    nom:str
    prenom:str
    email:str
    password:str

class Offres(BaseModel):
       titre:str
       recruteur_id:str
       salaire:str
       description:str
       competences:str
       


class log_recruteur(BaseModel):
      email:str
      password:str


class log_candidat(BaseModel):
        email:str
        password: str

class OByIdR(BaseModel):
      recruteurs_id:str

class OByIdC(BaseModel):
      candidats_id:str

class Arecruteurs(BaseModel):
      forfait:str
      recruteur_id:str


class Acandidats(BaseModel):
      forfait:str
      candidat_id:str

class Chat(BaseModel):
      id:str
      text:str

class Match(BaseModel):
      id:str
      

      
      





