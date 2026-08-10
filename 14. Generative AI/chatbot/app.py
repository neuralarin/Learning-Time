import os
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

st.set_page_config(page_title="AURA", page_icon="◈", layout="centered")

# ----------------------------------------------------------------------------
# MODE DEFINITIONS  (unchanged logic from the original script)
# ----------------------------------------------------------------------------
MODES = {
    "funny": {
        "label": "FUNNY",
        "sub": "Comic Reasoning Core",
        "prompt": "You are a funny AI agent. You crack concepts in joke",
        "accent": "#ffb454",
        "accent_dim": "#7a5a20",
    },
    "emotional": {
        "label": "EMOTIONAL",
        "sub": "Empathic Response Core",
        "prompt": "You are a emotional AI agent. You gets emotional while explaining concepts",
        "accent": "#c77dff",
        "accent_dim": "#5a3b7a",
    },
    "angry": {
        "label": "ANGRY",
        "sub": "Aggressive Override Core",
        "prompt": "You are a agressive AI agent. You respond aggresively and impatiently",
        "accent": "#ff5f6d",
        "accent_dim": "#7a2a2f",
    },
}

DEFAULT_ACCENT = "#37e6ff"
DEFAULT_ACCENT_DIM = "#0f8fa8"

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "key"          # key -> mode -> chat
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []          # list of langchain message objects
if "model" not in st.session_state:
    st.session_state.model = None
if "auth_error" not in st.session_state:
    st.session_state.auth_error = ""
if "thinking" not in st.session_state:
    st.session_state.thinking = False

current_accent = DEFAULT_ACCENT
current_accent_dim = DEFAULT_ACCENT_DIM
if st.session_state.mode:
    current_accent = MODES[st.session_state.mode]["accent"]
    current_accent_dim = MODES[st.session_state.mode]["accent_dim"]

