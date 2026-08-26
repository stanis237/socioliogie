"""
Service d'intégration avec l'API Google Gemini
Permet la génération réelle de cours et de réponses de tutorat interactives.
"""
import os
import json
import random
from django.conf import settings

# Charger les variables d'environnement au cas où
from dotenv import load_dotenv
load_dotenv()

# Tenter d'importer la bibliothèque google-generativeai
try:
    import google.generativeai as genai
    HAS_GEMINI_SDK = True
except ImportError:
    HAS_GEMINI_SDK = False

class GeminiService:
    """Service d'accès à l'API Google Gemini avec repli local intelligent"""
    
    @staticmethod
    def get_api_key():
        """Récupère la clé API Gemini depuis les configurations de Django ou l'environnement"""
        return getattr(settings, 'GEMINI_API_KEY', None) or os.environ.get('GEMINI_API_KEY')

    @staticmethod
    def is_configured():
        """Vérifie si l'API Gemini est disponible et configurée"""
        return HAS_GEMINI_SDK and bool(GeminiService.get_api_key())

    @staticmethod
    def generate_course_data(topic, difficulty, subject):
        """
        Génère les données structurées d'un cours en utilisant l'IA Gemini.
        Retourne un dictionnaire contenant le titre, la description, les vidéos, le quiz et les exercices.
        """
        difficulty_labels = {'beginner': 'Débutant', 'intermediate': 'Intermédiaire', 'advanced': 'Avancé'}
        diff_label = difficulty_labels.get(difficulty, 'Intermédiaire')
        
        prompt = f"""
        Tu es un professeur expert dans la matière suivante : {subject}.
        Génère un cours d'apprentissage complet sur le sujet : "{topic if topic else 'Introduction générale'}".
        Niveau de difficulté : {diff_label}.
        La langue du cours doit être impérativement le Français.
        
        Génère un objet JSON valide correspondant EXACTEMENT au schéma suivant, sans texte d'introduction ni de conclusion :
        {{
            "title": "Titre accrocheur du cours",
            "description": "Description détaillée et captivante expliquant les objectifs du cours, son importance et les concepts clés.",
            "videos": [
                {{"title": "Titre du chapitre vidéo 1", "duration": "Durée au format MM:SS (ex: 12:30)"}},
                {{"title": "Titre du chapitre vidéo 2", "duration": "Durée au format MM:SS (ex: 15:45)"}},
                {{"title": "Titre du chapitre vidéo 3", "duration": "Durée au format MM:SS (ex: 10:20)"}}
            ],
            "quizzes": [
                {{
                    "question": "Question de compréhension 1 ?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct": 0
                }},
                {{
                    "question": "Question de compréhension 2 ?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct": 1
                }}
            ],
            "exercises": [
                {{
                    "title": "Titre de l'exercice 1",
                    "content": "Consignes détaillées de l'exercice pratique (ex: dissertation, étude de cas).",
                    "difficulty": "easy"
                }},
                {{
                    "title": "Titre de l'exercice 2",
                    "content": "Consignes de l'exercice de niveau supérieur.",
                    "difficulty": "medium"
                }}
            ]
        }}
        """
        
        if GeminiService.is_configured():
            try:
                genai.configure(api_key=GeminiService.get_api_key())
                model = genai.GenerativeModel(
                    'gemini-1.5-flash',
                    generation_config={"response_mime_type": "application/json"}
                )
                response = model.generate_content(prompt)
                data = json.loads(response.text)
                return data
            except Exception as e:
                print(f"Erreur Gemini API: {str(e)}. Utilisation du fallback.")
        
        # Fallback si l'IA n'est pas configurée ou en cas d'erreur
        return GeminiService._generate_fallback_course_data(topic, difficulty, subject)

    @staticmethod
    def get_tutor_response(user, question):
        """
        Génère une réponse interactive de tutorat académique en sociologie ou autre matière
        """
        user_level = user.profile.get_level_display()
        is_premium = user.profile.is_premium
        
        prompt = f"""
        Tu es "Prophète", un tuteur intelligent expert de la plateforme d'apprentissage en ligne.
        L'apprenant s'appelle {user.username}. Son niveau de profil est : {user_level}.
        Son statut d'abonnement est : {"Premium (Accès illimité)" if is_premium else "Gratuit (Accès limité)"}.
        
        Réponds à sa question ci-dessous de manière pédagogique, structurée, et universitaire en français. 
        Utilise des citations célèbres d'auteurs (comme Karl Marx, Émile Durkheim, Max Weber en sociologie) pour illustrer.
        Mets en valeur la réponse avec du markdown propre (titres, listes à puces, texte en gras).
        
        Question de l'apprenant : "{question}"
        """
        
        if GeminiService.is_configured():
            try:
                genai.configure(api_key=GeminiService.get_api_key())
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Erreur Gemini API pour le tuteur : {str(e)}.")
                
        return GeminiService._generate_fallback_tutor_response(user, question)

    @staticmethod
    def _generate_fallback_course_data(topic, difficulty, subject):
        """Génère des données de cours simulées mais riches pour le fallback"""
        # Choix des titres basés sur le sujet et le topic
        title = topic if topic else f"Introduction avancée à la discipline ({subject})"
        
        description = (
            f"Ce cours complet traite en profondeur le sujet '{title}'. "
            f"Conçu spécifiquement pour le niveau {difficulty}, il permet de structurer les connaissances "
            f"fondamentales, d'analyser les dynamiques sociales et conceptuelles et d'aborder des études de cas concrètes. "
            f"À travers une série de chapitres vidéos et d'exercices d'application, vous maîtriserez les clés d'analyse "
            f"et les théories incontournables."
        )
        
        videos = [
            {"title": f"1. Les origines et fondements de : {title}", "duration": "14:20"},
            {"title": f"2. Analyse théorique et méthodologies clés", "duration": "18:15"},
            {"title": f"3. Perspectives critiques et applications modernes", "duration": "12:45"},
        ]
        
        quizzes = [
            {
                "question": f"Quel est le postulat principal concernant : {title} ?",
                "options": [
                    "Il s'agit d'une construction dynamique et historique",
                    "C'est un fait biologique immuable",
                    "C'est un concept purement abstrait sans application",
                    "Les avis sont unanimes et ne nécessitent aucune recherche"
                ],
                "correct": 0
            },
            {
                "question": f"Quelle méthodologie est la plus recommandée pour analyser ce sujet ?",
                "options": [
                    "Ignorer les statistiques descriptives",
                    "L'approche mixte conjuguant qualitatif et quantitatif",
                    "Se limiter uniquement à l'introspection",
                    "Le recours exclusif à des sources non vérifiées"
                ],
                "correct": 1
            },
            {
                "question": "Qui est considéré comme un pionnier sur ces questions ?",
                "options": [
                    "Un auteur fictif",
                    "Les grands classiques de la pensée critique",
                    "Aucun chercheur ne s'est intéressé à cela",
                    "La réponse reste inconnue"
                ],
                "correct": 1
            }
        ]
        
        exercises = [
            {
                "title": f"Étude de cas pratique : {title}",
                "content": "Rédigez une note de synthèse de 2 pages analysant un fait d'actualité sous l'angle des concepts étudiés dans ce cours. Identifiez les acteurs principaux et les dynamiques de pouvoir sous-jacentes.",
                "difficulty": "medium"
            },
            {
                "title": "Analyse critique comparative",
                "content": "Confrontez deux approches théoriques opposées concernant ce sujet. Dressez un tableau comparatif mettant en valeur leurs points de convergence et de divergence.",
                "difficulty": "hard"
            }
        ]
        
        return {
            "title": title,
            "description": description,
            "videos": videos,
            "quizzes": quizzes,
            "exercises": exercises
        }

    @staticmethod
    def _generate_fallback_tutor_response(user, question):
        """Génère une réponse de tutorat très qualitative et universitaire pour le fallback"""
        question_lower = question.lower()
        
        # Réponse personnalisée si on détecte des mots-clés de sociologie
        if "durkheim" in question_lower or "suicide" in question_lower:
            concept = "Émile Durkheim"
            quote = '"Le suicide varie en raison inverse du degré d\'intégration des groupes sociaux dont fait partie l\'individu."'
            body = """
            Émile Durkheim est le père fondateur de la sociologie quantitative française. Dans son ouvrage emblématique *Le Suicide* (1897), il démontre que ce geste, apparemment intime, est en réalité déterminé par des forces sociales.
            
            Durkheim identifie 4 grands types de suicides basés sur deux axes : l'**intégration** et la **régulation** :
            1. **Suicide égoïste** : Défaut d'intégration (l'individu se sent isolé).
            2. **Suicide altruiste** : Excès d'intégration (l'individu se sacrifie pour le groupe, ex: kamikaze).
            3. **Suicide anomique** : Défaut de régulation (les règles sociales se brouillent lors de crises économiques ou de changements brutaux).
            4. **Suicide fataliste** : Excès de régulation (les règles sont trop oppressantes, ex: esclavage).
            """
        elif "marx" in question_lower or "classe" in question_lower or "capital" in question_lower:
            concept = "Karl Marx"
            quote = '"L\'histoire de toute société jusqu\'à nos jours n\'a été que l\'histoire de luttes de classes."'
            body = """
            Karl Marx analyse la société sous le prisme du **matérialisme historique**. Pour lui, l'infrastructure économique (les moyens de production) détermine la superstructure politique et idéologique.
            
            Les concepts fondamentaux à retenir :
            - **La Bourgeoisie vs le Prolétariat** : La classe qui possède les moyens de production face à celle qui ne possède que sa force de travail.
            - **La Plus-value** : La valeur supplémentaire créée par le travailleur mais accaparée par le capitaliste, source de l'exploitation.
            - **La Conscience de classe** : Le passage de la *classe en soi* (partager des conditions de vie similaires) à la *classe pour soi* (s'organiser politiquement pour défendre ses intérêts).
            """
        elif "weber" in question_lower or "éthique" in question_lower or "bureaucratie" in question_lower:
            concept = "Max Weber"
            quote = '"L\'idéal-type est un tableau de pensée, il n\'est pas la réalité historique."'
            body = """
            Max Weber est le pionnier de la **sociologie compréhensive**. Contrairement à Durkheim qui étudie les "faits sociaux comme des choses", Weber s'intéresse au sens que les individus donnent à leurs actions (l'action sociale).
            
            Ses apports majeurs :
            - **La rationalisation du monde** (ou "désenchantement du monde") : le passage d'explications magiques ou religieuses à des choix basés sur l'efficacité et la rationalité instrumentale.
            - **L'éthique protestante et l'esprit du capitalisme** : Weber montre comment l'ascétisme calviniste a involontairement favorisé l'accumulation capitaliste en faisant du succès professionnel un signe d'élection divine.
            - **La domination** : Weber distingue trois formes de légitimité du pouvoir : *traditionnelle*, *charismatique* et *rationnelle-légale* (la bureaucratie moderne).
            """
        else:
            concept = "Introduction à la Sociologie"
            quote = '"La sociologie est la science qui se propose de comprendre par interprétation l\'activité sociale."'
            body = f"""
            Merci pour votre question intéressante : *"{question}"*.
            
            La sociologie consiste à dénaturaliser le monde social, c'est-à-dire à dépasser le sens commun (les idées reçues) pour analyser comment les structures sociales modèlent nos comportements individuels.
            
            Pour approfondir votre réflexion, je vous conseille de vous appuyer sur la distinction classique entre :
            1. **La socialisation primaire** : acquise durant l'enfance via la famille et l'école.
            2. **La socialisation secondaire** : qui se poursuit tout au long de la vie (milieu professionnel, couple, médias).
            
            N'hésitez pas à reformuler votre question avec des concepts précis (comme l'habitus de Pierre Bourdieu ou l'interactionnisme d'Erving Goffman) pour que nous puissions analyser cela ensemble !
            """
            
        response_text = f"""### Réponse de Tuteur Prophète 🎓

Bonjour **{user.username}**, en tant que tuteur en sociologie, je suis ravi de t'accompagner.

> **Citation de référence ({concept}) :**
> {quote}

{body}

---
*Astuce Premium : Tu as un accès complet à mes analyses. Continue à poser des questions pour accumuler des points et passer au niveau supérieur !*
"""
        return response_text
