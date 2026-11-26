# UniSphere – Student Networking Platform

## 1. Project Overview

UniSphere is a student networking web application developed using Python and Streamlit. It provides a platform for university students to connect, communicate, share updates and participate in communities.

The application aims to improve student interaction and collaboration through a centralized digital platform.

## 2. Project Objectives

- Provide secure student registration and login.
- Allow students to create and manage their profiles.
- Help students discover and connect with other students.
- Enable students to share posts, like and comment.
- Provide notifications for important activities.
- Allow students to create, join and participate in communities.
- Demonstrate practical applications of Data Structures and Algorithms.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| Streamlit | User interface and web application |
| SQLite | Database management |
| VS Code | Development environment |
| SQL | Database queries |
| HTML and CSS | Interface styling |

## 4. Main Features

### Authentication
- Student registration.
- Login using username and password.
- Password hashing using PBKDF2-HMAC-SHA256.
- Input validation and duplicate account prevention.

### Student Profiles
- Student information.
- Programme and branch.
- Academic year.
- Bio, skills and interests.

### Discover Students
- Search students by name or username.
- Filter students by branch and academic year.
- Prefix and substring searching using a Trie.
- View connection status.

### Student Connections
- Send connection requests.
- Accept or reject requests.
- View accepted connections.
- Remove connections.
- Discover recommendations using mutual connections.

### Student Feed
- Create text posts.
- Like and unlike posts.
- Add and view comments.
- Edit and delete personal posts.

### Notifications
- Receive activity notifications.
- View read and unread notifications.
- Mark notifications as read.
- Delete notifications.

### Communities
- Create student communities.
- Explore existing communities.
- Join and leave communities.
- Publish community discussions.

## 5. Data Structures and Algorithms

| Data Structure | Application |
|---|---|
| Graph | Represents student connections |
| Breadth-First Search (BFS) | Traverses the student network |
| Linked-List Queue | Manages FIFO notification queue operations |
| Trie | Supports student prefix and substring searching |
| Custom Hash Table | Demonstrates key-value storage, collision handling and resizing |
| Max Heap | Prioritizes student recommendations |

### Graph
An undirected graph with an adjacency list represents student connections. Each student is a vertex, and each accepted connection is an edge.

### BFS
Breadth-First Search traverses the student network using a custom queue.

### Trie
A Trie stores student name and username suffixes to support prefix-based matching, including substring searches.

### Custom Hash Table
A hash table uses a custom hash function and separate chaining to handle collisions. It also supports resizing.

### Max Heap
A Max Heap prioritizes recommendations according to the number of mutual connections.

### Queue
A linked-list-based queue demonstrates First-In-First-Out operations.

## 6. Database Design

UniSphere uses SQLite for persistent data storage.

Main database tables:

- users
- profiles
- connection_requests
- connections
- posts
- post_likes
- post_comments
- notifications
- communities
- community_members
- community_posts

The database stores student information, connections, posts, interactions, notifications and community activities.

## 7. Project Structure

```text
UniSphere/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── db.py
│   └── repositories/
│
├── dsa/
│   ├── graph.py
│   ├── queue.py
│   ├── trie.py
│   ├── hash_table.py
│   └── max_heap.py
│
├── services/
│   ├── auth_service.py
│   ├── profile_service.py
│   ├── discovery_service.py
│   ├── connection_service.py
│   ├── graph_service.py
│   ├── recommendation_service.py
│   ├── post_service.py
│   ├── notification_service.py
│   └── community_service.py
│
├── uploads/
├── pages/
├── ui/
├── config/
├── tests/
├── docs/
└── demo_data/
```

## 8. Installation and Execution

### Requirements
- Python 3.11 or later
- pip
- Visual Studio Code

### Step 1: Open the project directory

Open the UniSphere folder in Visual Studio Code.

### Step 2: Create a virtual environment

```bash
py -3.11 -m venv venv
```

### Step 3: Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Run the application

```bash
python -m streamlit run app.py
```

### Step 6: Open the application

Open the Local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

The SQLite database is initialized automatically when the application starts.

## 9. Testing

The project has undergone syntax compilation and manual functional testing.

Testing includes:

- Account registration and login.
- Profile creation and updates.
- Student search and filtering.
- Connection request and acceptance.
- Feed posts, likes and comments.
- Notification management.
- Community creation and discussions.
- Individual data structure operations.
- Recommendation ordering.

## 10. Conclusion

UniSphere demonstrates how Python programming, database management, web application development and Data Structures and Algorithms can be combined to develop a practical student networking platform.

The project provides students with a shared environment to discover peers, build connections, exchange information and participate in academic communities.

---

**Project:** UniSphere  
**Domain:** Student Networking Platform  
**Programming Language:** Python  
**Database:** SQLite  
**Framework:** Streamlit