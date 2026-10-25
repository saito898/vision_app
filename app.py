
import os
import streamlit as st
import base64
from openai import OpenAI


# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Análisis de Imagen | AI Vision",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# ESTILOS VISUALES
# --------------------------------------------------

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(0, 190, 220, 0.09),
            transparent 38%
        ),
        #080D18;
    color: #E6EDF7;
}

/* Contenedor principal */
.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

/* Textos */
html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", sans-serif;
}

h1, h2, h3 {
    color: #F2F7FC !important;
    letter-spacing: -0.7px;
}

p, label, .stMarkdown {
    color: #B8C6D9;
}

/* Encabezado */
.vision-header {
    text-align: center;
    padding: 1.5rem 0 2rem 0;
}

.vision-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 68px;
    height: 68px;
    border: 1px solid rgba(0, 220, 255, 0.35);
    border-radius: 20px;
    background: rgba(0, 210, 255, 0.08);
    color: #35E0F5;
    font-size: 36px;
    margin-bottom: 1rem;
    box-shadow: 0 0 35px rgba(0, 210, 255, 0.08);
}

.vision-title {
    font-size: 2.35rem;
    font-weight: 750;
    color: #F2F7FC;
    letter-spacing: -1.4px;
    margin: 0;
}

.vision-subtitle {
    font-size: 1rem;
    color: #8294AC;
    margin-top: 0.65rem;
}

.vision-tag {
    display: inline-block;
    margin-top: 1rem;
    padding: 5px 12px;
    border: 1px solid rgba(53, 224, 245, 0.25);
    border-radius: 20px;
    color: #35E0F5;
    background: rgba(53, 224, 245, 0.06);
    font-size: 0.72rem;
    letter-spacing: 1.5px;
    font-weight: 600;
}

/* Tarjetas de sección */
.section-card {
    background: #101827;
    border: 1px solid #243248;
    border-radius: 16px;
    padding: 1.4rem;
    margin: 1rem 0;
}

.section-heading {
    color: #E6EDF7;
    font-size: 1.05rem;
    font-weight: 650;
    margin-bottom: 0.3rem;
}

