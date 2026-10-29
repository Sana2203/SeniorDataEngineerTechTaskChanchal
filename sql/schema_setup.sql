CREATE TABLE IF NOT EXISTS cb_posts (
    post_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('lengthy', 'concise')),
    body_length INTEGER NOT NULL,
    user_name TEXT,
    user_email TEXT,
    company TEXT
);

CREATE INDEX IF NOT EXISTS idx_cb_posts_user_id
ON cb_posts(user_id);

CREATE INDEX IF NOT EXISTS idx_cb_posts_status
ON cb_posts(status);
