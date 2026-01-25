import os
import random
import schedule
import time
import requests
import sys
import re
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

if not all([PERPLEXITY_API_KEY, LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN, PIXABAY_API_KEY]):
    raise ValueError("❌ Faltan variables en .env")

client = OpenAI(
    api_key=PERPLEXITY_API_KEY,
    base_url="https://api.perplexity.ai"
)

# ========== TOPICS EJECUTIVOS (Generalista, no técnico bajo nivel) ==========
TOPICS = [
    # ===== AI & BUSINESS IMPACT =====
    "¿Cómo 2026 cambia la adopción empresarial de IA agéntica?",
    "Inversión en talento técnico: el nuevo cuello de botella",
    "La paradoja de la automatización: menos código, más arquitectos",
    "From AI Experiments to AI-Driven Revenue",
    "Startup Stack 2026: tech choices that matter",
    "El costo real de construir vs. comprar tecnología",
    "IA agéntica: del experimento al ROI",
    
    # ===== TEAM & CULTURE =====
    "Building engineering cultures that scale beyond 100 people",
    "The era of specialist engineers vs. generalists",
    "Remote-first engineering: lessons from distributed teams",
    "Developer productivity: measuring what matters",
    "Retaining senior engineers in a hyper-competitive market",
    "Technical debt: cuando la deuda técnica es una inversión",
    
    # ===== PRODUCT & STRATEGY =====
    "Fast iteration or stable architecture? False dichotomy",
    "Data-driven decisions: from experimentation to conviction",
    "When to build vs. buy: the hidden costs of DIY",
    "Open source as competitive advantage",
    "Feature parity trap: why you're losing to smaller competitors",
    "Technical strategy: aligning engineering with business",
    
    # ===== INFRASTRUCTURE & SCALE =====
    "Serverless, containers, or VMs? Architecture decisions that compound",
    "Database selection: the choice that haunts you later",
    "Cost optimization: engineering discipline, not accounting",
    "Scaling from startup to enterprise: inflection points",
    "Infrastructure as competitive advantage",
    
    # ===== SECURITY & RELIABILITY =====
    "Security from day one: not a feature you add later",
    "Building resilient systems: chaos engineering for startups",
    "The cost of downtime: more than you think",
    "Privacy regulations: the new competitive differentiator",
    "Zero-trust architecture: necessary or overengineering?",
]

