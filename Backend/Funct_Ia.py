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

def lettre_motivation(reponse):
        model=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.0,api_key=os.getenv("ApiKey"))

        parser=StrOutputParser()
        chain=model|parser

        
        template= """
        À partir de l'offre d'emploi suivante :
        {offre_emploi}

        Rédige une lettre de motivation professionnelle en suivant ces règles :

        1. Personnaliser 100% à partir des informations de l'offre
        2. Structure classique : introduction, compétences techniques, compétences comportementales, conclusion
        3. Ton professionnel et enthousiaste
        4. Ne pas inventer d'informations non présentes dans l'offre
        """ 
        prompt=ChatPromptTemplate.from_template(template)


        chain=prompt|model|parser


        text_split_offre=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
        doc_offre=text_split_offre.split_text(reponse)

        embeddings=OpenAIEmbeddings(model="text-embedding-ada-002", api_key=os.getenv("ApiKey"))

        VectorStore_offre= DocArrayInMemorySearch.from_texts(doc_offre,embedding=embeddings)

        chunks_retriever_offre=VectorStore_offre.as_retriever()

        setup=RunnableParallel(offre_emploi=chunks_retriever_offre ,question=RunnablePassthrough())

        chain=setup|prompt|model|parser
        question="resume moi l'offre d'emploie"
        x=chain.invoke(question)
        print(x)
        return(x)


# fonction du chatbot

def chat(path,response,question):
        model=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.0,api_key=os.getenv("ApiKey"))

        parser=StrOutputParser()
        chain=model|parser

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


