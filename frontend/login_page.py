"""Standalone e-commerce login page."""

from __future__ import annotations

import streamlit as st

from supabase_auth import login_user, register_user, reset_password


def render_login_page() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Jost:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #0a0a0a;
    background-image:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(180,145,90,0.12) 0%, transparent 70%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23b4915a' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    min-height: 100vh;
    font-family: 'Jost', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding: 2rem 1rem 3rem 1rem !important; max-width: 480px !important; }

.brand-header { text-align: center; padding: 3rem 0 2.5rem; position: relative; }
.brand-wordmark { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; font-weight: 300; letter-spacing: 0.25em; color: #e8d5b0; display: block; line-height: 1; text-transform: uppercase; }
.brand-sub { font-family: 'Jost', sans-serif; font-size: 0.65rem; letter-spacing: 0.4em; color: #b4915a; text-transform: uppercase; display: block; margin-top: 0.5rem; font-weight: 400; }
.brand-ornament { display: flex; align-items: center; justify-content: center; gap: 0.75rem; margin-top: 1.2rem; }
.brand-ornament span { display: block; height: 1px; width: 60px; background: linear-gradient(90deg, transparent, #b4915a88, transparent); }
.brand-ornament .diamond { color: #b4915a; font-size: 0.5rem; width: auto; height: auto; background: none; }
.auth-card { background: linear-gradient(145deg, #141414, #111111); border: 1px solid #2a2a2a; border-radius: 2px; padding: 2.5rem 2.5rem 2rem; box-shadow: 0 0 0 1px rgba(180,145,90,0.08), 0 32px 64px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.03); position: relative; overflow: hidden; }
.auth-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, #b4915a55, transparent); }
.card-title { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 400; color: #e8d5b0; letter-spacing: 0.05em; margin-bottom: 0.2rem; text-align: center; }
.card-subtitle { font-size: 0.75rem; color: #666; letter-spacing: 0.12em; text-align: center; text-transform: uppercase; margin-bottom: 2rem; font-weight: 300; }
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #1e1e1e !important; gap: 0 !important; padding: 0 !important; margin-bottom: 1.5rem !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border: none !important; color: #555 !important; font-family: 'Jost', sans-serif !important; font-size: 0.72rem !important; font-weight: 500 !important; letter-spacing: 0.2em !important; text-transform: uppercase !important; padding: 0.75rem 1.5rem !important; flex: 1 !important; text-align: center !important; transition: color 0.2s !important; }
.stTabs [aria-selected="true"] { color: #b4915a !important; border-bottom: 1px solid #b4915a !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }
.stTextInput > label, .stPasswordInput > label { font-family: 'Jost', sans-serif !important; font-size: 0.68rem !important; font-weight: 500 !important; letter-spacing: 0.18em !important; text-transform: uppercase !important; color: #888 !important; margin-bottom: 0.4rem !important; }
.stTextInput > div > div > input, .stPasswordInput > div > div > input { background: #0d0d0d !important; border: 1px solid #222 !important; border-radius: 1px !important; color: #e8d5b0 !important; font-family: 'Jost', sans-serif !important; font-size: 0.9rem !important; font-weight: 300 !important; letter-spacing: 0.05em !important; padding: 0.75rem 1rem !important; transition: border-color 0.2s !important; caret-color: #b4915a !important; }
.stTextInput > div > div > input:focus, .stPasswordInput > div > div > input:focus { border-color: #b4915a55 !important; box-shadow: 0 0 0 3px rgba(180,145,90,0.08) !important; outline: none !important; }
.stTextInput > div > div > input::placeholder, .stPasswordInput > div > div > input::placeholder { color: #333 !important; }
.stCheckbox label { font-family: 'Jost', sans-serif !important; font-size: 0.78rem !important; color: #666 !important; letter-spacing: 0.05em !important; }
.stCheckbox [data-baseweb="checkbox"] [data-checked="true"] { background: #b4915a !important; border-color: #b4915a !important; }
.stButton > button { background: linear-gradient(135deg, #b4915a, #c9a96e, #b4915a) !important; background-size: 200% 100% !important; border: none !important; border-radius: 1px !important; color: #0a0a0a !important; font-family: 'Jost', sans-serif !important; font-size: 0.72rem !important; font-weight: 600 !important; letter-spacing: 0.25em !important; text-transform: uppercase !important; padding: 0.85rem 2rem !important; width: 100% !important; cursor: pointer !important; transition: all 0.3s ease !important; margin-top: 0.75rem !important; box-shadow: 0 4px 20px rgba(180,145,90,0.25) !important; }
.stButton > button:hover { background-position: right center !important; box-shadow: 0 6px 28px rgba(180,145,90,0.4) !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }
.stAlert { border-radius: 1px !important; font-family: 'Jost', sans-serif !important; font-size: 0.82rem !important; border-left: 2px solid !important; }
.stSuccess { background: rgba(180,145,90,0.08) !important; border-left-color: #b4915a !important; color: #c9a96e !important; }
.stError { background: rgba(200,60,60,0.08) !important; border-left-color: #c83c3c !important; color: #e07070 !important; }
.stInfo { background: rgba(100,140,200,0.06) !important; border-left-color: #4a7fc1 !important; color: #7aaae8 !important; }
hr { border: none !important; border-top: 1px solid #1a1a1a !important; margin: 1.5rem 0 !important; }
.footer-links { text-align: center; margin-top: 1.5rem; font-size: 0.72rem; color: #444; letter-spacing: 0.08em; }
.footer-links a { color: #b4915a88; text-decoration: none; margin: 0 0.75rem; transition: color 0.2s; }
.footer-links a:hover { color: #b4915a; }
.page-footer { text-align: center; margin-top: 2.5rem; font-size: 0.65rem; color: #2a2a2a; letter-spacing: 0.15em; text-transform: uppercase; }
.or-divider { display: flex; align-items: center; gap: 1rem; margin: 1.2rem 0; color: #333; font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; }
.or-divider::before, .or-divider::after { content: ''; flex: 1; height: 1px; background: #1e1e1e; }
.welcome-banner { background: linear-gradient(135deg, #141414, #111); border: 1px solid #2a2a2a; border-top: 2px solid #b4915a; border-radius: 2px; padding: 2.5rem; text-align: center; box-shadow: 0 20px 48px rgba(0,0,0,0.5); }
.welcome-title { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 300; color: #e8d5b0; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
.welcome-email { font-size: 0.8rem; color: #b4915a; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 1.5rem; }
.welcome-badge { display: inline-block; background: rgba(180,145,90,0.1); border: 1px solid rgba(180,145,90,0.3); color: #b4915a; font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; padding: 0.35rem 0.9rem; border-radius: 0; margin-bottom: 1.5rem; }
.stForm, [data-testid="stForm"] { border: none !important; padding: 0 !important; }
</style>
""",
        unsafe_allow_html=True,
    )

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.authenticated:
        user = st.session_state.user or {}
        name = user.get("name", "Shopper")

        st.markdown(
            f"""
    <div class="brand-header">
        <span class="brand-wordmark">Store</span>
        <span class="brand-sub">Ecommerce Login</span>
        <div class="brand-ornament">
            <span></span><span class="diamond">✦</span><span></span>
        </div>
    </div>
    """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
    <div class="welcome-banner">
        <div class="welcome-title">Welcome back, {name}</div>
        <div class="welcome-email">{user.get("email", "")}</div>
        <div class="welcome-badge">✦ Authenticated</div>
        <p style="color:#555; font-size:0.8rem; letter-spacing:0.05em; line-height:1.6;">
            You are now signed in to your shopper account.<br>
            Browse products, manage orders, and track your activity.
        </p>
    </div>
    """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("BROWSE COLLECTIONS"):
                st.info("→ Redirect to /shop")
        with col2:
            if st.button("MY ACCOUNT"):
                st.info("→ Redirect to /account")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("SIGN OUT"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

        st.markdown('<div class="page-footer">© 2025 Ecommerce Store · All rights reserved</div>', unsafe_allow_html=True)
        return

    st.markdown(
        """
<div class="brand-header">
    <span class="brand-wordmark">Store</span>
    <span class="brand-sub">Ecommerce Login · Est. 2025</span>
    <div class="brand-ornament">
        <span></span><span class="diamond">✦</span><span></span>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    tab_login, tab_register, tab_reset = st.tabs(["Sign In", "Create Account", "Reset Password"])

    with tab_login:
        st.markdown('<div class="card-subtitle">Sign in to continue shopping</div>', unsafe_allow_html=True)

        email_login = st.text_input("Email Address", key="login_email", placeholder="you@example.com")
        password_login = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••••")

        col_remember, col_forgot = st.columns([1, 1])
        with col_remember:
            st.checkbox("Remember me", key="remember")
        with col_forgot:
            st.markdown('<div style="text-align:right; margin-top:0.5rem;"><a href="#" style="font-size:0.72rem; color:#b4915a55; text-decoration:none; letter-spacing:0.05em;">Forgot password?</a></div>', unsafe_allow_html=True)

        if st.button("SIGN IN  →", key="btn_login"):
            if not email_login or not password_login:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Authenticating..."):
                    result = login_user(email_login, password_login)

                if result["success"]:
                    st.session_state.authenticated = True
                    st.session_state.user = result["user"]
                    st.success(f"Welcome back, {result['user']['name']}!")
                    st.rerun()
                else:
                    st.error(result.get("error", "Login failed. Please try again."))

        st.markdown('<div class="or-divider">or continue with</div>', unsafe_allow_html=True)

        col_g, col_a = st.columns(2)
        with col_g:
            st.markdown("""
        <button style="width:100%; background:#111; border:1px solid #222; color:#888;
            font-family:'Jost',sans-serif; font-size:0.72rem; letter-spacing:0.1em;
            padding:0.65rem; cursor:pointer; border-radius:1px;">
            G  Google
        </button>""", unsafe_allow_html=True)
        with col_a:
            st.markdown("""
        <button style="width:100%; background:#111; border:1px solid #222; color:#888;
            font-family:'Jost',sans-serif; font-size:0.72rem; letter-spacing:0.1em;
            padding:0.65rem; cursor:pointer; border-radius:1px;">
            ⌘  Apple
        </button>""", unsafe_allow_html=True)

        st.markdown('<div class="footer-links"><a href="#">Privacy Policy</a><a href="#">Terms of Service</a></div>', unsafe_allow_html=True)

    with tab_register:
        st.markdown('<div class="card-subtitle">Create your shopper account</div>', unsafe_allow_html=True)

        full_name = st.text_input("Full Name", key="reg_name", placeholder="Alexandra Chen")
        email_reg = st.text_input("Email Address", key="reg_email", placeholder="you@example.com")
        password_reg = st.text_input("Password", type="password", key="reg_pass", placeholder="Min. 6 characters")
        password_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")
        agree = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="reg_agree")

        if st.button("CREATE ACCOUNT  →", key="btn_register"):
            if not all([full_name, email_reg, password_reg, password_confirm]):
                st.error("Please fill in all fields.")
            elif password_reg != password_confirm:
                st.error("Passwords do not match.")
            elif len(password_reg) < 6:
                st.error("Password must be at least 6 characters.")
            elif not agree:
                st.error("Please accept the Terms of Service to continue.")
            else:
                with st.spinner("Creating your account..."):
                    result = register_user(email_reg, password_reg, full_name)

                if result["success"]:
                    st.success(result.get("message", "Account created successfully!"))
                else:
                    st.error(result.get("error", "Registration failed."))

    with tab_reset:
        st.markdown('<div class="card-subtitle">Reset your password</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; color:#555; line-height:1.6; margin-bottom:1.2rem; letter-spacing:0.03em;">Enter your email address and we\'ll send you a secure link to reset your password.</p>', unsafe_allow_html=True)

        email_reset = st.text_input("Email Address", key="reset_email", placeholder="you@example.com")

        if st.button("SEND RESET LINK  →", key="btn_reset"):
            if not email_reset:
                st.error("Please enter your email address.")
            else:
                with st.spinner("Sending reset link..."):
                    result = reset_password(email_reset)

                if result["success"]:
                    st.success(result.get("message", "Reset link sent!"))
                else:
                    st.error(result.get("error", "Failed to send reset link."))

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-footer">© 2025 Ecommerce Store · Secured by Supabase</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    render_login_page()
