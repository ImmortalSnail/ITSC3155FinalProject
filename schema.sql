CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  bio TEXT,
  profile_picture_url VARCHAR(255)
);

CREATE TABLE topics (
  topic_id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT
);

CREATE TABLE posts (
  post_id SERIAL PRIMARY KEY,
  topic_id INTEGER NOT NULL REFERENCES topics(topic_id),
  user_id INTEGER NOT NULL REFERENCES users(user_id),
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  image_url VARCHAR(255),
  upvotes INTEGER DEFAULT 0,
  downvotes INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post_replies (
  reply_id SERIAL PRIMARY KEY,
  post_id INTEGER NOT NULL REFERENCES posts(post_id),
  user_id INTEGER NOT NULL REFERENCES users(user_id),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reply_replies (
  reply_id SERIAL PRIMARY KEY,
  parent_reply_id INTEGER NOT NULL REFERENCES post_replies(reply_id),
  user_id INTEGER NOT NULL REFERENCES users(user_id),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