# ----------------------------------------------------------------------------
# CSS / VISUAL SYSTEM
# ----------------------------------------------------------------------------
def inject_css(accent: str, accent_dim: str) -> None:
    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&display=swap');

    :root {{
        --accent: {accent};
        --accent-dim: {accent_dim};
        --bg: #03060b;
        --bg-panel: rgba(8, 18, 28, 0.72);
        --bg-panel-solid: #060d15;
        --text: #d8f4ff;
        --text-dim: #5f7f96;
        --border: color-mix(in srgb, var(--accent) 45%, transparent);
    }}

    html, body, [class*="css"] {{
        font-family: 'Share Tech Mono', monospace;
    }}

    .stApp {{
        background:
            radial-gradient(ellipse 80% 60% at 50% -10%, color-mix(in srgb, var(--accent) 14%, transparent), transparent 60%),
            radial-gradient(ellipse 60% 50% at 100% 100%, color-mix(in srgb, var(--accent) 8%, transparent), transparent 60%),
            var(--bg);
        color: var(--text);
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    .block-container {{ padding-top: 2.2rem; max-width: 760px; }}

    /* ---------- animated backdrop grid ---------- */
    .aura-grid {{
        position: fixed; inset: 0; z-index: -1; pointer-events: none;
        background-image:
            linear-gradient(color-mix(in srgb, var(--accent) 6%, transparent) 1px, transparent 1px),
            linear-gradient(90deg, color-mix(in srgb, var(--accent) 6%, transparent) 1px, transparent 1px);
        background-size: 42px 42px;
        mask-image: radial-gradient(ellipse 70% 60% at 50% 30%, black, transparent 75%);
        animation: gridDrift 40s linear infinite;
    }}
    @keyframes gridDrift {{
        0% {{ background-position: 0 0, 0 0; }}
        100% {{ background-position: 84px 84px, 84px 84px; }}
    }}

    /* ---------- header ---------- */
    .aura-header {{
        text-align: center; margin-bottom: 0.6rem;
    }}
    .aura-title {{
        font-family: 'Orbitron', sans-serif; font-weight: 900;
        font-size: 2.6rem; letter-spacing: 0.35em; margin: 0;
        color: var(--text);
        text-shadow: 0 0 18px color-mix(in srgb, var(--accent) 80%, transparent),
                     0 0 46px color-mix(in srgb, var(--accent) 40%, transparent);
    }}
    .aura-subtitle {{
        font-size: 0.72rem; letter-spacing: 0.42em; color: var(--accent);
        text-transform: uppercase; margin-top: 0.35rem; opacity: 0.85;
    }}
    .aura-rule {{
        height: 1px; margin: 1.1rem auto 1.6rem auto; width: 100%;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        opacity: 0.6;
    }}

    /* ---------- reactor core ---------- */
    .core-wrap {{ display: flex; justify-content: center; margin: 0.4rem 0 1.4rem 0; }}
    .core {{
        position: relative; width: 132px; height: 132px;
    }}
    .core::before, .core::after {{
        content: ""; position: absolute; inset: 0; border-radius: 50%;
        border: 1px solid var(--border);
    }}
    .core::before {{
        animation: spin 7s linear infinite;
        border-top-color: var(--accent); border-right-color: var(--accent);
    }}
    .core::after {{
        inset: 14px; animation: spin 5s linear infinite reverse;
        border-bottom-color: var(--accent); border-left-color: var(--accent);
    }}
    .core-inner {{
        position: absolute; inset: 34px; border-radius: 50%;
        background: radial-gradient(circle at 40% 35%, color-mix(in srgb, var(--accent) 90%, white 10%), var(--accent-dim) 70%);
        box-shadow: 0 0 24px 6px color-mix(in srgb, var(--accent) 65%, transparent),
                    inset 0 0 14px rgba(0,0,0,0.4);
        animation: corePulse 2.4s ease-in-out infinite;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes corePulse {{
        0%, 100% {{ transform: scale(1); filter: brightness(1); }}
        50% {{ transform: scale(1.08); filter: brightness(1.25); }}
    }}
    .core.thinking::before {{ animation-duration: 1.4s; }}
    .core.thinking::after {{ animation-duration: 0.9s; }}
    .core.thinking .core-inner {{ animation-duration: 0.7s; }}

    /* ---------- HUD panel ---------- */
    .hud-panel {{
        position: relative; background: var(--bg-panel);
        border: 1px solid var(--border); border-radius: 4px;
        padding: 1.8rem 1.9rem; backdrop-filter: blur(6px);
        box-shadow: 0 0 30px rgba(0,0,0,0.35), inset 0 0 30px rgba(0,0,0,0.25);
        margin-bottom: 1.2rem; overflow: hidden;
    }}
    .hud-panel::before {{
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        animation: scan 3.2s linear infinite;
    }}
    @keyframes scan {{
        0% {{ transform: translateY(0); opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ transform: translateY(220px); opacity: 0; }}
    }}
    .corner {{ position: absolute; width: 14px; height: 14px; border-color: var(--accent); opacity: 0.8; }}
    .corner.tl {{ top: 6px; left: 6px; border-top: 2px solid; border-left: 2px solid; }}
    .corner.tr {{ top: 6px; right: 6px; border-top: 2px solid; border-right: 2px solid; }}
    .corner.bl {{ bottom: 6px; left: 6px; border-bottom: 2px solid; border-left: 2px solid; }}
    .corner.br {{ bottom: 6px; right: 6px; border-bottom: 2px solid; border-right: 2px solid; }}

    .hud-label {{
        font-size: 0.68rem; letter-spacing: 0.28em; color: var(--accent);
        text-transform: uppercase; margin-bottom: 0.6rem; opacity: 0.9;
    }}
    .hud-caption {{ color: var(--text-dim); font-size: 0.82rem; line-height: 1.55; }}

    .status-row {{
        display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem;
        font-size: 0.72rem; color: var(--text-dim); letter-spacing: 0.08em;
    }}
    .status-dot {{
        width: 7px; height: 7px; border-radius: 50%; background: var(--accent);
        box-shadow: 0 0 8px 2px var(--accent);
        animation: blink 1.6s ease-in-out infinite;
    }}
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}

    /* ---------- inputs & buttons ---------- */
    .stTextInput input, .stTextInput > div > div {{
        background: rgba(0,0,0,0.35) !important; color: var(--text) !important;
        border: 1px solid var(--border) !important; border-radius: 3px !important;
        font-family: 'Share Tech Mono', monospace !important; letter-spacing: 0.03em;
    }}
    .stTextInput input:focus {{
        box-shadow: 0 0 0 1px var(--accent), 0 0 14px color-mix(in srgb, var(--accent) 55%, transparent) !important;
    }}
    label, .stTextInput label p {{ color: var(--text-dim) !important; letter-spacing: 0.08em; font-size: 0.78rem !important; }}

    .stButton > button, .stFormSubmitButton > button {{
        width: 100%; background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 18%, transparent), transparent) !important;
        color: var(--accent) !important; border: 1px solid var(--accent) !important;
        border-radius: 3px !important; font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.18em !important; font-size: 0.78rem !important;
        padding: 0.6rem 0.4rem !important; text-transform: uppercase;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover, .stFormSubmitButton > button:hover {{
        background: var(--accent) !important; color: #04070b !important;
        box-shadow: 0 0 20px color-mix(in srgb, var(--accent) 70%, transparent);
    }}

    /* ---------- mode cards ---------- */
    .mode-name {{ font-family: 'Orbitron', sans-serif; letter-spacing: 0.16em; font-size: 0.95rem; }}
    .mode-sub {{ color: var(--text-dim); font-size: 0.7rem; margin-top: 0.2rem; letter-spacing: 0.04em; }}

    /* ---------- chat ---------- */
    .msg-row {{ display: flex; margin: 0.55rem 0; animation: rise 0.35s ease; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .msg-row.user {{ justify-content: flex-end; }}
    .msg-row.ai {{ justify-content: flex-start; }}
    .bubble {{
        max-width: 78%; padding: 0.65rem 0.95rem; border-radius: 3px;
        font-size: 0.88rem; line-height: 1.5; letter-spacing: 0.01em;
    }}
    .bubble.user {{
        background: color-mix(in srgb, var(--accent) 16%, transparent);
        border: 1px solid var(--border); color: var(--text);
        border-radius: 10px 10px 2px 10px;
    }}
    .bubble.ai {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08); color: var(--text);
        border-radius: 10px 10px 10px 2px;
    }}
    .bubble-tag {{
        display: block; font-size: 0.6rem; letter-spacing: 0.2em; margin-bottom: 0.3rem;
        color: var(--accent); opacity: 0.8; text-transform: uppercase;
    }}

    .typing-dots span {{
        display: inline-block; width: 5px; height: 5px; margin-right: 3px;
        border-radius: 50%; background: var(--accent);
        animation: dotPulse 1.1s infinite ease-in-out;
    }}
    .typing-dots span:nth-child(2) {{ animation-delay: 0.15s; }}
    .typing-dots span:nth-child(3) {{ animation-delay: 0.3s; }}
    @keyframes dotPulse {{ 0%, 80%, 100% {{ opacity: 0.25; transform: scale(0.8); }} 40% {{ opacity: 1; transform: scale(1.1); }} }}

    [data-testid="stChatInput"] {{
        background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
        border-radius: 4px !important;
    }}
    [data-testid="stChatInput"] textarea {{ color: var(--text) !important; font-family: 'Share Tech Mono', monospace !important; }}

    .stAlert {{ background: rgba(255,80,80,0.08) !important; border: 1px solid rgba(255,80,80,0.4) !important; }}
    </style>
    <div class="aura-grid"></div>
    """,
        unsafe_allow_html=True,
    )


def render_header(sub: str) -> None:
    st.markdown(
        f"""
        <div class="aura-header">
            <div class="aura-title">AURA</div>
            <div class="aura-subtitle">{sub}</div>
        </div>
        <div class="aura-rule"></div>
        """,
        unsafe_allow_html=True,
    )


def render_core(thinking: bool = False) -> None:
    cls = "core thinking" if thinking else "core"
    st.markdown(
        f"""
        <div class="core-wrap">
            <div class="{cls}"><div class="core-inner"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_css(current_accent, current_accent_dim)

# ============================================================================
# STAGE 1 — API KEY
# ============================================================================
if st.session_state.stage == "key":
    render_header("Autonomous Uplink &amp; Response Agent")
    render_core()

    st.markdown(
        """
        <div class="hud-panel">
            <div class="corner tl"></div><div class="corner tr"></div>
            <div class="corner bl"></div><div class="corner br"></div>
            <div class="hud-label">// Authentication Required</div>
            <div class="hud-caption">
                AURA is offline. Provide a valid Mistral API key to establish an uplink
                and bring the reasoning core online.
            </div>
            <div class="status-row"><span class="status-dot"></span> AWAITING CREDENTIALS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("key_form", clear_on_submit=False):
        key_input = st.text_input(
            "MISTRAL API KEY",
            type="password",
            placeholder="••••••••••••••••••••••••••••",
            value=st.session_state.api_key,
        )
        submitted = st.form_submit_button("Initialize Uplink")

    if submitted:
        key_input = (key_input or "").strip()
        if not key_input:
            st.session_state.auth_error = "No key detected. Enter a valid API key to proceed."
        else:
            with st.spinner("Verifying credentials..."):
                try:
                    test_model = ChatMistralAI(
                        model="mistral-small-2603",
                        temperature=0.9,
                        max_tokens=40,
                        mistral_api_key=key_input,
                    )
                    test_model.invoke([HumanMessage(content="ping")])
                    st.session_state.api_key = key_input
                    st.session_state.model = test_model
                    st.session_state.auth_error = ""
                    st.session_state.stage = "mode"
                    st.rerun()
                except Exception as exc:  # noqa: BLE001
                    st.session_state.auth_error = f"Authentication failed: {exc}"

    if st.session_state.auth_error:
        st.error(st.session_state.auth_error)

# ============================================================================
# STAGE 2 — MODE SELECTION
# ============================================================================
elif st.session_state.stage == "mode":
    render_header("Uplink Established — Select Personality Core")
    render_core()

    st.markdown(
        """
        <div class="hud-panel">
            <div class="corner tl"></div><div class="corner tr"></div>
            <div class="corner bl"></div><div class="corner br"></div>
            <div class="hud-label">// Core Calibration</div>
            <div class="hud-caption">Choose the response matrix AURA will operate under for this session.</div>
            <div class="status-row"><span class="status-dot"></span> UPLINK ACTIVE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for col, key in zip(cols, MODES.keys()):
        m = MODES[key]
        with col:
            st.markdown(
                f"""
                <div style="text-align:center; margin-bottom:0.4rem;">
                    <div class="mode-name" style="color:{m['accent']};">{m['label']}</div>
                    <div class="mode-sub">{m['sub']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Select", key=f"mode_{key}"):
                st.session_state.mode = key
                st.session_state.messages = [SystemMessage(content=m["prompt"])]
                st.session_state.stage = "chat"
                st.rerun()

# ============================================================================
# STAGE 3 — CHAT
# ============================================================================
elif st.session_state.stage == "chat":
    mode_info = MODES[st.session_state.mode]
    render_header(f"Core Online — {mode_info['label']} Mode")
    render_core(thinking=st.session_state.thinking)

    st.markdown(
        f"""
        <div class="status-row" style="justify-content:center; margin-bottom:0.8rem;">
            <span class="status-dot"></span> {mode_info['sub'].upper()} ENGAGED
        </div>
        """,
        unsafe_allow_html=True,
    )

    for msg in st.session_state.messages:
        if isinstance(msg, SystemMessage):
            continue
        role = "user" if isinstance(msg, HumanMessage) else "ai"
        tag = "You" if role == "user" else "AURA"
        st.markdown(
            f"""
            <div class="msg-row {role}">
                <div class="bubble {role}">
                    <span class="bubble-tag">{tag}</span>{msg.content}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.thinking:
        st.markdown(
            """
            <div class="msg-row ai">
                <div class="bubble ai">
                    <span class="bubble-tag">AURA</span>
                    <span class="typing-dots"><span></span><span></span><span></span></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    user_prompt = st.chat_input("Transmit a message to AURA...")
    if user_prompt:
        st.session_state.messages.append(HumanMessage(content=user_prompt))
        st.session_state.thinking = True
        st.rerun()

    if st.session_state.thinking and st.session_state.messages and isinstance(
        st.session_state.messages[-1], HumanMessage
    ):
        response = st.session_state.model.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        st.session_state.thinking = False
        st.rerun()