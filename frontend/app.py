import streamlit as st

st.set_page_config(
    page_title="Responsive Navbar",
    page_icon="🌐",
    layout="wide",
)

st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">

    <style>
    .navbar-wrap {
      width: 100%;
      max-width: none;
      margin: 1.25rem 0;
      padding: 0 18px;
      overflow: visible;
    }

    .navbar-custom {
      width: 100%;
      max-width: 100%;
      background: linear-gradient(135deg, #0d6efd 0%, #6610f2 100%);
      border-radius: 22px;
      min-height: 70px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 22px;
      box-shadow: 0 24px 68px rgba(15, 23, 42, 0.18);
      overflow: hidden;
    }

    .navbar-custom .brand-text {
      color: #ffffff;
      font-size: 1.18rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-decoration: none;
    }

    .navbar-custom .brand-text strong {
      color: #f8fafc;
    }

    .navbar-custom .search-group {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1 1 320px;
      max-width: 420px;
      margin: 0 16px;
    }

    .navbar-custom .search-group input {
      flex: 1;
      min-height: 42px;
      border: 1px solid rgba(255, 255, 255, 0.28);
      background: rgba(255, 255, 255, 0.12);
      color: #ffffff;
      padding: 0 14px;
      border-radius: 14px;
      outline: none;
      transition: border-color 0.2s ease, background 0.2s ease;
    }

    .navbar-custom .search-group input::placeholder {
      color: rgba(255, 255, 255, 0.72);
    }

    .navbar-custom .search-group input:focus {
      border-color: rgba(255, 255, 255, 0.84);
      background: rgba(255, 255, 255, 0.18);
    }

    .navbar-custom .search-group button {
      min-width: 88px;
      border: none;
      background: rgba(255, 255, 255, 0.22);
      color: #ffffff;
      font-weight: 600;
      border-radius: 14px;
      padding: 10px 14px;
      cursor: pointer;
      transition: background 0.2s ease, transform 0.2s ease;
    }

    .navbar-custom .search-group button:hover {
      background: rgba(255, 255, 255, 0.32);
      transform: translateY(-1px);
    }

    .navbar-custom .nav-links {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    /* Profile (right-most) */
    .profile {
      position: relative;
      display: flex;
      align-items: center;
      margin-left: 8px;
    }

    .profile-button {
      width: 44px;
      height: 44px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: rgba(255,255,255,0.14);
      color: #fff;
      border: 1px solid rgba(255,255,255,0.18);
      cursor: pointer;
      transition: transform 0.12s ease, background 0.12s ease;
    }

    .profile-button:hover { transform: translateY(-2px); background: rgba(255,255,255,0.22); }

    .profile-dropdown {
      position: absolute;
      right: 0;
      top: calc(100% + 8px);
      min-width: 220px;
      background: #ffffff;
      color: #111827;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(17,24,39,0.12);
      padding: 8px;
      display: none;
      z-index: 9999;
    }

    .profile.open .profile-dropdown { display: block; }

    .profile-dropdown .user-info { padding: 8px 10px; }
    .profile-dropdown .user-info .name { font-weight: 700; }
    .profile-dropdown .user-info .email { font-size: 0.9rem; color: #6b7280; }

    .profile-dropdown .divider { height: 1px; background: #eef2f6; margin: 8px 0; }

    .profile-dropdown a.item { display: block; padding: 8px 10px; border-radius: 8px; color: #111827; text-decoration: none; font-weight: 600; }
    .profile-dropdown a.item:hover { background: #f3f4f6; }

    .navbar-custom .nav-links a {
      color: rgba(255,255,255,0.94);
      text-decoration: none;
      font-weight: 500;
      padding: 10px 12px;
      border-radius: 999px;
      transition: transform 0.18s ease, background 0.18s ease, color 0.18s ease;
      white-space: nowrap;
    }

    .navbar-custom .nav-links a:hover {
      background: rgba(255,255,255,0.18);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .navbar-custom .mobile-toggle {
      display: none;
      border: 1px solid rgba(255,255,255,0.72);
      background: rgba(255,255,255,0.11);
      color: #ffffff;
      border-radius: 14px;
      width: 44px;
      height: 44px;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }

    .navbar-custom .mobile-toggle:hover {
      background: rgba(255,255,255,0.2);
    }

    .navbar-custom .mobile-toggle span {
      display: block;
      width: 22px;
      height: 2px;
      background: #fff;
      box-shadow: 0 6px 0 #fff, 0 -6px 0 #fff;
      border-radius: 2px;
    }

    .nav-checkbox {
      display: none;
    }

    @media (max-width: 840px) {
      .navbar-wrap {
        padding: 0 14px;
      }

      .navbar-custom {
        flex-wrap: wrap;
        min-height: auto;
        padding: 14px 16px;
        gap: 12px;
      }

      .navbar-custom .search-group {
        width: 100%;
        order: 2;
        max-width: none;
        margin: 0;
      }

      .navbar-custom .nav-links {
        width: 100%;
        flex-direction: column;
        align-items: stretch;
        gap: 0;
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.28s ease;
      }

      .navbar-custom .nav-links a {
        width: 100%;
        padding: 12px 16px;
        border-radius: 18px;
      }

      .navbar-custom .mobile-toggle {
        display: flex;
      }

      .nav-checkbox:checked + .navbar-custom .nav-links {
        max-height: 360px;
      }
    }

    @media (max-width: 520px) {
      .navbar-custom {
        padding: 12px 14px;
        border-radius: 18px;
      }
    }

    .stApp {
      background: #eef2ff;
    }
    </style>

    <div class="navbar-wrap">
      <input class="nav-checkbox" id="nav-checkbox" type="checkbox">
      <nav class="navbar-custom">
        <a class="brand-text" href="#">My<strong>Brand</strong></a>
        <div class="search-group">
          <input type="search" placeholder="Search products..." aria-label="Search">
          <button type="button">Search</button>
        </div>
        <label class="mobile-toggle" for="nav-checkbox" aria-label="Toggle navigation">
          <span></span>
        </label>
        <div class="nav-links">
          <a href="#home">Home</a>
          <a href="#products">Products</a>
          <a href="#recommendations">Recommendations</a>
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
          <!-- Profile icon (right-most) -->
          <div class="profile" id="profileMenu">
            <button class="profile-button" id="profileBtn" aria-haspopup="true" aria-expanded="false">
              <i class="bi bi-person-circle" style="font-size:22px"></i>
            </button>
            <div class="profile-dropdown" role="menu" aria-labelledby="profileBtn">
              <div class="user-info">
                <div class="name">Ajay Kumar</div>
                <div class="email">ajay@example.com</div>
              </div>
              <div class="divider"></div>
              <a class="item" href="?action=profile">My Profile</a>
              <a class="item" href="?action=orders">My Orders</a>
              <a class="item" href="?action=logout">Logout</a>
            </div>
          </div>
        </div>
      </nav>
    </div>
    <script>
    (function(){
      const profile = document.getElementById('profileMenu');
      const btn = document.getElementById('profileBtn');
      document.addEventListener('click', function(e){
        const inside = e.target.closest && e.target.closest('#profileMenu');
        if(inside){
          profile.classList.toggle('open');
          btn.setAttribute('aria-expanded', profile.classList.contains('open'));
        } else {
          profile.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
        }
      });
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

params = st.experimental_get_query_params() if hasattr(st, 'experimental_get_query_params') else st.query_params

if 'action' in params:
  action = params.get('action')[0]
  if action == 'logout':
    # clear user-related session keys
    for k in list(st.session_state.keys()):
      if k in ('user', 'email', 'logged_in'):
        del st.session_state[k]
    # clear query params and reload
    if hasattr(st, 'experimental_set_query_params'):
      st.experimental_set_query_params()
    else:
      st.query_params = {}
    st.experimental_rerun()
  elif action == 'login':
    st.session_state['user'] = 'Ajay Kumar'
    st.session_state['email'] = 'ajay@example.com'
    st.session_state['logged_in'] = True
    if hasattr(st, 'experimental_set_query_params'):
      st.experimental_set_query_params()
    else:
      st.query_params = {}
    st.experimental_rerun()

# simple login flow: show login prompt when no user in session
if 'user' not in st.session_state:
  st.markdown("## Please sign in")
  st.write("You are not signed in. Click the button to sign in as a demo user.")
  if st.button('Login as Ajay Kumar'):
    st.session_state['user'] = 'Ajay Kumar'
    st.session_state['email'] = 'ajay@example.com'
    st.session_state['logged_in'] = True
    st.experimental_rerun()
else:
  st.write("# Home")
  st.write("This is a responsive Bootstrap-style navbar implemented with Streamlit.")
  st.write("Use the links above to navigate the page sections.")