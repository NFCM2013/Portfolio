/* テーブルの作成 */
CREATE TABLE events (
  id INT PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NOT NULL,
  location VARCHAR(100)
);

/* 予定の追加*/
INSERT INTO events (id, title, start_date, end_date, location)
VALUES (1, 'ミーティング', '2023-06-01 09:00:00', '2023-06-01 10:00:00', '会議室A');

/* 予定の編集 */
UPDATE events
SET title = '重要なプレゼン', start_date = '2023-06-02 14:00:00', end_date = '2023-06-02 16:00:00', location = '会議室B'
WHERE id = 1;

/* 予定の削除 */
DELETE FROM events
WHERE id = 1;

/* 日時に基づく予定の検索 */
SELECT * FROM events
WHERE start_date >= '2023-06-01' AND start_date < '2023-06-02';

/* 場所に基づく予定の検索 */
SELECT * FROM events
WHERE location = '会議室A';

