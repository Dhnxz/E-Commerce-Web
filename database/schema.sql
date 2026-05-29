-- Supabase schema for recommendation engine

CREATE TABLE IF NOT EXISTS products (
    product_id BIGINT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    description TEXT,
    price NUMERIC,
    rating FLOAT
);

CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT
);

CREATE TABLE IF NOT EXISTS interactions (
    interaction_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    product_id BIGINT REFERENCES products(product_id),
    rating FLOAT
);

CREATE INDEX IF NOT EXISTS idx_interactions_user_id ON interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_interactions_product_id ON interactions(product_id);

CREATE OR REPLACE FUNCTION get_recommendations(
    p_user_id BIGINT,
    p_limit INTEGER DEFAULT 10
)
RETURNS TABLE (
    product_id BIGINT,
    score BIGINT
)
LANGUAGE sql
STABLE
AS $$
    WITH user_products AS (
        SELECT DISTINCT i.product_id
        FROM interactions i
        WHERE i.user_id = p_user_id
    ),
    ranked AS (
        SELECT
            i.product_id,
            COUNT(*)::BIGINT AS score
        FROM interactions i
        WHERE NOT EXISTS (
            SELECT 1
            FROM user_products up
            WHERE up.product_id = i.product_id
        )
        GROUP BY i.product_id
        ORDER BY score DESC, i.product_id ASC
        LIMIT p_limit
    )
    SELECT product_id, score
    FROM ranked;
$$;
