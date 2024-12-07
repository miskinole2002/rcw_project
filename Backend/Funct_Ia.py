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

        template1="""
        Tu es un assistant professionnel en recrutement et développement de carrière.
        En te basant sur les contextes suivants :
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
        je veux que tu inclus obliagtoirement les informations de l'offre d'emploie dans la lettre


        Fournis une réponse détaillée et professionnelle."""

        template12 = """
                Contexte de l'offre d'emploi : {offre_emploi}
                question de l'utilisateur:{question}

                Objectif : Rédiger une lettre de motivation personnalisée basée UNIQUEMENT sur le descriptif du poste

                Instructions de génération :
                1. Analyser en profondeur CHAQUE élément de l'offre d'emploi
                2. Mapper précisément les compétences requises
                3. Créer un narrative convaincant démontrant l'adéquation parfaite

                Structure de la lettre :
                I. Introduction
                - Référence directe au poste : poste
                - Entreprise : entreprise
                - Accroche dynamique basée sur les points clés de l'offre

                II. Premier paragraphe : Compétences techniques
                - Répondre EXACTEMENT aux exigences techniques de l'offre
                - Utiliser le MÊME vocabulaire que le descriptif
                - Exemples : competences_techniques

                III. Deuxième paragraphe : Compétences comportementales
                - Adresser les soft skills recherchées
                - Démontrer l'alignement culturel
                - Exemples : competences_comportementales

                IV. Conclusion
                - Réaffirmer la motivation
                - Démontrer la valeur ajoutée pour l'entreprise
                - Ton : Professionnel et enthousiaste

                Consignes cruciales :
                - AUCUNE information externe n'est utilisée
                - 100% aligné sur l'offre d'emploi
                - Personnalisation maximale
                - Langage précis et dynamique
                - Maximum 500 mots

                Ton : 
                - Professionnel
                - Direct
                - Enthousiaste
                - Aligné sur la culture recherchée
                """
        template= """
À partir de l'offre d'emploi suivante :
{offre_emploi}

Rédige une lettre de motivation professionnelle en suivant ces règles :

1. Personnaliser 100% à partir des informations de l'offre
2. Structure classique : introduction, compétences techniques, compétences comportementales, conclusion
3. Ton professionnel et enthousiaste
4. Mettre en avant l'adéquation entre le profil et le poste
5. Ne pas inventer d'informations non présentes dans l'offre
"""
        prompt=ChatPromptTemplate.from_template(template)


        chain=prompt|model|parser


        embeddings=OpenAIEmbeddings(model="text-embedding-ada-002", api_key=os.getenv("ApiKey"))

        VectorStore_offre= DocArrayInMemorySearch.from_texts(reponse,embedding=embeddings)

        chunks_retriever_offre=VectorStore_offre.as_retriever()

        setup=RunnableParallel(offre_emploi=chunks_retriever_offre ,question=RunnablePassthrough())

        chain=setup|prompt|model|parser
        question=" redige moi une lettre de motivation professionelle en fonction des informations de l'offre"
        x=chain.invoke(question)
        return(x)