def extraer_query_imagen_del_contenido(post_text, tema=None):
    """
    Analiza PROFUNDAMENTE el contenido del post para generar queries PRECISAS.
    
    🎯 MEJORA: Multi-criterio contextual
    - Busca múltiples palabras clave
    - Combina contexto para queries más específicas
    - Prioriza combinaciones temáticas
    - Muestra análisis en logs
    """
    
    post_lower = post_text.lower()
    
    # Patrones específicos: (palabras clave) -> (queries de imagen)
    keyword_patterns = {
        # PRODUCT & STRATEGY
        'product': ['product design', 'product strategy', 'innovation'],
        'feature': ['feature development', 'product roadmap', 'design thinking'],
        'competitive': ['competition', 'market strategy', 'business advantage'],
        'strateg': ['strategy', 'planning', 'business roadmap'],
        'portafolio': ['portfolio management', 'product', 'business planning'],
        'decisión': ['decision making', 'planning', 'strategy'],
        'trade-off': ['balance', 'choice', 'equilibrium'],
        'roadmap': ['product roadmap', 'planning', 'strategy'],
        
        # TEAM & ORGANIZATION
        'equipo': ['team collaboration', 'teamwork', 'diverse team working'],
        'team': ['team collaboration', 'teamwork', 'group meeting'],
        'cultura': ['company culture', 'team culture', 'workplace'],
        'liderazgo': ['leadership', 'mentoring', 'executive'],
        'organizacional': ['organization', 'structure', 'management'],
        'ingeniero': ['engineers', 'technical team', 'professionals'],
        'talento': ['talent', 'people', 'professionals'],
        
        # BUSINESS & GROWTH & ECONOMICS
        'crecimiento': ['business growth', 'expansion', 'success'],
        'escala': ['growth', 'scaling business', 'expansion'],
        'negocio': ['business', 'entrepreneurship', 'startup office'],
        'roi': ['financial success', 'profit', 'growth'],
        'revenue': ['revenue growth', 'income', 'financial success'],
        'adopción': ['adoption', 'growth', 'technology adoption'],
        'unit economics': ['business metrics', 'financial planning', 'business growth'],
        'ltv': ['customer value', 'business metrics', 'growth'],
        'churn': ['customer retention', 'business metrics', 'growth'],
        'payback': ['financial metrics', 'business success', 'profitability'],
        'saas': ['SaaS business', 'subscription model', 'business growth'],
        'infra': ['infrastructure', 'technology', 'business efficiency'],
        
        # TECHNICAL DECISIONS
        'arquitectura': ['architecture', 'blueprint', 'planning'],
        'infraestructur': ['cloud', 'infrastructure', 'technology'],
        'datos': ['data', 'analytics', 'database visualization'],
        'base de datos': ['database', 'data storage', 'technology'],
        'seguridad': ['security', 'protection', 'cybersecurity'],
        'stack': ['technology stack', 'infrastructure', 'software development'],
        
        # INNOVATION & TECHNOLOGY
        'ia': ['artificial intelligence', 'AI', 'technology'],
        'agente': ['automation', 'AI', 'technology workflow'],
        'automatización': ['automation', 'efficiency', 'workflow'],
        'digital': ['digital transformation', 'technology', 'innovation'],
        'innovación': ['innovation', 'future', 'technology'],
        
        # FINANCIAL & OPTIMIZATION & COST
        'costo': ['cost optimization', 'finance', 'business efficiency'],
        'coste': ['cost optimization', 'finance', 'business efficiency'],
        'optimización': ['optimization', 'efficiency', 'business planning'],
        'presupuesto': ['budget', 'finance', 'business planning'],
        'gastar': ['expense', 'budget', 'financial planning'],
        'inversión': ['investment', 'strategic planning', 'business growth'],
        'margin': ['profitability', 'business metrics', 'growth'],
        'disciplina': ['discipline', 'planning', 'strategy'],
        'excel': ['financial planning', 'business metrics', 'accounting'],
        'p&l': ['profitability', 'financial metrics', 'business growth'],
        
        # LEARNING & DEVELOPMENT
        'aprendizaje': ['learning', 'education', 'development'],
        'desarrollo': ['development', 'growth', 'learning'],
        'productividad': ['productivity', 'efficiency', 'team working'],
        
        # RELIABILITY & QUALITY
        'resiliente': ['reliability', 'strong', 'robust'],
        'downtime': ['crisis', 'recovery', 'failure'],
        'confiabilidad': ['reliability', 'trust', 'stability'],
    }
    
    # ========== BÚSQUEDA MULTI-CRITERIO ==========
    print(f"  🔎 Análisis contextual del contenido...")
    
    # 1. Buscar coincidencias
    matches_encontrados = {}
    for keyword, queries in keyword_patterns.items():
        if keyword in post_lower:
            matches_encontrados[keyword] = queries
            print(f"     ✓ Detectado: '{keyword}'")
    
    if not matches_encontrados:
        print(f"     ℹ️ Sin palabras clave exactas, usando fallback del tema...")
        if tema:
            palabras_tema = tema.lower().split()
            for palabra in palabras_tema:
                for keyword, queries in keyword_patterns.items():
                    if palabra in keyword:
                        matches_encontrados[keyword] = queries
                        print(f"     ✓ Detectado (tema): '{keyword}'")
                        break
    
    if not matches_encontrados:
        print(f"     → Query genérica")
        return random.choice([
            'business strategy',
            'leadership meeting',
            'innovation',
            'teamwork',
            'professional growth',
            'business planning'
        ])
    
    # 2. Prioridad: combinar contexto relevante
    if len(matches_encontrados) > 1:
        print(f"     📊 Múltiples contextos detectados ({len(matches_encontrados)}), priorizando...")
        
        # Prioridades: Economics > Strategy > People > Tech
        priority_order = [
            'unit economics', 'ltv', 'churn', 'payback', 'p&l', 'excel',
            'costo', 'coste', 'margin', 'disciplina',
            'strateg', 'decisión', 'roadmap', 'inversión',
            'equipo', 'team', 'liderazgo', 'talento',
            'ia', 'arquitectura', 'infraestructur', 'stack', 'saas'
        ]
        
        primary_keyword = None
        for priority_kw in priority_order:
            if priority_kw in matches_encontrados:
                primary_keyword = priority_kw
                print(f"     🎯 Prioridad elegida: '{priority_kw}'")
                break
        
        if not primary_keyword:
            primary_keyword = list(matches_encontrados.keys())[0]
        
        queries_primary = matches_encontrados[primary_keyword]
        selected_query = random.choice(queries_primary)
        
        return selected_query
    
    # 3. Si solo hay un match
    single_keyword = list(matches_encontrados.keys())[0]
    queries = matches_encontrados[single_keyword]
    selected_query = random.choice(queries)
    
    return selected_query

