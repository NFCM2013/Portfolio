/* テーブルの作成 */
CREATE TABLE players (
  player_id INT PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  level INT,
  experience INT,
  last_login DATETIME
);

CREATE TABLE items (
  item_id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255),
  type VARCHAR(50)
);

CREATE TABLE player_items (
  player_item_id INT PRIMARY KEY,
  player_id INT,
  item_id INT,
  equipped BOOLEAN,
  quantity INT,
  FOREIGN KEY (player_id) REFERENCES players (player_id),
  FOREIGN KEY (item_id) REFERENCES items (item_id)
);

CREATE TABLE scores (
  score_id INT PRIMARY KEY,
  player_id INT,
  score INT,
  level INT,
  game_date DATE,
  FOREIGN KEY (player_id) REFERENCES players (player_id)
);

/* プレイヤーの追加 */
INSERT INTO players (player_id, username, level, experience, last_login)
VALUES (1, 'NAME1', 10, 5000, '2023-05-01 18:30:00');

/* アイテムの追加 */
INSERT INTO items (item_id, name, description, type)
VALUES (1, 'NAME2', 'A powerful weapon', 'Weapon');

/* プレイヤーのアイテムの追加 */
INSERT INTO player_items (player_item_id, player_id, item_id, equipped, quantity)
VALUES (1, 1, 1, TRUE, 1);

/* スコアの追加 */
INSERT INTO scores (score_id, player_id, score, level, game_date)
VALUES (1, 1, 1000, 5, '2023-05-02');

/* プレイヤーのスコアの更新 */
UPDATE scores
SET score = 600, level = 10
WHERE score_id = 1;

/* リーダーボードの取得 */
SELECT players.username, scores.score
FROM players
JOIN scores ON players.player_id = scores.player_id
ORDER BY scores.score DESC
LIMIT 10;

/* 成績表の取得 */
SELECT players.username, scores.score, scores.level, scores.game_date
FROM players
JOIN scores ON players.player_id = scores.player_id
WHERE players.username = 'NAME1';
