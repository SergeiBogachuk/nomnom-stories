import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Manrope:wght@400;500;600;700;800&display=swap');

        :root {
            --bg-deep: #0f1727;
            --bg-mid: #1b2640;
            --surface: rgba(14, 24, 42, 0.78);
            --surface-strong: rgba(10, 18, 33, 0.88);
            --surface-soft: rgba(255, 248, 236, 0.08);
            --line: rgba(255, 222, 173, 0.14);
            --line-strong: rgba(255, 203, 129, 0.28);
            --text-main: #fff9ef;
            --text-soft: #eadfce;
            --text-muted: #cdbda9;
            --accent: #f4a261;
            --accent-2: #e76f51;
            --accent-3: #8ab17d;
            --paper: #fffaf1;
            --paper-text: #35271c;
            --shadow-lg: 0 24px 70px rgba(6, 10, 18, 0.42);
            --shadow-md: 0 14px 36px rgba(6, 10, 18, 0.24);
            --radius-xl: 28px;
            --radius-lg: 22px;
            --radius-md: 18px;
            --radius-sm: 14px;
        }

        html, body, [class*="css"] {
            font-family: "Manrope", sans-serif;
        }

        .stApp {
            color: var(--text-main) !important;
            background:
                radial-gradient(circle at 15% 18%, rgba(244, 162, 97, 0.16), transparent 28%),
                radial-gradient(circle at 82% 12%, rgba(138, 177, 125, 0.14), transparent 24%),
                radial-gradient(circle at 50% 0%, rgba(255, 255, 255, 0.06), transparent 26%),
                linear-gradient(180deg, #15233b 0%, #101928 48%, #0c1320 100%) !important;
            position: relative;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                repeating-linear-gradient(
                    135deg,
                    rgba(255, 255, 255, 0.02) 0,
                    rgba(255, 255, 255, 0.02) 2px,
                    transparent 2px,
                    transparent 18px
                );
            opacity: 0.22;
        }

        header[data-testid="stHeader"] {
            background: rgba(12, 19, 32, 0.16) !important;
            backdrop-filter: blur(8px) !important;
        }

        [data-testid="collapsedControl"] {
            position: fixed !important;
            top: 14px !important;
            left: 14px !important;
            z-index: 999999 !important;
            background: rgba(15, 23, 39, 0.92) !important;
            border: 1px solid var(--line-strong) !important;
            border-radius: 14px !important;
            box-shadow: var(--shadow-md) !important;
            padding: 4px !important;
        }

        [data-testid="collapsedControl"] svg,
        [data-testid="collapsedControl"] path {
            color: var(--text-main) !important;
            fill: var(--text-main) !important;
            stroke: var(--text-main) !important;
        }

        [data-testid="block-container"] {
            max-width: 900px !important;
            margin-top: 22px !important;
            margin-bottom: 44px !important;
            padding: 2.4rem 2.15rem 2.2rem 2.15rem !important;
            background:
                linear-gradient(180deg, rgba(18, 29, 49, 0.86), rgba(11, 19, 33, 0.8)) !important;
            border: 1px solid var(--line) !important;
            border-radius: var(--radius-xl) !important;
            box-shadow: var(--shadow-lg) !important;
            backdrop-filter: blur(16px) !important;
            animation: riseIn 0.55s ease-out both;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(11, 19, 33, 0.96), rgba(14, 24, 42, 0.98)) !important;
            border-right: 1px solid rgba(255, 203, 129, 0.14) !important;
            box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.04) !important;
        }

        [data-testid="stSidebar"] .stAlert {
            border-radius: var(--radius-md) !important;
            border: 1px solid rgba(138, 177, 125, 0.26) !important;
            background: rgba(138, 177, 125, 0.14) !important;
            color: var(--text-main) !important;
        }

        h1, h2, h3 {
            color: var(--text-main) !important;
            font-family: "Fraunces", serif !important;
            letter-spacing: -0.02em !important;
        }

        .hero-title {
            text-align: center;
            font-family: "Fraunces", serif;
            font-size: 3.1rem;
            font-weight: 700;
            line-height: 1.02;
            margin-bottom: 0.55rem;
            color: var(--text-main);
            text-wrap: balance;
        }

        .story-title {
            font-size: 2.5rem;
        }

        .hero-subtitle {
            text-align: center;
            font-size: 1.02rem;
            line-height: 1.7;
            color: var(--text-soft);
            max-width: 640px;
            margin: 0 auto 1.4rem auto;
        }

        .hero-badge {
            width: fit-content;
            margin: 0 auto 14px auto;
            padding: 9px 16px;
            border-radius: 999px;
            border: 1px solid var(--line-strong);
            background: linear-gradient(135deg, rgba(244, 162, 97, 0.14), rgba(255, 248, 236, 0.08));
            color: #fff4e8;
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            box-shadow: 0 10px 24px rgba(14, 24, 42, 0.16);
            animation: glowPulse 3.2s ease-in-out infinite;
        }

        .sidebar-brand {
            font-family: "Fraunces", serif;
            font-size: 1.32rem;
            font-weight: 700;
            color: var(--text-main);
            margin-top: 8px;
            margin-bottom: 6px;
        }

        .sidebar-subbrand {
            font-size: 0.94rem;
            line-height: 1.6;
            color: var(--text-soft);
            margin-bottom: 18px;
        }

        .section-label {
            margin-top: 10px;
            margin-bottom: 8px;
            font-size: 0.98rem;
            font-weight: 800;
            letter-spacing: 0.01em;
            color: #fff4e8 !important;
        }

        .soft-info-chip {
            width: fit-content;
            margin: 12px auto 14px auto;
            padding: 12px 16px;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(244, 162, 97, 0.18), rgba(138, 177, 125, 0.18));
            border: 1px solid rgba(255, 203, 129, 0.24);
            color: #fff7ef;
            font-weight: 700;
            box-shadow: 0 14px 28px rgba(6, 10, 18, 0.16);
            text-align: center;
        }

        p, label, span, div {
            color: var(--text-main);
        }

        .stCaptionContainer, .stCaptionContainer p {
            color: var(--text-muted) !important;
            line-height: 1.6 !important;
        }

        div[data-testid="stForm"] {
            border: 1px solid var(--line) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1rem !important;
            background: rgba(255, 248, 236, 0.05) !important;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        .stTextArea textarea {
            background: rgba(255, 248, 236, 0.08) !important;
            border: 1px solid rgba(255, 203, 129, 0.18) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-main) !important;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.04),
                0 10px 28px rgba(6, 10, 18, 0.12) !important;
        }

        .stTextInput input,
        .stTextArea textarea {
            color: var(--text-main) !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: rgba(234, 223, 206, 0.64) !important;
        }

        .stTextArea textarea {
            min-height: 150px !important;
        }

        div[data-baseweb="tag"] {
            background: linear-gradient(135deg, rgba(244, 162, 97, 0.95), rgba(231, 111, 81, 0.95)) !important;
            border-radius: 999px !important;
            border: none !important;
            color: white !important;
            padding-left: 8px !important;
            padding-right: 8px !important;
            font-weight: 700 !important;
        }

        div[data-baseweb="tag"] span {
            color: white !important;
        }

        .stCheckbox {
            background: rgba(255, 248, 236, 0.05) !important;
            padding: 14px 16px !important;
            border-radius: var(--radius-md) !important;
            border: 1px solid rgba(255, 203, 129, 0.18) !important;
            box-shadow: 0 10px 24px rgba(6, 10, 18, 0.12) !important;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .stCheckbox:hover {
            transform: translateY(-1px);
            border-color: rgba(255, 203, 129, 0.34) !important;
        }

        div.stButton > button {
            border-radius: var(--radius-md) !important;
            min-height: 50px !important;
            font-weight: 800 !important;
            border: 1px solid rgba(255, 203, 129, 0.18) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
        }

        div.stButton > button[kind="primary"],
        button[kind="primaryFormSubmit"] {
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 16px 34px rgba(231, 111, 81, 0.28) !important;
        }

        div.stButton > button[kind="primary"]:hover,
        button[kind="primaryFormSubmit"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 20px 38px rgba(231, 111, 81, 0.34) !important;
        }

        div.stButton > button[kind="secondary"] {
            background: rgba(255, 248, 236, 0.06) !important;
            color: var(--text-main) !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            border-color: rgba(255, 203, 129, 0.34) !important;
            background: rgba(255, 248, 236, 0.1) !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid rgba(255, 203, 129, 0.14) !important;
            border-radius: var(--radius-md) !important;
            background: rgba(255, 248, 236, 0.04) !important;
            overflow: hidden !important;
        }

        [data-testid="stExpander"] summary {
            background: rgba(255, 248, 236, 0.04) !important;
            border-radius: var(--radius-sm) !important;
            padding-top: 0.25rem !important;
            padding-bottom: 0.25rem !important;
        }

        [data-testid="stExpander"] summary:hover {
            background: rgba(255, 248, 236, 0.08) !important;
        }

        [data-testid="stSidebar"] [data-testid="stExpander"] .stButton button,
        [data-testid="stExpander"] .stButton button {
            background: rgba(255, 248, 236, 0.06) !important;
            color: var(--text-main) !important;
            border: 1px solid rgba(255, 203, 129, 0.16) !important;
            border-radius: var(--radius-sm) !important;
            box-shadow: none !important;
        }

        [data-testid="stSidebar"] [data-testid="stExpander"] .stButton button:hover,
        [data-testid="stExpander"] .stButton button:hover {
            background: rgba(255, 248, 236, 0.1) !important;
            border-color: rgba(255, 203, 129, 0.28) !important;
        }

        [data-testid="stSidebar"] [data-testid="stExpander"] .stButton button p,
        [data-testid="stSidebar"] [data-testid="stExpander"] .stButton button span,
        [data-testid="stSidebar"] [data-testid="stExpander"] .stButton button div {
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            opacity: 1 !important;
        }

        [data-testid="stSidebar"] [data-testid="stExpander"] div[data-testid="column"]:last-child .stButton button {
            min-width: 44px !important;
            width: 44px !important;
            padding: 0 !important;
        }

        .stInfo, .stSuccess, .stWarning, .stError {
            border-radius: var(--radius-md) !important;
            border: 1px solid rgba(255, 203, 129, 0.16) !important;
        }

        .stInfo {
            background: rgba(244, 162, 97, 0.1) !important;
        }

        .story-shell {
            margin-top: 18px;
        }

        .story-output {
            background: linear-gradient(180deg, var(--paper) 0%, #fdf3e7 100%) !important;
            color: var(--paper-text) !important;
            padding: 32px !important;
            border-radius: 26px !important;
            font-size: 1.08rem !important;
            line-height: 1.92 !important;
            max-width: 920px !important;
            margin: 20px auto 0 auto !important;
            white-space: pre-wrap !important;
            box-shadow: 0 18px 40px rgba(9, 13, 22, 0.18) !important;
            border: 1px solid rgba(244, 162, 97, 0.12) !important;
        }

        .story-output,
        .story-output p,
        .story-output span,
        .story-output div,
        .story-output strong,
        .story-output em,
        .story-output li,
        .story-output h1,
        .story-output h2,
        .story-output h3,
        .story-output h4,
        .story-output h5,
        .story-output h6 {
            color: var(--paper-text) !important;
            font-weight: 500 !important;
        }

        [data-testid="stImage"] img {
            border-radius: 24px !important;
            box-shadow: 0 20px 42px rgba(9, 13, 22, 0.24) !important;
        }

        audio {
            width: 100% !important;
            margin-top: 12px !important;
            margin-bottom: 16px !important;
            border-radius: 16px !important;
        }

        hr {
            border-color: rgba(255, 203, 129, 0.12) !important;
        }

        @keyframes riseIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes glowPulse {
            0%, 100% {
                box-shadow: 0 10px 24px rgba(14, 24, 42, 0.16);
            }
            50% {
                box-shadow: 0 14px 30px rgba(244, 162, 97, 0.18);
            }
        }

        @media (max-width: 768px) {
            [data-testid="block-container"] {
                padding: 1.35rem 1rem 1.3rem 1rem !important;
                border-radius: 24px !important;
                margin-top: 10px !important;
            }

            .hero-title {
                font-size: 2.35rem !important;
            }

            .story-title {
                font-size: 2.05rem !important;
            }

            .hero-subtitle {
                font-size: 0.96rem !important;
            }

            .story-output {
                padding: 22px !important;
                font-size: 1rem !important;
                line-height: 1.82 !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