def buscar_imagen_pixabay(search_query):
    """Busca imagen RELEVANTE en Pixabay"""
    
    if not PIXABAY_API_KEY:
        print("  ⚠️ PIXABAY_API_KEY no configurada, saltando imagen")
        return None
    
    try:
        print(f"  🔍 Buscando imagen para: '{search_query}'...")
        
        response = requests.get(
            "https://pixabay.com/api/",
            params={
                "key": PIXABAY_API_KEY,
                "q": search_query,
                "per_page": 15,
                "orientation": "landscape",
                "image_type": "photo",
                "order": "popular",
                "category": "business"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data['hits']:
                photo = random.choice(data['hits'])
                
                image_info = {
                    "url": photo['largeImageURL'],
                    "thumb": photo['webformatURL'],
                    "credit": photo['user'],
                    "source": "Pixabay"
                }
                
                print(f"  ✅ Imagen encontrada: {search_query}")
                
                return image_info
        
        print(f"  ⚠️ No encontramos imagen para '{search_query}'")
        return None
        
    except requests.exceptions.Timeout:
        print("  ⚠️ Timeout buscando imagen")
        return None
    except Exception as e:
        print(f"  ⚠️ Error buscando imagen: {e}")
        return None

def registrar_imagen_en_linkedin(image_url, image_credit):
    """
    Registra una imagen en LinkedIn usando registerUpload
    """
    
    try:
        print(f"  📥 Registrando imagen en LinkedIn...")
        
        register_payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": LINKEDIN_PERSON_URN,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        
        register_response = requests.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            json=register_payload,
            headers={
                "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            timeout=15
        )
        
        if register_response.status_code != 200:
            print(f"  ❌ Error registrando: {register_response.status_code}")
            return None
        
        register_data = register_response.json()
        
        if 'value' not in register_data or 'uploadMechanism' not in register_data['value']:
            print(f"  ❌ Respuesta inesperada")
            return None
        
        upload_url = register_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset_urn = register_data['value']['asset']
        
        print(f"  ☁️ Uploadando imagen...")
        
        image_response = requests.get(image_url, timeout=15)
        if image_response.status_code != 200:
            print(f"  ❌ Error descargando imagen")
            return None
        
        upload_response = requests.put(
            upload_url,
            data=image_response.content,
            headers={"Content-Type": "image/jpeg"},
            timeout=30
        )
        
        if upload_response.status_code not in [200, 201]:
            print(f"  ❌ Error uploadando")
            return None
        
        print(f"  ✅ Imagen registrada")
        return asset_urn
        
    except Exception as e:
        print(f"  ❌ Error en registro/upload: {e}")
        return None

def buscar_noticias_recientes():
    """Busca noticias recientes con perspectiva ejecutiva"""
    
    try:
        print(f"  📰 Buscando noticias recientes...")
        
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "user",
                    "content": """Dame 2-3 noticias RECIENTES (últimos 7 días) sobre:
- IA y business impact
- Tech talent y hiring
- Startup tech decisions
- Engineering leadership
- Product strategy

Formato: Qué pasó, impacto en negocio. Sin términos técnicos. Máx 150 palabras.
IMPORTANTE: Sin faltas de ortografía ni gramática."""
                }
            ],
            max_tokens=300,
            temperature=0.5
        )
        
        noticias = response.choices[0].message.content.strip()
        noticias = re.sub(r'\[\d+\]', '', noticias)
        noticias = re.sub(r'\s+', ' ', noticias)
        
        print(f"  ✅ Noticias encontradas")
        return noticias
        
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
        return None

