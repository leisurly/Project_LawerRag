CREATE DATABASE LawerJudgment;
USE LawerJudgment;

DROP DATABASE  LawerJudgment;
CREATE TABLE Judgments (
    jid VARCHAR(100) UNIQUE,            -- 判決唯一 ID
    jyear INT,                         -- 民國年
    jcase VARCHAR(10),                 -- 案件類型（如「判」、「裁」）
    jno VARCHAR(20) PRIMARY KEY,         -- 案號
    jdate DATE,                        -- 公告日期
    jtitle VARCHAR(255),              -- 案件主題（簡稱）
    jfull LONGTEXT,                   -- 判決全文
    file_path VARCHAR(500)            -- 對應檔案路徑（可選）
);
SELECT * FROM Judgments;
CREATE TABLE IF NOT EXISTS JudgmentChunks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jid VARCHAR(100) NOT NULL,
    chunk_index INT NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_inbox TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



