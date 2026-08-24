# User Table

| Field Name    | Type         | Comment |
|---------------|--------------|----|
| id            | varchar(36)  ||
| user_name     | varchar(50)  ||
| password_hash | varchar(256) ||
| full_name     | varchar(50)  ||
| status        | varchar(36)  ||
| create_time   | varchar(36)  ||
| last_login    | varchar(36)  ||

```
CREATE TABLE users (
    id VARCHAR(36) PRIMARY key default gen_random_uuid(),
    user_name VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    full_name VARCHAR(50),
    status VARCHAR(36) NOT NULL DEFAULT 'active',
    create_time VARCHAR(36),
    last_login VARCHAR(36)
);

```