def buscar_contexto_actualizado(topic):
    """Busca contexto ejecutivo sobre el topic"""
    
    try:
        print(f"  🔍 Buscando contexto: {topic}...")
        
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "user",
                    "content": f"""Resumen ejecutivo (máx 150 palabras) sobre: '{topic}'

Perspectiva: Por qué importa para CTOs, founders, tech leaders
Incluye: 1 dato actual (si aplica)
Evita: Detalles técnicos, código, jerga low-level

IMPORTANTE: Sin faltas de ortografía ni gramática.
Contexto para 2026."""
                }
            ],
            max_tokens=300,
            temperature=0.5
        )
        
        contexto = response.choices[0].message.content.strip()
        contexto = re.sub(r'\[\d+\]', '', contexto)
        contexto = re.sub(r'\s+', ' ', contexto)
        
        print(f"  ✅ Contexto obtenido")
        return contexto
        
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
        return None

def agregar_parrafos_inteligentes(texto):
    """
    Agrega párrafos inteligentemente al texto del post.
    Los hashtags van todos juntos en una línea al final.
    """
    
    # Primero extraer los hashtags
    hashtags = re.findall(r'#\w+', texto)
    
    # Remover hashtags del texto
    texto_sin_hashtags = re.sub(r'\n?#\w+\n?', '', texto).strip()
    
    # Separadores lógicos que indican inicio de párrafo
    separadores = [
        '. Un ',
        '. La ',
        '. Dos ',
        '. Tres ',
        '. En ',
        '. Con ',
        '. Sin ',
        '. Por ',
        '. Esto ',
        '. Se ',
        '. Es ',
        '. Hoy ',
        '. En 2026',
        '. Cuando ',
        '. Si ',
        '. Mientras ',
        '. Además ',
        '. Por eso ',
        '. Más allá ',
        '. Lo real ',
    ]
    
    # Aplicar separadores
    resultado = texto_sin_hashtags
    for sep in separadores:
        resultado = resultado.replace(sep, f'.\n\n{sep[2:]}')
    
    # Limpiar múltiples saltos
    resultado = re.sub(r'\n\n+', '\n\n', resultado)
    
    # Agregar los hashtags al final en una sola línea
    if hashtags:
        resultado = resultado.strip() + '\n\n' + ' '.join(hashtags)
    
    return resultado.strip()

def corregir_ortografia_y_gramatica(texto):
    """
    Corrige ortografía, gramática y puntuación del texto.
    Usa LLM para garantizar corrección perfecta.
    """
    
    try:
        print(f"  ✏️ Corrigiendo ortografía, gramática y puntuación...")
        
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "user",
                    "content": f"""Corrige SOLO ortografía, gramática y puntuación. 
NO cambies el contenido, ni el tono, ni el significado.
NO cambies el formato de los hashtags (deben ir todos en una línea al final).
SOLO correcciones ortográficas y gramaticales.

Texto original:
{texto}

Responde SOLO con el texto corregido, sin explicaciones."""
                }
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        texto_corregido = response.choices[0].message.content.strip()
        
        if not texto_corregido or len(texto_corregido) < len(texto) * 0.5:
            print(f"  ⚠️ Corrección fallida, usando original")
            return texto
        
        print(f"  ✅ Texto corregido correctamente")
        return texto_corregido
        
    except Exception as e:
        print(f"  ⚠️ Error al corregir: {e}")
        return texto

