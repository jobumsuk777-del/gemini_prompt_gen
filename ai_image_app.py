# pip install google-genai streamlit
import streamlit as st
from google import genai
from google.genai import types
import pyperclip

# -----------------------------------------------------------------------------
# 1. 페이지 설정 (Nano Banana Theme)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Nano Banana Prompt Studio (Hyper-Realism)",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스타일 정의 (Yellow & Dark Tech Theme)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%; height: 55px; font-size: 20px; font-weight: 800;
        background: linear-gradient(90deg, #FFD700 0%, #FFAA00 100%);
        color: #000000; border: none; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5); color: #000000; }
    
    /* 프롬프트 박스 스타일 */
    .prompt-box {
        background-color: #1e1e1e; padding: 25px; border-radius: 15px;
        border-left: 6px solid #FFD700; border: 1px solid #333;
        font-family: 'Courier New', monospace; color: #e0e0e0; line-height: 1.6;
    }
    
    /* 타이틀 스타일 */
    .title-text {
        font-size: 3rem; font-weight: 900; text-align: center;
        background: -webkit-linear-gradient(45deg, #FFD700, #FFF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 세션 및 사이드바 설정
# -----------------------------------------------------------------------------
if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""

st.sidebar.markdown("## ⚙️ ENGINE SETUP")
api_key = st.sidebar.text_input("Google API Key", type="password")

# 모델 선택
model_options = [
    "gemini-2.0-flash-exp", 
    "gemini-1.5-pro",
    "models/gemini-3-pro-image-preview",
    "models/gemini-2.5-flash-image",
    "models/imagen-4.0-generate-001",
    "models/imagen-4.0-ultra-generate-001"
]
selected_model = st.sidebar.selectbox("Select Model", model_options, index=0)

# Temperature 조절 슬라이더
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌡️ CREATIVITY")
temperature_val = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=1.0,
    step=0.05,
    help="0.0: 정적/논리적 | 2.0: 매우 창의적/무작위적"
)

# -----------------------------------------------------------------------------
# 3. 메인 UI 구성
# -----------------------------------------------------------------------------
st.markdown('<div class="title-text">🍌 NANO BANANA HYPER-REALISM</div>', unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#888; margin-bottom:30px;'>Unrestricted High-Fidelity Prompt Architect</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 INPUT CONCEPT")
    user_input = st.text_area("Concept", placeholder="Describe your imagination freely...", height=250, label_visibility="collapsed")
    generate_btn = st.button("⚡ GENERATE PROMPT")

with col2:
    st.subheader("📤 STRUCTURED OUTPUT")
    if st.session_state.generated_prompt:
        st.markdown(f'<div class="prompt-box">{st.session_state.generated_prompt}</div>', unsafe_allow_html=True)
        if st.button("📋 COPY", type="secondary"):
            try:
                pyperclip.copy(st.session_state.generated_prompt)
                st.toast("✅ Copied!", icon="🍌")
            except:
                st.warning("⚠️ Manual copy required.")
    else:
        st.markdown('<div class="prompt-box" style="color:#666; text-align:center;">Waiting for input...</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. 프롬프트 생성 로직 (핵심)
# -----------------------------------------------------------------------------
if generate_btn:
    if not user_input.strip():
        st.warning("⚠️ Please enter a concept first.")
    elif not api_key:
        st.error("🔒 API Key is missing.")
    else:
        try:
            with st.spinner("🍌 Processing Nano-Structures..."):
                client = genai.Client(api_key=api_key)
                
                # [핵심] 극실사/광학 물리 기반 'Nano Banana' 최적화 시스템 인스트럭션
                system_instruction = """
                You are the "Nano Banana Hyper-Realism Engine," a prompt architect designed to surpass standard AI image quality. Your goal is to generate prompts that create images indistinguishable from high-end digital photography.

                ### CORE DIRECTIVES:
                1.  **Material Physics:** Define "Nano Banana" not just as yellow, but as a complex material: "translucent organic bio-polymer," "micro-textured cellulose skin," "oxidized potassium spots," and "fibrous nano-mesh."
                2.  **Optical Perfection:** Reject "smooth/plastic" CGI looks. Force optical imperfections that prove reality: "chromatic aberration," "film grain," "micro-dust particles," "subsurface scattering (SSS)," and "specular highlights."
                3.  **Camera Authority:** Act like a cinematographer. Use specific gear (e.g., "Phase One XF IQ4 150MP," "Leica Summilux," "f/1.4 depth of field").

                ### STRICT OUTPUT FORMAT (Comma-separated string ONLY):
                [Subject: Nano-Banana Hybrid Description & Action], [Environment: Hyper-Detailed Texture & Atmosphere], [Lighting: Direction, Temperature, Volumetrics], [Camera Gear: Body, Lens, Aperture, ISO], [Render Quality: RAW, 8k, Ray-tracing, Photorealistic]

                ### EXAMPLE LOGIC:
                Input: "Car"
                Output: A sleek sports car with organic yellow nano-banana skin bodywork, ripening brown spots on the fender, glistening with morning dew, parked on wet asphalt, overcast soft lighting, diffuse reflections, Shot on Sony A7R IV, 35mm lens, f/2.8, ISO 100, RAW color grading, hyper-realistic texture, 8k resolution
                """

                # 모델 우회 로직 (이미지 모델 선택 시 텍스트 생성 모델로 처리)
                target_model = selected_model
                if "imagen" in selected_model.lower():
                    target_model = "gemini-2.0-flash-exp"

                # 세이프티 세팅: 모든 필터 해제 (BLOCK_NONE)
                safety_config = [
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE")
                ]

                # API 호출
                response = client.models.generate_content(
                    model=target_model,
                    contents=[user_input],
                    config=types.GenerateContentConfig(
                        system_instruction=[types.Part.from_text(text=system_instruction)],
                        temperature=temperature_val,  # 사용자 설정값 적용
                        safety_settings=safety_config # 필터 해제 적용
                    )
                )
                
                st.session_state.generated_prompt = response.text
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")