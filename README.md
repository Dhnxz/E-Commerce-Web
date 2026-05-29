# E-Commerce-Web

Recommendation engine scaffold for an e-commerce project.

Architecture
------------

Streamlit (frontend) -> Supabase -> PostgreSQL -> Recommendation Engine (Python)

Project Structure
-----------------

```text
recommendation-engine/
├── frontend/
│   └── app.py
├── backend/
│   ├── recommendation.py
│   ├── data_loader.py
│   └── supabase_client.py
├── dataset/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── database/
│   └── schema.sql
├── docs/
├── requirements.txt
└── README.md
```

Running locally
---------------

1. Create a Python virtual env and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set Supabase environment variables (replace with your project values):

```powershell
$env:SUPABASE_URL = "https://xyzcompany.supabase.co"
$env:SUPABASE_KEY = "public-anon-key"
```

3. Run the frontend (Streamlit):

```powershell
streamlit run frontend/app.py
```

Notes
-----
- `backend/supabase_client.py` loads `SUPABASE_URL` and `SUPABASE_KEY` from `.env`.
- `backend/recommendation.py` calls the `get_recommendations` RPC function from Supabase.
- `database/schema.sql` contains the table definitions and the recommendation function.

Next steps: apply `database/schema.sql` in Supabase, seed `products` and `interactions`, and iterate on ranking logic.