def generar_post_con_noticias_o_topic(usar_noticias, noticias=None, topic=None, contexto=None):
    """Genera post EJECUTIVO (no técnico bajo nivel)"""
    
    if usar_noticias and noticias:
        prompt = f"""
Eres un CTO/VP Engineering escribiendo insights sobre noticias tech recientes.
Audiencia: CTOs, VP Product, Tech Leaders, Founders

NOTICIAS:
{noticias}

REQUISITOS:
- Perspectiva: Por qué importa al NEGOCIO, no al código
- Largo: 600-800 caracteres
- Ejemplos: 1-2 casos concretos (business outcomes, no implementation)
- Tono: Reflexivo, estratégico, experiencia
- 3-4 hashtags al final en una línea separada
- Evita: Jerga técnica específica, low-level details
- Español
- USA PUNTOS (.) para separar ideas, eso me ayuda a agregar párrafos
- CRÍTICO: Sin faltas de ortografía, gramática ni puntuación
- No cerrar siempre con una pregunta
- No utilizar formato Markdown

Formato de hashtags (UNA LÍNEA AL FINAL):
#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4

Responde SOLO con el post.
"""
    else:
        prompt = f"""
Eres un CTO/VP Engineering escribiendo insights estratégicos.
Especialidad: IA agéntica, tech decisions, team building, product strategy
Audiencia: CTOs, Tech Leaders, Founders, VP Product

TEMA: {topic}

CONTEXTO:
{contexto}

REQUISITOS:
- Perspectiva: Por qué importa al negocio/organización
- Largo: 600-800 caracteres
- Enfoque: DECISIONES y TRADE-OFFS, no implementación
- Ejemplos: 1-2 casos de negocio reales (no técnicos)
- Tono: Reflexivo, pragmático, experience-driven
- 3-4 hashtags al final en una línea separada
- Estructura: Usa PUNTOS (.) para separar ideas diferentes, eso me ayuda a agregar párrafos
- CRÍTICO: Sin faltas de ortografía, gramática ni puntuación
- No cerrar siempre con una pregunta
- No utilizar formato Markdown

Formato de hashtags (UNA LÍNEA AL FINAL):
#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4

- Evita: 
  * Jerga técnica específica (indices, LoRA, DAG, etc)
  * Código o pseudocódigo
  * Términos low-level
  * Recomendaciones genéricas
- Español

Responde SOLO con el post.
"""
    
    try:
        print(f"  ✍️ Generando post...")
        
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        
        text = response.choices[0].message.content.strip()
        text = text.replace("**", "").replace("*", "").replace("##", "").replace("`", "")
        text = re.sub(r'\[\d+\]', '', text)
        
        text = agregar_parrafos_inteligentes(text)
        text = corregir_ortografia_y_gramatica(text)
        
        return text
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def publicar_en_linkedin(post_content, asset_urn=None):
    """Publica post en LinkedIn con imagen opcional"""
    
    try:
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        
        if asset_urn:
            data = {
                "author": LINKEDIN_PERSON_URN,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": post_content},
                        "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {"text": ""},
                                "media": asset_urn
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
        else:
            data = {
                "author": LINKEDIN_PERSON_URN,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": post_content},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
        
        headers = {
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        
        print("  📤 Publicando en LinkedIn...")
        response = requests.post(post_url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 201:
            print(f"  ✅ ¡Publicado!")
            if asset_urn:
                print(f"     📷 Con imagen")
            return True
        else:
            print(f"  ❌ Error ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"  ❌ Error publicando: {e}")
        return False

def generar_y_publicar():
    """Pipeline completo"""
    
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        usar_noticias = random.choice([True, False])
        
        print(f"\n{'='*70}")
        if usar_noticias:
            print(f"[{timestamp}] Generando post: NOTICIAS RECIENTES")
        else:
            print(f"[{timestamp}] Generando post: TEMA ESTRATÉGICO")
        print(f"{'='*70}")
        
        if usar_noticias:
            noticias = buscar_noticias_recientes()
            if not noticias:
                print("⚠️ No se encontraron noticias, usando tema estratégico")
                usar_noticias = False
            else:
                print(f"Noticias:\n{noticias[:100]}...\n")
                post = generar_post_con_noticias_o_topic(True, noticias=noticias)
                
                if not post:
                    return False
        
        if not usar_noticias:
            topic = random.choice(TOPICS)
            print(f"Tema: {topic}")
            
            contexto = buscar_contexto_actualizado(topic)
            if not contexto:
                return False
            
            print(f"Contexto:\n{contexto[:100]}...\n")
            post = generar_post_con_noticias_o_topic(False, topic=topic, contexto=contexto)
            
            if not post:
                return False
        
        print(f"✅ Post generado ({len(post)} caracteres)")
        print(f"\n📝 Contenido:")
        print(f"-" * 70)
        print(post)
        print(f"-" * 70)
        
        print(f"\n🖼️ Analizando contenido para imagen relevante...")
        image_query = extraer_query_imagen_del_contenido(post, topic if not usar_noticias else None)
        print(f"   ✓ Query final: '{image_query}'")
        
        imagen = buscar_imagen_pixabay(image_query)
        
        asset_urn = None
        if imagen:
            asset_urn = registrar_imagen_en_linkedin(imagen['url'], imagen['credit'])
        
        if publicar_en_linkedin(post, asset_urn):
            print(f"{'='*70}")
            print("✅✅ ¡POST PUBLICADO EN LINKEDIN!")
            if imagen and asset_urn:
                print(f"     📷 Con imagen: {image_query}")
            print(f"{'='*70}\n")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    
    immediate_mode = len(sys.argv) > 1 and sys.argv[1] == "now"
    
    if immediate_mode:
        print("⚡" * 30)
        print("MODO INMEDIATO: Generando y publicando ahora")
        print("⚡" * 30)
        generar_y_publicar()
        
    else:
        schedule.every(3.5).days.at("10:00").do(generar_y_publicar)
        
        print("\n" + "🚀" * 30)
        print("\n            BOT LINKEDIN - ANTONIO TRIGUERO")
        print("\n" + "🚀" * 30)
        print(f"\n  📊 Posts: 600-800 caracteres, nivel EJECUTIVO")
        print(f"     • Perspectiva: Negocio, no código")
        print(f"     • Audiencia: CTOs, Founders, VP Product")
        print(f"     • Enfoque: Decisiones estratégicas, trade-offs")
        print(f"     • Párrafos: Agrupados inteligentemente")
        print(f"     • Hashtags: Línea única al final")
        print(f"\n  📸 Imágenes: Análisis MULTI-CRITERIO")
        print(f"     • Detecta múltiples palabras clave en el post")
        print(f"     • Prioriza por relevancia (economics > strategy > people > tech)")
        print(f"     • Queries contextuales PRECISAS")
        print(f"     • Siempre alineadas con el mensaje")
        print(f"\n  ✏️ Corrección: ORTOGRAFÍA, GRAMÁTICA Y PUNTUACIÓN")
        print(f"     • Análisis LLM de cada post")
        print(f"     • Verificación antes de publicar")
        print(f"     • Cero tolerancia a errores")
        print(f"\n  📚 Contenido personalizado:")
        print(f"     • IA agéntica & Business Impact")
        print(f"     • Team Building & Culture")
        print(f"     • Product & Strategy")
        print(f"     • Infrastructure & Scale")
        print(f"     • Security & Reliability")
        print(f"     • 50% noticias, 50% temas estratégicos")
        print(f"\n  👤 Audiencia: CTOs, Founders, Tech Leaders, VP Product")
        print(f"\n  💰 Costo: $0.04/post (generación + corrección) + gratis (Pixabay)")
        print(f"\n  ⏰ Frecuencia: Automática cada 3.5 días a las 10:00")
        print(f"     O modo inmediato: python3 main.py now")
        print(f"\n{'='*70}\n")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
