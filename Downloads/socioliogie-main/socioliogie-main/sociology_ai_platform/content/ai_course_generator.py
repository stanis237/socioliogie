"""
Service d'IA pour générer automatiquement des cours dans toutes les matières
Utilise YouTube pour les vidéos, Google pour la documentation, et ChatGPT pour les quiz/exercices
"""
import random
import json
import os
from django.conf import settings
from .models import Course, Video, Quiz, Exercise, Document
# Imports pour les services externes
try:
    from youtubesearchpython import VideosSearch
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

try:
    from serpapi import GoogleSearch
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

import requests


class AICourseGenerator:
    """Générateur de cours basé sur l'IA pour toutes les matières"""
    
    # Mapping émotion -> matières recommandées
    EMOTION_TO_SUBJECTS = {
        'happy': ['sociology', 'literature', 'arts', 'history', 'philosophy'],
        'excited': ['mathematics', 'science', 'computer_science', 'psychology'],
        'focused': ['mathematics', 'science', 'philosophy', 'economics', 'computer_science'],
        'neutral': ['sociology', 'history', 'geography', 'languages', 'literature'],
        'confused': ['sociology', 'history', 'languages', 'arts'],
        'sad': ['literature', 'arts', 'philosophy', 'psychology', 'history']
    }
    
    # Templates de cours par matière
    COURSE_TEMPLATES = {
        'sociology': {
            'beginner': [
                {'topics': ['Introduction à la sociologie', 'Les fondements de la société', 'Les concepts de base'], 
                 'descriptions': ['Un cours d\'introduction complet pour comprendre les bases de la sociologie moderne.']},
            ],
            'intermediate': [
                {'topics': ['Théories sociologiques contemporaines', 'Stratification sociale', 'Sociologie des organisations'], 
                 'descriptions': ['Approfondissez votre compréhension des théories sociologiques modernes.']},
            ],
            'advanced': [
                {'topics': ['Théories critiques en sociologie', 'Sociologie postmoderne', 'Méthodologies avancées'], 
                 'descriptions': ['Plongez dans les théories critiques et leurs applications contemporaines.']},
            ]
        },
        'mathematics': {
            'beginner': [
                {'topics': ['Algèbre de base', 'Géométrie élémentaire', 'Arithmétique'], 
                 'descriptions': ['Maîtrisez les fondamentaux des mathématiques.']},
            ],
            'intermediate': [
                {'topics': ['Calcul différentiel', 'Statistiques', 'Probabilités'], 
                 'descriptions': ['Approfondissez vos connaissances mathématiques.']},
            ],
            'advanced': [
                {'topics': ['Analyse avancée', 'Algèbre linéaire', 'Topologie'], 
                 'descriptions': ['Explorez les concepts mathématiques avancés.']},
            ]
        },
        'science': {
            'beginner': [
                {'topics': ['Introduction à la physique', 'Chimie de base', 'Biologie cellulaire'], 
                 'descriptions': ['Découvrez les principes fondamentaux des sciences.']},
            ],
            'intermediate': [
                {'topics': ['Mécanique quantique', 'Chimie organique', 'Génétique'], 
                 'descriptions': ['Approfondissez votre compréhension des sciences.']},
            ],
            'advanced': [
                {'topics': ['Physique théorique', 'Biochimie avancée', 'Évolution'], 
                 'descriptions': ['Explorez les frontières de la science moderne.']},
            ]
        },
        'history': {
            'beginner': [
                {'topics': ['Histoire ancienne', 'Histoire médiévale', 'Histoire moderne'], 
                 'descriptions': ['Découvrez les grandes périodes de l\'histoire.']},
            ],
            'intermediate': [
                {'topics': ['Histoire contemporaine', 'Histoire des civilisations', 'Histoire économique'], 
                 'descriptions': ['Analysez les événements historiques majeurs.']},
            ],
            'advanced': [
                {'topics': ['Historiographie', 'Histoire comparée', 'Méthodologie historique'], 
                 'descriptions': ['Maîtrisez les méthodes de recherche historique.']},
            ]
        },
        'literature': {
            'beginner': [
                {'topics': ['Introduction à la littérature', 'Genres littéraires', 'Analyse de texte'], 
                 'descriptions': ['Découvrez les bases de l\'analyse littéraire.']},
            ],
            'intermediate': [
                {'topics': ['Littérature classique', 'Mouvements littéraires', 'Critique littéraire'], 
                 'descriptions': ['Explorez les grands courants littéraires.']},
            ],
            'advanced': [
                {'topics': ['Théorie littéraire', 'Littérature comparée', 'Écriture créative'], 
                 'descriptions': ['Approfondissez votre compréhension de la littérature.']},
            ]
        },
        'philosophy': {
            'beginner': [
                {'topics': ['Introduction à la philosophie', 'Logique de base', 'Éthique fondamentale'], 
                 'descriptions': ['Découvrez les concepts fondamentaux de la philosophie.']},
            ],
            'intermediate': [
                {'topics': ['Philosophie antique', 'Philosophie moderne', 'Épistémologie'], 
                 'descriptions': ['Explorez les grandes traditions philosophiques.']},
            ],
            'advanced': [
                {'topics': ['Philosophie contemporaine', 'Métaphysique', 'Philosophie du langage'], 
                 'descriptions': ['Plongez dans les débats philosophiques contemporains.']},
            ]
        },
        'psychology': {
            'beginner': [
                {'topics': ['Introduction à la psychologie', 'Psychologie cognitive', 'Développement humain'], 
                 'descriptions': ['Découvrez les bases de la psychologie.']},
            ],
            'intermediate': [
                {'topics': ['Psychologie sociale', 'Psychologie clinique', 'Neurosciences'], 
                 'descriptions': ['Approfondissez votre compréhension de l\'esprit humain.']},
            ],
            'advanced': [
                {'topics': ['Psychologie expérimentale', 'Thérapies avancées', 'Neuropsychologie'], 
                 'descriptions': ['Explorez les recherches avancées en psychologie.']},
            ]
        },
        'economics': {
            'beginner': [
                {'topics': ['Économie de base', 'Microéconomie', 'Macroéconomie'], 
                 'descriptions': ['Comprenez les principes fondamentaux de l\'économie.']},
            ],
            'intermediate': [
                {'topics': ['Économie internationale', 'Économie du développement', 'Finance'], 
                 'descriptions': ['Analysez les mécanismes économiques complexes.']},
            ],
            'advanced': [
                {'topics': ['Économétrie', 'Théorie économique avancée', 'Politique économique'], 
                 'descriptions': ['Maîtrisez les modèles économiques avancés.']},
            ]
        },
        'languages': {
            'beginner': [
                {'topics': ['Grammaire de base', 'Vocabulaire essentiel', 'Communication orale'], 
                 'descriptions': ['Apprenez les bases d\'une nouvelle langue.']},
            ],
            'intermediate': [
                {'topics': ['Grammaire avancée', 'Expression écrite', 'Compréhension orale'], 
                 'descriptions': ['Améliorez votre maîtrise de la langue.']},
            ],
            'advanced': [
                {'topics': ['Littérature en langue étrangère', 'Traduction', 'Linguistique'], 
                 'descriptions': ['Maîtrisez la langue à un niveau avancé.']},
            ]
        },
        'arts': {
            'beginner': [
                {'topics': ['Histoire de l\'art', 'Techniques de base', 'Analyse d\'œuvres'], 
                 'descriptions': ['Découvrez les fondamentaux de l\'art.']},
            ],
            'intermediate': [
                {'topics': ['Mouvements artistiques', 'Création artistique', 'Critique d\'art'], 
                 'descriptions': ['Explorez les différents courants artistiques.']},
            ],
            'advanced': [
                {'topics': ['Théorie de l\'art', 'Art contemporain', 'Conservation et restauration'], 
                 'descriptions': ['Approfondissez votre compréhension de l\'art.']},
            ]
        },
        'geography': {
            'beginner': [
                {'topics': ['Géographie physique', 'Géographie humaine', 'Cartographie'], 
                 'descriptions': ['Découvrez les bases de la géographie.']},
            ],
            'intermediate': [
                {'topics': ['Géographie régionale', 'Géopolitique', 'Environnement'], 
                 'descriptions': ['Analysez les enjeux géographiques contemporains.']},
            ],
            'advanced': [
                {'topics': ['Géographie économique', 'Aménagement du territoire', 'Géographie urbaine'], 
                 'descriptions': ['Maîtrisez les concepts géographiques avancés.']},
            ]
        },
        'computer_science': {
            'beginner': [
                {'topics': ['Programmation de base', 'Algorithmes simples', 'Structures de données'], 
                 'descriptions': ['Apprenez les bases de la programmation.']},
            ],
            'intermediate': [
                {'topics': ['Programmation orientée objet', 'Bases de données', 'Réseaux'], 
                 'descriptions': ['Développez vos compétences en programmation.']},
            ],
            'advanced': [
                {'topics': ['Intelligence artificielle', 'Architecture logicielle', 'Sécurité informatique'], 
                 'descriptions': ['Maîtrisez les technologies avancées.']},
            ]
        }
    }
    
    @staticmethod
    def _search_youtube_videos(query, max_results=5):
        """
        Recherche des vidéos YouTube pertinentes
        """
        if not YOUTUBE_AVAILABLE:
            return []
        
        try:
            videos_search = VideosSearch(query, limit=max_results)
            results = videos_search.result()
            
            videos = []
            for item in results.get('result', [])[:max_results]:
                video_id = item.get('id', '')
                title = item.get('title', '')
                duration = item.get('duration', '')
                url = f"https://www.youtube.com/watch?v={video_id}"
                
                videos.append({
                    'title': title,
                    'url': url,
                    'duration': duration,
                    'video_id': video_id
                })
            
            return videos
        except Exception as e:
            print(f"Erreur lors de la recherche YouTube: {e}")
            return []
    
    @staticmethod
    def _search_google_docs(query, max_results=3):
        """
        Recherche de documentation via Google Search
        """
        if not GOOGLE_AVAILABLE:
            return []
        
        try:
            api_key = getattr(settings, 'GOOGLE_SEARCH_API_KEY', '')
            engine_id = getattr(settings, 'GOOGLE_SEARCH_ENGINE_ID', '')
            
            if not api_key or not engine_id:
                return []
            
            params = {
                "q": query,
                "api_key": api_key,
                "engine": "google",
                "num": max_results
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            docs = []
            for item in results.get('organic_results', [])[:max_results]:
                docs.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                })
            
            return docs
        except Exception as e:
            print(f"Erreur lors de la recherche Google: {e}")
            return []
    
    @staticmethod
    def _generate_with_chatgpt(prompt, max_tokens=500):
        """
        Génère du contenu avec ChatGPT
        """
        if not OPENAI_AVAILABLE:
            return None
        
        try:
            api_key = getattr(settings, 'OPENAI_API_KEY', '')
            if not api_key:
                return None
            
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un assistant pédagogique expert qui crée du contenu éducatif adapté aux étudiants."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erreur lors de la génération ChatGPT: {e}")
            return None
    
    @staticmethod
    def _generate_quiz_with_chatgpt(course_title, subject, difficulty, user_level=None):
        """
        Génère un quiz adapté avec ChatGPT
        """
        difficulty_label = AICourseGenerator._get_difficulty_label(difficulty)
        subject_label = AICourseGenerator._get_subject_label(subject)
        
        prompt = f"""Crée un quiz de {difficulty_label} en {subject_label} sur le sujet "{course_title}".

Le quiz doit contenir 5 questions à choix multiples avec 4 options chacune.
Format JSON requis:
{{
    "questions": [
        {{
            "question": "Question ici",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0
        }}
    ]
}}

Le niveau de difficulté est {difficulty_label}. Les questions doivent être adaptées à ce niveau.
Réponds UNIQUEMENT avec le JSON, sans texte supplémentaire."""

        response = AICourseGenerator._generate_with_chatgpt(prompt, max_tokens=1000)
        
        if response:
            try:
                # Nettoyer la réponse pour extraire le JSON
                response = response.strip()
                if response.startswith('```json'):
                    response = response[7:]
                if response.startswith('```'):
                    response = response[3:]
                if response.endswith('```'):
                    response = response[:-3]
                response = response.strip()
                
                quiz_data = json.loads(response)
                return quiz_data.get('questions', [])
            except json.JSONDecodeError:
                print("Erreur de parsing JSON du quiz")
        
        # Fallback vers un quiz basique
        return [{
            'question': f'Quel est le concept fondamental de {course_title}?',
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct': 0
        }]
    
    @staticmethod
    def _generate_exercise_with_chatgpt(course_title, subject, difficulty, exercise_type='practice'):
        """
        Génère un exercice adapté avec ChatGPT
        """
        difficulty_label = AICourseGenerator._get_difficulty_label(difficulty)
        subject_label = AICourseGenerator._get_subject_label(subject)
        
        difficulty_map = {'beginner': 'facile', 'intermediate': 'moyen', 'advanced': 'difficile'}
        difficulty_fr = difficulty_map.get(difficulty, 'moyen')
        
        prompt = f"""Crée un exercice {difficulty_fr} en {subject_label} sur le sujet "{course_title}".

L'exercice doit être adapté au niveau {difficulty_label} et permettre à l'étudiant de pratiquer les concepts appris.
Format JSON requis:
{{
    "title": "Titre de l'exercice",
    "content": "Description détaillée de l'exercice avec instructions claires",
    "difficulty": "{difficulty}"
}}

Réponds UNIQUEMENT avec le JSON, sans texte supplémentaire."""

        response = AICourseGenerator._generate_with_chatgpt(prompt, max_tokens=500)
        
        if response:
            try:
                # Nettoyer la réponse pour extraire le JSON
                response = response.strip()
                if response.startswith('```json'):
                    response = response[7:]
                if response.startswith('```'):
                    response = response[3:]
                if response.endswith('```'):
                    response = response[:-3]
                response = response.strip()
                
                exercise_data = json.loads(response)
                return exercise_data
            except json.JSONDecodeError:
                print("Erreur de parsing JSON de l'exercice")
        
        # Fallback vers un exercice basique
        return {
            'title': f'Exercice pratique - {course_title}',
            'content': f'Appliquez les concepts de {course_title} à un cas concret.',
            'difficulty': difficulty
        }
    
    @staticmethod
    def get_subjects_by_emotion(emotion_type):
        """Retourne les matières recommandées selon l'émotion"""
        return AICourseGenerator.EMOTION_TO_SUBJECTS.get(emotion_type, ['sociology', 'history', 'literature'])
    
    @staticmethod
    def generate_course(topic=None, difficulty='intermediate', subject='sociology', user=None, user_preferences=None, custom_youtube_url=None):
        """
        Génère un cours complet avec son contenu adapté à l'étudiant

        Args:
            topic: Sujet du cours (optionnel)
            difficulty: Niveau de difficulté (beginner, intermediate, advanced)
            subject: Matière du cours
            user: Utilisateur pour adapter le contenu (optionnel)
            user_preferences: Préférences de l'utilisateur (optionnel)
            custom_youtube_url: URL YouTube personnalisée pour le cours (optionnel)
        """
        # Adapter la difficulté selon le profil utilisateur si disponible
        if user and hasattr(user, 'profile'):
            user_level = user.profile.level
            # Ajuster la difficulté si nécessaire
            if user_level == 'beginner' and difficulty == 'advanced':
                difficulty = 'intermediate'
            elif user_level == 'advanced' and difficulty == 'beginner':
                difficulty = 'intermediate'
        
        # Obtenir les templates pour la matière
        subject_templates = AICourseGenerator.COURSE_TEMPLATES.get(
            subject, 
            AICourseGenerator.COURSE_TEMPLATES['sociology']
        )
        
        difficulty_templates = subject_templates.get(
            difficulty,
            subject_templates.get('intermediate', subject_templates.get('beginner', [{}]))
        )
        
        if not difficulty_templates:
            difficulty_templates = [{'topics': [f'Cours de {subject}'], 'descriptions': ['Cours généré automatiquement.']}]
        
        template = random.choice(difficulty_templates) if difficulty_templates else {}
        
        # Générer le titre
        if topic:
            title = topic
        else:
            topics = template.get('topics', [f'Cours de {subject}'])
            title = random.choice(topics) if topics else f'Cours de {subject}'
        
        # Générer la description
        descriptions = template.get('descriptions', ['Cours généré automatiquement.'])
        description = random.choice(descriptions) if descriptions else 'Cours généré automatiquement.'
        description += f" Ce cours de niveau {AICourseGenerator._get_difficulty_label(difficulty)} vous permettra d'approfondir vos connaissances en {AICourseGenerator._get_subject_label(subject)}."
        
        # Créer le cours
        course = Course.objects.create(
            title=title,
            description=description,
            difficulty=difficulty,
            subject=subject,
            custom_youtube_url=custom_youtube_url
        )
        
        # Générer des vidéos YouTube
        AICourseGenerator._generate_videos(course, difficulty, subject, title)
        
        # Générer de la documentation Google
        AICourseGenerator._generate_documents(course, subject, title)
        
        # Générer un quiz avec ChatGPT
        AICourseGenerator._generate_quiz(course, difficulty, subject, title, user)
        
        # Générer des exercices avec ChatGPT
        AICourseGenerator._generate_exercises(course, difficulty, subject, title)
        
        return course
    
    @staticmethod
    def _generate_videos(course, difficulty, subject, course_title):
        """Génère des vidéos YouTube pour le cours"""
        video_count = {'beginner': 3, 'intermediate': 4, 'advanced': 5}.get(difficulty, 4)

        # Si une URL YouTube personnalisée est fournie, l'utiliser comme première vidéo
        if course.custom_youtube_url:
            Video.objects.create(
                course=course,
                title=f"{course_title} - Vidéo personnalisée",
                url=course.custom_youtube_url,
                duration='10:00'  # Durée par défaut
            )
            video_count -= 1  # Réduire le nombre de vidéos à générer

        subject_label = AICourseGenerator._get_subject_label(subject)
        difficulty_label = AICourseGenerator._get_difficulty_label(difficulty)

        # Rechercher des vidéos pertinentes
        search_query = f"{course_title} {subject_label} cours {difficulty_label}"
        youtube_videos = AICourseGenerator._search_youtube_videos(search_query, max_results=video_count)

        if youtube_videos and YOUTUBE_AVAILABLE:
            # Utiliser les vidéos trouvées
            for video in youtube_videos[:video_count]:
                Video.objects.create(
                    course=course,
                    title=video['title'],
                    url=video['url'],
                    duration=video.get('duration', '10:00')
                )
    
    @staticmethod
    def _generate_documents(course, subject, course_title):
        """Génère des liens de documentation via Google Search"""
        subject_label = AICourseGenerator._get_subject_label(subject)
        search_query = f"{course_title} {subject_label} documentation cours pdf"

        google_docs = AICourseGenerator._search_google_docs(search_query, max_results=3)

        if google_docs and GOOGLE_AVAILABLE:
            for doc in google_docs:
                Document.objects.create(
                    course=course,
                    title=doc['title'],
                    url=doc['link']
                )
        else:
            # Fallback vers des liens Google Search quand l'API n'est pas disponible
            fallback_docs = {
                'sociology': [
                    {'title': f'Documentation sociologie - {course_title}', 'url': f'https://www.google.com/search?q={course_title.replace(" ", "+")}+sociologie+documentation+cours+pdf'},
                    {'title': f'Théories sociologiques - {course_title}', 'url': f'https://www.google.com/search?q={course_title.replace(" ", "+")}+théories+sociologiques+pdf'},
                    {'title': f'Méthodes de recherche en sociologie', 'url': f'https://www.google.com/search?q=méthodes+de+recherche+sociologie+{course_title.replace(" ", "+")}+pdf'},
                ],
                'science': [
                    {'title': f'Cours de sciences - {course_title}', 'url': f'https://www.google.com/search?q={course_title.replace(" ", "+")}+sciences+cours+pdf'},
                    {'title': f'Expériences scientifiques - {course_title}', 'url': f'https://www.google.com/search?q={course_title.replace(" ", "+")}+expériences+sciences+pdf'},
                    {'title': f'Principes scientifiques fondamentaux', 'url': f'https://www.google.com/search?q=principes+scientifiques+{course_title.replace(" ", "+")}+pdf'},
                ],
                'mathematics': [
                    {'title': f'Cours de mathématiques - {course_title}', 'url': f'https://www.google.com/search?q={course_title.replace(" ", "+")}+mathématiques+cours+pdf'},
                    {'title': f'Exercices de mathématiques - {course_title}', 'url': f'https://www.google.com/search?q={course_title.replace(" ", "+")}+exercices+mathématiques+pdf'},
                    {'title': f'Théorèmes mathématiques', 'url': f'https://www.google.com/search?q=théorèmes+mathématiques+{course_title.replace(" ", "+")}+pdf'},
                ]
            }

            # Utiliser les documents de fallback pour la matière
            subject_fallbacks = fallback_docs.get(subject, fallback_docs['sociology'])

            for doc in subject_fallbacks:
                Document.objects.create(
                    course=course,
                    title=doc['title'],
                    url=doc['url']
                )
    
    @staticmethod
    def _generate_quiz(course, difficulty, subject, course_title, user=None):
        """Génère un quiz avec ChatGPT adapté au niveau de l'étudiant"""
        user_level = None
        if user and hasattr(user, 'profile'):
            user_level = user.profile.level
        
        questions = AICourseGenerator._generate_quiz_with_chatgpt(
            course_title, subject, difficulty, user_level
        )
        
        Quiz.objects.create(
            course=course,
            title=f"Quiz - {course.title}",
            questions=questions
        )
    
    @staticmethod
    def _generate_exercises(course, difficulty, subject, course_title):
        """Génère des exercices avec ChatGPT"""
        exercise_count = {'beginner': 2, 'intermediate': 3, 'advanced': 4}.get(difficulty, 3)

        exercise_types = ['practice', 'analysis', 'project']

        # Mapping difficulté cours -> difficulté exercice
        difficulty_mapping = {
            'beginner': 'easy',
            'intermediate': 'medium',
            'advanced': 'hard'
        }

        for i in range(exercise_count):
            exercise_type = exercise_types[i % len(exercise_types)]
            exercise_data = AICourseGenerator._generate_exercise_with_chatgpt(
                course_title, subject, difficulty, exercise_type
            )

            # Utiliser le mapping pour la difficulté
            exercise_difficulty = difficulty_mapping.get(
                exercise_data.get('difficulty', difficulty),
                difficulty_mapping.get(difficulty, 'medium')
            )

            Exercise.objects.create(
                course=course,
                title=exercise_data.get('title', f'Exercice {i+1} - {course.title}'),
                content=exercise_data.get('content', 'Exercice généré automatiquement.'),
                difficulty=exercise_difficulty
            )
    
    @staticmethod
    def _get_difficulty_label(difficulty):
        """Retourne le label de difficulté"""
        labels = {'beginner': 'débutant', 'intermediate': 'intermédiaire', 'advanced': 'avancé'}
        return labels.get(difficulty, 'intermédiaire')
    
    @staticmethod
    def _get_subject_label(subject):
        """Retourne le label de la matière"""
        labels = {
            'sociology': 'sociologie',
            'mathematics': 'mathématiques',
            'science': 'sciences',
            'history': 'histoire',
            'literature': 'littérature',
            'philosophy': 'philosophie',
            'psychology': 'psychologie',
            'economics': 'économie',
            'languages': 'langues',
            'arts': 'arts',
            'geography': 'géographie',
            'computer_science': 'informatique'
        }
        return labels.get(subject, subject)
    
    @staticmethod
    def generate_course_based_on_emotion(user, emotion_type):
        """
        Génère un cours basé sur l'émotion de l'utilisateur dans une matière appropriée
        """
        # Obtenir les matières recommandées pour cette émotion
        recommended_subjects = AICourseGenerator.get_subjects_by_emotion(emotion_type)
        subject = random.choice(recommended_subjects)
        
        # Mapping émotion -> difficulté
        emotion_to_difficulty = {
            'happy': 'intermediate',
            'excited': 'advanced',
            'focused': 'advanced',
            'neutral': 'intermediate',
            'confused': 'beginner',
            'sad': 'beginner'
        }
        
        difficulty = emotion_to_difficulty.get(emotion_type, 'intermediate')
        
        # Adapter selon le profil utilisateur
        if hasattr(user, 'profile'):
            user_level = user.profile.level
            if user_level == 'beginner' and difficulty == 'advanced':
                difficulty = 'intermediate'
        
        # Générer le cours
        course = AICourseGenerator.generate_course(
            difficulty=difficulty,
            subject=subject,
            user=user
        )
        
        return course
    
    @staticmethod
    def generate_multiple_courses_by_emotion(user, emotion_type, count=3):
        """
        Génère plusieurs cours dans différentes matières selon l'émotion
        """
        recommended_subjects = AICourseGenerator.get_subjects_by_emotion(emotion_type)
        emotion_to_difficulty = {
            'happy': 'intermediate',
            'excited': 'advanced',
            'focused': 'advanced',
            'neutral': 'intermediate',
            'confused': 'beginner',
            'sad': 'beginner'
        }
        difficulty = emotion_to_difficulty.get(emotion_type, 'intermediate')
        
        # Adapter selon le profil utilisateur
        if hasattr(user, 'profile'):
            user_level = user.profile.level
            if user_level == 'beginner' and difficulty == 'advanced':
                difficulty = 'intermediate'
        
        courses = []
        # Générer un cours par matière recommandée (jusqu'à count)
        subjects_to_use = recommended_subjects[:count] if len(recommended_subjects) >= count else recommended_subjects
        
        for subject in subjects_to_use:
            course = AICourseGenerator.generate_course(
                difficulty=difficulty,
                subject=subject,
                user=user
            )
            courses.append(course)
        
        return courses
    
    @staticmethod
    def generate_course_based_on_profile(user):
        """
        Génère un cours basé sur le profil de l'utilisateur
        """
        profile = user.profile
        difficulty = profile.level
        
        # Sélectionner une matière aléatoire
        all_subjects = list(AICourseGenerator.COURSE_TEMPLATES.keys())
        subject = random.choice(all_subjects)
        
        course = AICourseGenerator.generate_course(
            difficulty=difficulty,
            subject=subject,
            user=user
        )
        
        return course