.section-description {
    color: #8294AC;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* Campos de texto */
.stTextInput input,
.stTextArea textarea {
    background-color: #0B1220 !important;
    color: #E6EDF7 !important;
    border: 1px solid #2A3A50 !important;
    border-radius: 10px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #28CDE3 !important;
    box-shadow: 0 0 0 1px #28CDE3 !important;
}

/* Área de carga */
[data-testid="stFileUploader"] {
    background: #0B1220;
    border: 1px dashed #34506A;
    border-radius: 12px;
    padding: 1rem;
    transition: border-color 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #28CDE3;
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

[data-testid="stFileUploader"] button {
    background: #18273A !important;
    color: #C9D8E8 !important;
    border: 1px solid #344A63 !important;
    border-radius: 8px !important;
}

/* Botones */
.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 10px;
    border: 1px solid #28CDE3;
    background: linear-gradient(135deg, #13B8D1, #087DAB);
    color: #FFFFFF;
    font-size: 0.96rem;
    font-weight: 650;
    letter-spacing: 0.2px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #66EDFA;
    background: linear-gradient(135deg, #25D2E8, #0B9DCC);
    color: #FFFFFF;
    box-shadow: 0 5px 22px rgba(0, 200, 230, 0.16);
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Interruptor */
[data-testid="stToggle"] label {
    color: #C9D8E8;
}

/* Imagen cargada */
[data-testid="stImage"] img {
    border-radius: 12px;
}

/* Expansor */
[data-testid="stExpander"] {
    background: #101827;
    border: 1px solid #243248;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    color: #DCE8F5;
}

/* Separadores */
hr {
    border-color: #243248;
    margin: 1.5rem 0;
}

/* Alertas */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Respuesta del análisis */
.analysis-label {
    color: #35E0F5;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.7px;
    margin-bottom: 0.6rem;
}

/* Pie de página */
.vision-footer {
    text-align: center;
    color: #52647B;
    font-size: 0.78rem;
    margin-top: 3rem;
    padding-top: 1.3rem;
    border-top: 1px solid #1D2A3C;
}

.vision-footer span {
    color: #35CDE1;
}

/* Ajustes para pantallas pequeñas */
@media (max-width: 600px) {
    .block-container {
        padding-top: 1.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .vision-title {
        font-size: 1.85rem;
    }

    .section-card {
        padding: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FUNCIONES
# --------------------------------------------------

def encode_image(image_file):
    return base64.b64encode(
        image_file.getvalue()
    ).decode("utf-8")


# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.markdown("""
<div class="vision-header">
    <div class="vision-icon">◈</div>
    <div class="vision-title">Análisis de Imagen</div>
    <div class="vision-subtitle">
        Inteligencia artificial para interpretar el mundo visual.
    </div>
    <div class="vision-tag">AI VISION SYSTEM</div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CLAVE DE OPENAI
# --------------------------------------------------

st.markdown("""
<div class="section-heading">01 / Conexión</div>
<div class="section-description">
    Ingresa tu clave para conectar con el sistema de inteligencia artificial.
</div>
""", unsafe_allow_html=True)

ke = st.text_input(
    "Clave de API de OpenAI",
    type="password",
    placeholder="sk-...",
    help="Tu clave se utiliza para realizar el análisis."
)

os.environ["OPENAI_API_KEY"] = ke

api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)


st.markdown("<hr>", unsafe_allow_html=True)


# --------------------------------------------------
# CARGA DE IMAGEN
# --------------------------------------------------

st.markdown("""
<div class="section-heading">02 / Imagen de entrada</div>
<div class="section-description">
    Selecciona una imagen para que la inteligencia artificial la interprete.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Selecciona tu imagen",
    type=["jpg", "png", "jpeg"],
    help="Formatos permitidos: JPG, JPEG y PNG."
)

if uploaded_file:
    with st.expander("Vista previa de la imagen", expanded=True):
        st.image(
            uploaded_file,
            caption=uploaded_file.name,
            use_container_width=True
        )


# --------------------------------------------------
# CONTEXTO OPCIONAL
# --------------------------------------------------

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
<div class="section-heading">03 / Contexto adicional</div>
<div class="section-description">
    Personaliza el análisis con una pregunta o información específica.
</div>
""", unsafe_allow_html=True)

show_details = st.toggle(
    "Quiero hacer una pregunta específica sobre la imagen",
    value=False
)

if show_details:
    additional_details = st.text_area(
        "¿Qué quieres saber?",
        placeholder=(
            "Ejemplo: Describe los objetos que aparecen, "
            "explica qué está sucediendo o identifica los colores..."
        ),
        disabled=not show_details
    )


# --------------------------------------------------
# BOTÓN DE ANÁLISIS
# --------------------------------------------------

st.markdown("<hr>", unsafe_allow_html=True)

analyze_button = st.button(
    "◈  Analizar imagen",
    type="secondary",
    use_container_width=True
)


# --------------------------------------------------
# ANÁLISIS CON OPENAI
# --------------------------------------------------

if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("Procesando imagen con inteligencia artificial..."):

        base64_image = encode_image(uploaded_file)

        prompt_text = (
            "Describe what you see in the image in spanish"
        )

        if show_details and additional_details:
            prompt_text += (
                f"\n\nAdditional Context Provided by the User:\n"
                f"{additional_details}"
            )

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:image/jpeg;base64,{base64_image}"
                            )
                        }
                    }
                ]
            }
        ]

        try:
            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("""
            <div class="section-heading">04 / Resultado</div>
            <div class="section-description">
                Interpretación generada a partir de la imagen.
            </div>
            <div class="analysis-label">ANÁLISIS EN TIEMPO REAL</div>
            """, unsafe_allow_html=True)

            full_response = ""
            message_placeholder = st.empty()

            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Ocurrió un error durante el análisis: {e}")

else:
    if not uploaded_file and analyze_button:
        st.warning("Primero debes cargar una imagen.")

    if not api_key:
        st.warning("Ingresa tu clave de API para continuar.")


# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.markdown("""
<div class="vision-footer">
    <span>◈ AI VISION</span> &nbsp;·&nbsp;
    Análisis visual impulsado por inteligencia artificial
</div>
""", unsafe_allow_html=True)
