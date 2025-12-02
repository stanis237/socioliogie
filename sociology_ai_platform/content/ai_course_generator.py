"""
Service d'IA pour générer automatiquement des cours dans toutes les matières
"""
import random
from .models import Course, Video, Quiz, Exercise

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
    
    QUIZ_QUESTIONS_TEMPLATES = {
        'beginner': [
            {'question': 'Quel est le concept fondamental de cette matière ?', 
             'options': ['Option A', 'Option B', 'Option C', 'Option D'], 'correct': 0},
        ],
        'intermediate': [
            {'question': 'Comment appliquer ce concept dans un contexte réel ?', 
             'options': ['Méthode 1', 'Méthode 2', 'Méthode 3', 'Méthode 4'], 'correct': 0},
        ],
        'advanced': [
            {'question': 'Quelle est l\'approche théorique la plus appropriée ?', 
             'options': ['Théorie A', 'Théorie B', 'Théorie C', 'Théorie D'], 'correct': 0},
        ]
    }
    
    EXERCISE_TEMPLATES = {
        'beginner': [
            {'title': 'Exercice pratique de base', 'content': 'Appliquez les concepts fondamentaux à un cas concret.', 'difficulty': 'easy'},
        ],
        'intermediate': [
            {'title': 'Analyse approfondie', 'content': 'Réalisez une analyse détaillée en utilisant les concepts appris.', 'difficulty': 'medium'},
        ],
        'advanced': [
            {'title': 'Projet de recherche', 'content': 'Développez un projet complet intégrant les concepts avancés.', 'difficulty': 'hard'},
        ]
    }
    
    @staticmethod
    def get_subjects_by_emotion(emotion_type):
        """Retourne les matières recommandées selon l'émotion"""
        return AICourseGenerator.EMOTION_TO_SUBJECTS.get(emotion_type, ['sociology', 'history', 'literature'])
    
    @staticmethod
    def generate_course(topic=None, difficulty='intermediate', subject='sociology', user_preferences=None):
        """
        Génère un cours complet avec son contenu
        
        Args:
            topic: Sujet du cours (optionnel)
            difficulty: Niveau de difficulté (beginner, intermediate, advanced)
            subject: Matière du cours
            user_preferences: Préférences de l'utilisateur (optionnel)
        """
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
            subject=subject
        )
        
        # Générer des vidéos
        AICourseGenerator._generate_videos(course, difficulty, subject)
        
        # Générer un quiz
        AICourseGenerator._generate_quiz(course, difficulty)
        
        # Générer des exercices
        AICourseGenerator._generate_exercises(course, difficulty)
        
        return course
    
    @staticmethod
    def _generate_videos(course, difficulty, subject):
        """Génère des vidéos pour le cours"""
        video_count = {'beginner': 3, 'intermediate': 4, 'advanced': 5}.get(difficulty, 4)
        
        video_titles_base = {
            'beginner': ['Introduction et concepts de base', 'Applications pratiques', 'Conclusion et synthèse'],
            'intermediate': ['Introduction théorique', 'Analyse approfondie', 'Cas pratiques', 'Conclusion et perspectives'],
            'advanced': ['Cadre théorique avancé', 'Méthodologies complexes', 'Analyses critiques', 'Débats contemporains', 'Synthèse et réflexions']
        }
        
        titles = video_titles_base.get(difficulty, video_titles_base['intermediate'])
        
        for i, title in enumerate(titles[:video_count]):
            Video.objects.create(
                course=course,
                title=f"{course.title} - {title}",
                url=f"https://example.com/video/{course.id}/{i+1}",
                duration=f"{random.randint(10, 30)}:00"
            )
    
    @staticmethod
    def _generate_quiz(course, difficulty):
        """Génère un quiz pour le cours"""
        questions_template = AICourseGenerator.QUIZ_QUESTIONS_TEMPLATES.get(
            difficulty, 
            AICourseGenerator.QUIZ_QUESTIONS_TEMPLATES['intermediate']
        )
        
        selected_questions = random.sample(
            questions_template, 
            min(len(questions_template), random.randint(3, 5))
        )
        
        questions = []
        for q in selected_questions:
            questions.append({
                'question': q['question'],
                'options': q['options'],
                'correct': q['correct']
            })
        
        Quiz.objects.create(
            course=course,
            title=f"Quiz - {course.title}",
            questions=questions
        )
    
    @staticmethod
    def _generate_exercises(course, difficulty):
        """Génère des exercices pour le cours"""
        exercise_template = AICourseGenerator.EXERCISE_TEMPLATES.get(
            difficulty,
            AICourseGenerator.EXERCISE_TEMPLATES['intermediate']
        )
        
        exercise_count = {'beginner': 2, 'intermediate': 3, 'advanced': 4}.get(difficulty, 3)
        
        selected_exercises = random.sample(
            exercise_template,
            min(len(exercise_template), exercise_count)
        )
        
        for ex in selected_exercises:
            Exercise.objects.create(
                course=course,
                title=f"{ex['title']} - {course.title}",
                content=ex['content'],
                difficulty=ex['difficulty']
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
        
        # Générer le cours
        course = AICourseGenerator.generate_course(
            difficulty=difficulty,
            subject=subject
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
        
        courses = []
        # Générer un cours par matière recommandée (jusqu'à count)
        subjects_to_use = recommended_subjects[:count] if len(recommended_subjects) >= count else recommended_subjects
        
        for subject in subjects_to_use:
            course = AICourseGenerator.generate_course(
                difficulty=difficulty,
                subject=subject
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
            subject=subject
        )
        
        return course
