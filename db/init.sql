CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
  id UUID UNIQUE PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
  name varchar,
  email varchar,
  password varchar,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);
