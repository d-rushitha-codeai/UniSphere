
# UniSphere – System Architecture

```mermaid
flowchart TB
    A["Student / User"] --> B["Streamlit User Interface"]

    B --> C["Application Layer"]

    C --> D["Authentication Service"]
    C --> E["Profile Service"]
    C --> F["Discovery Service"]
    C --> G["Connection Service"]
    C --> H["Post Service"]
    C --> I["Notification Service"]
    C --> J["Community Service"]
    C --> K["Recommendation Service"]

    D --> L["Database Layer"]
    E --> L
    F --> M["Trie"]
    F --> L
    G --> N["Graph and BFS"]
    G --> L
    H --> L
    I --> O["Linked-List Queue"]
    I --> L
    J --> L
    K --> N
    K --> P["Max Heap"]
    K --> L

    L --> Q[("SQLite Database")]

    M --> F
    N --> G
    O --> I
    P --> K
```

## Architecture Explanation

1. **Presentation Layer:** Streamlit provides the user interface.
2. **Application Layer:** Services handle authentication, profiles, connections, posts, notifications and communities.
3. **DSA Layer:** Custom data structures support searching, network traversal, notification queue operations and recommendation ranking.
4. **Database Layer:** SQLite stores application data persistently.

The application follows a modular architecture that separates the user interface, business logic, data structures and database operations.
