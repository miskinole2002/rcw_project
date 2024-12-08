
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import *
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader
from dotenv import load_dotenv
import os

load_dotenv()

def chat(path,response,question):
        model=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.0,api_key=os.getenv("ApiKey"))

        parser=StrOutputParser()
        chain=model|parser
     
        
        

        template1="""
        Tu es un assistant de recrutement expert. 
        En te basant sur les contextes suivants :
        - CV : {cv}
        - Offre d'emploi : {offre_emploi}
        

        Réponds à la question : {question}

        Fournis une réponse détaillée et professionnelle."""

        template0= """
        Tu es Audrey 3.0, assistant professionnel en recrutement et développement de carrière.

        Éléments d'entrée :
        - Offre d'emploi : {offre_emploi}
        - CV du candidat : {cv}
        - Question de l'utilisateur : {question}

        Missions principales :
        1. Répondre à la question spécifique de l'utilisateur
        2. Générer une lettre de motivation personnalisée
        3. Analyser et conseiller sur le CV du candidat en fonction de {offre_emploi}
        4. Évaluer l'adéquation entre le profil et l'offre d'emploi

        Étapes de traitement :

        I. Réponse à la question de l'utilisateur
        - Traitement direct de la demande
        - Réponse précise et contextualisée
        - Si la question ne peut être traitée, proposer des alternatives

        II. Analyse du CV
        - Points forts à mettre en valeur
        - Points à améliorer
        - Suggestions de renforcement du profil

        III. Analyse de l'offre d'emploi
        - Compétences clés requises
        - Mots-clés importants
        - Attentes spécifiques du recruteur

        IV. Génération de la lettre de motivation
        Structure :
        - Introduction percutante
        - Mise en valeur des compétences
        - Adéquation profil-poste
        - Conclusion motivante

        V. Conseils personnalisés
        - Recommandations pour optimiser le CV
        - Stratégies pour se démarquer
        - Préparation à l'entretien
        
        Format de sortie :
        1. Réponse à la question
        2. Conseils CV a la demande de l'utilisateur
        3. Analyse de l'offre d'emploie que tu as en contexte  si l'utilisateur te le demande 
        4. Lettre de motivation si l'utilisateur la  demande, redige la  avec tous ses informations inclus son nom etc.. si non n'en parle pas 
        5. Recommandations personnalisées

        Ton : Professionnel, bienveillant et encourageant

        """

        template= """
CONTEXTE OBLIGATOIRE :
1. CV du candidat ({cv})
   - Extraire exhaustivement :
     * Compétences techniques
     * Expériences professionnelles
     * Formations
     * Certifications
     * Réalisations significatives

2. Offre d'emploi ({offre_emploi})
   - Identification précise :
     * Intitulé du poste
     * Missions principales
     * Compétences techniques requises
     * Compétences comportementales
     * Prérequis et profil recherché

3. Question de l'utilisateur ({question})
   - Analyse du besoin spécifique
   - Intention de la demande
   - Contexte de la requête

MÉCANISME DE TRAITEMENT :
- Mapping compétences à 100%
- Scoring de correspondance
- Identification des écarts et opportunités
- Réponse ultraPersonnalisée

RÈGLES DE GÉNÉRATION :
- 90% des informations proviennent du contexte
- Zéro invention
- Langage précis et professionnel
- Justification systématique

ALGORITHME DE RÉPONSE :
- Correspondance > 80% : Valorisation
- Correspondance < 80% : Recommandations de développement
- Traçabilité des éléments de réponse

TON :
- Expert
- Bienveillant
- Constructif
- Orienté solution
"""
        prompt=ChatPromptTemplate.from_template(template)


        chain=prompt|model|parser

        #cv 
        path_cv=rf"{path}"
        loader_cv=Docx2txtLoader(path_cv)
        text_cv=loader_cv.load()
        text_split_cv=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
        doc_cv=text_split_cv.split_documents(text_cv)
        #offre
        text_split_offre=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
        doc_offre=text_split_offre.split_text(response)

        embeddings=OpenAIEmbeddings(model="text-embedding-ada-002", api_key=os.getenv("ApiKey"))

        VectorStore_cv= DocArrayInMemorySearch.from_documents(doc_cv,embedding=embeddings)
        VectorStore_offre= DocArrayInMemorySearch.from_texts(doc_offre,embedding=embeddings)

        chunks_retriever_cv=VectorStore_cv.as_retriever()
        chunks_retriever_offre=VectorStore_offre.as_retriever()
        print(VectorStore_offre) 
        setup=RunnableParallel(cv=chunks_retriever_cv, offre_emploi=chunks_retriever_offre ,question=RunnablePassthrough())

        chain=setup|prompt|model|parser
        x=chain.invoke(question)
        return x


