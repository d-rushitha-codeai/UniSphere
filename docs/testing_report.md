# UniSphere – Software Testing Report

## 1. Introduction

This document describes the testing performed on UniSphere, a student networking platform developed using Python, Streamlit and SQLite.

The application was tested to verify its main features, database operations, user interactions and custom data structures.

## 2. Testing Environment

- Programming Language: Python 3.11.2
- Frontend Framework: Streamlit
- Database: SQLite
- Development Environment: Visual Studio Code
- Operating System: Windows
- Testing Approach: Manual functional testing and Python compilation checks

## 3. Functional Testing

| Test ID | Feature Tested | Expected Result | Status |
|---|---|---|---|
| TC01 | Student Registration | New account is created successfully | Passed |
| TC02 | Student Login | Valid credentials allow login | Passed |
| TC03 | Profile Management | Profile details can be saved | Passed |
| TC04 | Student Discovery | Students can be searched and filtered | Passed |
| TC05 | Connection Requests | Requests can be sent and received | Passed |
| TC06 | Connection Management | Requests can be accepted and connections displayed | Passed |
| TC07 | Student Feed | Posts can be created and displayed | Passed |
| TC08 | Post Likes | Users can like and unlike posts | Passed |
| TC09 | Comments | Users can add comments to posts | Passed |
| TC10 | Notifications | Notifications can be viewed and managed | Passed |
| TC11 | Communities | Users can create and join communities | Passed |
| TC12 | Community Discussions | Members can publish discussions | Passed |

## 4. Data Structure Testing

The custom data structures were tested independently and, where applicable, integrated into application features.

| Data Structure | Testing Performed | Result |
|---|---|---|
| Graph | Vertex creation, edge creation and neighbour retrieval | Passed |
| BFS | Traversal of connected students | Passed |
| Linked-List Queue | Enqueue and dequeue operations | Passed |
| Trie | Prefix-based student searching | Passed |
| Hash Table | Insert, search and delete operations | Passed |
| Max Heap | Priority-based insertion and extraction | Passed |

## 5. Database Testing

The SQLite database was checked to verify the creation and operation of the required tables.

The database contains tables for:

- Users
- Profiles
- Connection Requests
- Connections
- Posts
- Post Likes
- Post Comments
- Notifications
- Communities
- Community Members
- Community Posts

Database operations such as inserting, retrieving and updating records were tested through the application.

## 6. Compilation Testing

The following command was executed:

`python -m compileall -q .`

The command completed without reporting compilation errors.

## 7. User Interface Testing

The following application sections were checked:

- Landing Page
- Student Dashboard
- My Profile
- Discover Students
- My Network
- Student Feed
- Notifications
- Communities

Navigation between the sections and their main operations worked as expected during manual testing.

## 8. Conclusion

The testing process verified that the main UniSphere application features, database operations and custom data structures work as expected in the tested environment.

The application successfully demonstrates student networking functionality through a modular Python application supported by SQLite and custom Data Structures and Algorithms.