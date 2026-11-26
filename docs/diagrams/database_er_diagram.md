
# UniSphere – Database ER Diagram

## Entity Relationship Diagram

```mermaid
erDiagram

    USERS ||--o| PROFILES : has
    USERS ||--o{ CONNECTION_REQUESTS : sends
    USERS ||--o{ CONNECTION_REQUESTS : receives
    USERS ||--o{ CONNECTIONS : participates
    USERS ||--o{ POSTS : creates
    USERS ||--o{ POST_LIKES : gives
    USERS ||--o{ POST_COMMENTS : writes
    USERS ||--o{ NOTIFICATIONS : receives
    USERS ||--o{ NOTIFICATIONS : triggers
    USERS ||--o{ COMMUNITIES : creates
    USERS ||--o{ COMMUNITY_MEMBERS : joins
    USERS ||--o{ COMMUNITY_POSTS : writes

    POSTS ||--o{ POST_LIKES : receives
    POSTS ||--o{ POST_COMMENTS : contains

    COMMUNITIES ||--o{ COMMUNITY_MEMBERS : has
    COMMUNITIES ||--o{ COMMUNITY_POSTS : contains

    USERS {
        int id PK
        string full_name
        string username UK
        string email UK
        string password_hash
        string password_salt
        datetime created_at
        int is_active
    }

    PROFILES {
        int user_id PK, FK
        string programme
        string branch
        string academic_year
        string bio
        string skills
        string interests
        string profile_picture
    }

    CONNECTION_REQUESTS {
        int id PK
        int sender_id FK
        int receiver_id FK
        string status
        datetime created_at
    }

    CONNECTIONS {
        int id PK
        int user1_id FK
        int user2_id FK
        datetime created_at
    }

    POSTS {
        int id PK
        int user_id FK
        string content
        string image_path
        datetime created_at
        datetime updated_at
    }

    POST_LIKES {
        int id PK
        int post_id FK
        int user_id FK
        datetime created_at
    }

    POST_COMMENTS {
        int id PK
        int post_id FK
        int user_id FK
        string comment
        datetime created_at
    }

    NOTIFICATIONS {
        int id PK
        int recipient_id FK
        int actor_id FK
        string notification_type
        string message
        int related_id
        int is_read
        datetime created_at
    }

    COMMUNITIES {
        int id PK
        string name UK
        string description
        int created_by FK
        datetime created_at
        int is_active
    }

    COMMUNITY_MEMBERS {
        int id PK
        int community_id FK
        int user_id FK
        datetime joined_at
    }

    COMMUNITY_POSTS {
        int id PK
        int community_id FK
        int user_id FK
        string content
        datetime created_at
    }
```

## Database Explanation

### 1. Users and Profiles
Each registered student has an account. A profile stores additional academic and personal information.

### 2. Connections
Connection requests store pending requests between students. Accepted connections are stored separately using two user IDs.

### 3. Student Feed
Posts are connected to their authors. Likes and comments are stored in separate tables.

### 4. Notifications
Notifications identify the recipient and the user who triggered the activity.

### 5. Communities
Students can create communities, join communities and publish discussions.

## Database Design

UniSphere uses a relational SQLite database with primary keys, foreign keys and unique constraints to maintain data consistency.
