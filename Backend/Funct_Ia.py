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

def lettre_motivation():
        model=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.0,api_key=os.getenv("ApiKey"))

        parser=StrOutputParser()
        chain=model|parser

        template="""
        Tu es un assistant professionnel en recrutement et développement de carrière.
        En te basant sur les contextes suivants :
        - CV : {cv}
        - Offre d'emploi : {offre_emploi}
        -redige une lettre de motivation 
        -question de l'utilisateur:{question}


        IV. Génération de la lettre de motivation
        Structure :
        - avec pour entete les informations personnelle de l'utilisateur si disponble
        - information de l'utilisateur si disponible
        - Introduction percutante
        - Mise en valeur des compétences
        - Adéquation profil-poste
        - Conclusion motivante

        -Ton : Professionnel, bienveillant et encourageant



        Fournis une réponse détaillée et professionnelle."""


        prompt=ChatPromptTemplate.from_template(template)


        chain=prompt|model|parser

        #cv
        path_cv=r"Backend\Cvs\cv_train.docx"
        loader_cv=Docx2txtLoader(path_cv)
        text_cv=loader_cv.load()
        text_split_cv=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
        doc_cv=text_split_cv.split_documents(text_cv)

        #offre
        path_offre=r"Backend\Cvs\offre_train.docx"
        loader_offre=Docx2txtLoader(path_offre)
        text_offre=loader_offre.load()
        text_split_offre=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
        doc_offre=text_split_offre.split_documents(text_offre)


        embeddings=OpenAIEmbeddings(model="text-embedding-ada-002", api_key=os.getenv("ApiKey"))

        VectorStore_cv= DocArrayInMemorySearch.from_documents(doc_cv,embedding=embeddings)
        VectorStore_offre= DocArrayInMemorySearch.from_documents(doc_offre,embedding=embeddings)

        chunks_retriever_cv=VectorStore_cv.as_retriever()
        chunks_retriever_offre=VectorStore_offre.as_retriever()

        setup=RunnableParallel(cv=chunks_retriever_cv,offre_emploi=chunks_retriever_offre ,question=RunnablePassthrough())

        chain=setup|prompt|model|parser
        question=" redige moi une lettre de motivation professionelle"
        x=chain.invoke(question)
        return(x)


x=lettre_motivation()
print(x)