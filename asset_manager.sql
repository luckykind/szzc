-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user' -- 'admin' or 'user'
);

-- 创建代码资产表
CREATE TABLE IF NOT EXISTS code_assets (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(50),
    tags VARCHAR(200),
    file_path VARCHAR(200),
    repo_url VARCHAR(200),
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建一个管理员用户
INSERT INTO users (username, password, role) VALUES ('admin', '\$2b\$12$EXAMPLE_HASHED_PASSWORD', 'admin');
-- 注意: 替换 '\$2b\$12$EXAMPLE_HASHED_PASSWORD' 为实际的 bcrypt 哈希密码
