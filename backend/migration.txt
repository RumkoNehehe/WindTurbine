CREATE TABLE recording (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    data JSONB NOT NULL
);

CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    user_type TEXT NOT NULL
);

INSERT INTO app_user (username, password, user_type)
VALUES 
/*admin123, user123*/
    ('admin', 'pbkdf2:sha256:260000$NSgmdnjyhlWjrY2l$c9db6a5223b2a4217051e82088382bac7c31f9d79959c21dd333eec87cfddbf4', 'admin'),
    ('user', 'pbkdf2:sha256:260000$MQfJchIhkE1L4N6G$8d052cf7a776a921453abf9e62ccf34cea2de4a6af8ae9eacb64c4922eb3a6da', 'user');