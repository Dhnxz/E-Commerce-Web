"""Streamlit frontend for recommendation-engine.

Flow:
Streamlit -> Supabase -> PostgreSQL -> Recommendation Engine
"""

import os
import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Ensure project root is on sys.path so `backend` package imports work
# when running `streamlit run frontend/app.py` from the project folder.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

from backend.supabase_client import SupabaseClient
from backend.recommendation import recommend
from login_page import render_login_page


st.set_page_config(
    page_title="Recommendation Engine",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        st.error("Set SUPABASE_URL and SUPABASE_KEY environment variables")
        return None
    return SupabaseClient(url, key)


def main():
    st.sidebar.title("Navigation")
    view = st.sidebar.radio("Choose a screen", ["Recommendation Demo", "Ecommerce Login"], index=0)

    if view == "Ecommerce Login":
        render_login_page()
        return

    st.title("Recommendation Engine — Demo")

    client = get_client()
    if client is None:
        return

    st.sidebar.header("User")
    user_id = st.sidebar.number_input("User ID", min_value=1, value=1)
    top_k = st.sidebar.slider("Top K", min_value=1, max_value=20, value=5)

    # Fetch products
    with st.spinner("Loading products..."):
        products = client.get_table("products") or []

    prod_map = {p.get("product_id"): p for p in products}

    st.subheader("Products")
    if not products:
        st.info("No products found yet. Apply `database/schema.sql` in Supabase and seed products/interactions.")
    else:
        for p in products[:50]:
            st.write(f"{p.get('product_id')}: {p.get('product_name')} — ${p.get('price')}")

    if st.button("Get recommendations"):
        with st.spinner("Computing recommendations..."):
            rec_ids = recommend(user_id=int(user_id), top_k=int(top_k))

        if not rec_ids:
            st.info("No recommendations found — ensure interactions exist.")
        else:
            st.subheader("Recommended for you")
            for rid in rec_ids:
                p = prod_map.get(rid)
                if p:
                    st.write(f"{p.get('product_id')}: {p.get('product_name')} — ${p.get('price')}")
                else:
                    st.write(f"Product id {rid}")


if __name__ == "__main__":
    main()
