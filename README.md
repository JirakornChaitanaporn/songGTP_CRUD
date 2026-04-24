# 🎵 SongGTP CRUD Application

A Django-based CRUD (Create, Read, Update, Delete) web application for managing SongGTP data.  
This project demonstrates backend development using Django and Django Admin for rapid data management.

---

## 🚀 Getting Started

Follow the steps below to run the project locally.

---

## 1. Clone the Repository

```bash
git clone https://github.com/JirakornChaitanaporn/songGTP_CRUD.git
cd songGTP_CRUD
```
## 2. Create a Virtual Environment
macOS / Linux:
```bash
python3 -m venv .env
```
Windows:
```bash
python -m venv .env
```
## 3. Activate the Virtual Environment
macOS / Linux:
```bash
source .env/bin/activate
```
Windows
```bash
.env\Scripts\activate
```
## 4. Install Dependencies
```bash
pip install -r requirements.txt
```
## 5. Configure Environment Variables

Before running the app, copy the example env file and fill in your own values:

```bash
cp .env.example .env
```

Then open `.env` and fill in each variable. See the table and guides below.

### 📋 Variable Reference

| Variable | Description | Required |
|---|---|---|
| `SUNO_API_KEY` | Your Suno API key for real song generation | Only for `suno` strategy |
| `GENERATOR_STRATEGY` | Generation strategy: `mock` or `suno` | ✅ Yes |
| `GOOGLE_OAUTH_CLIENT_ID` | Google OAuth 2.0 Client ID | ✅ Yes |
| `GOOGLE_OAUTH_CLIENT_SECRET` | Google OAuth 2.0 Client Secret | ✅ Yes |
| `BASE_URL` | Base URL of your local server (default: `http://localhost:8000/`) | ✅ Yes |

---

### 🔑 How to Get Your Google OAuth Credentials

Follow these steps to create a Google OAuth 2.0 client for local development:

**Step 1 — Go to Google Cloud Console**
- Visit [https://console.cloud.google.com/](https://console.cloud.google.com/)
- Sign in with your Google account.

**Step 2 — Create or Select a Project**
- Click the project dropdown at the top.
- Click **"New Project"**, give it a name (e.g. `SongGTP`), and click **"Create"**.

**Step 3 — Enable the OAuth Consent Screen**
1. In the left sidebar, go to **APIs & Services → OAuth consent screen**.
2. Choose **External** (so any Google account can log in) and click **"Create"**.
3. Fill in the required fields:
   - **App name**: `SongGTP`
   - **User support email**: your email
   - **Developer contact email**: your email
4. Click **"Save and Continue"** through the remaining steps (Scopes, Test users) — defaults are fine for local dev.

**Step 4 — Create OAuth 2.0 Credentials**
1. Go to **APIs & Services → Credentials**.
2. Click **"+ Create Credentials"** → **"OAuth client ID"**.
3. Set **Application type** to **Web application**.
4. Give it a name (e.g. `SongGTP Local`).
5. Under **Authorised redirect URIs**, add:
   ```
   http://localhost:8000/accounts/google/login/callback/
   ```
6. Click **"Create"**.
7. A dialog will show your **Client ID** and **Client Secret** — copy both.

**Step 5 — Paste into `.env`**
```env
GOOGLE_OAUTH_CLIENT_ID="your-client-id-here.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret-here"
```

---

### 🎵 Choosing a Generation Strategy (`GENERATOR_STRATEGY`)

This project supports two song generation strategies:

| Value | Behaviour |
|---|---|
| `mock` | Generates a fake song instantly using placeholder data — no API key needed, great for testing |
| `suno` | Calls the real Suno API to generate actual songs — requires a valid `SUNO_API_KEY` |

**To get a Suno API Key:**
1. Visit [https://sunoapi.org/](https://sunoapi.org/) and sign up.
2. Copy your API key from the dashboard.
3. Paste it into `.env`:
   ```env
   SUNO_API_KEY="your-suno-api-key-here"
   GENERATOR_STRATEGY="suno"
   ```

For local testing without a Suno account, just use:
```env
GENERATOR_STRATEGY="mock"
```

---

## 🎨 Architecture & Design Patterns

### 🏗️ Class Diagram (Full Application & Strategy Pattern)
This diagram illustrates all the major components of the system, matching the application's actual Django structure and including the Strategy Pattern for song generation.

```mermaid
classDiagram
    %% Django Base Models
    class Model {
        <<Django Model>>
    }
    class AbstractUser {
        <<Django Model>>
    }
    
    %% Application Models
    class UserModel {
        +id : int
        +email : str
        +first_name : str
        +last_name : str
        +created_at : datetime
    }
    
    class LibraryModel {
        +id : int
        +user_id : int
        +created_at : datetime
    }
    
    class PromptModel {
        +id : int
        +task_id : str
        +song_name : str
        +song_genre : Genre
        +song_mood : Mood
        +generation_status : Generation
        +description : str
        +lyrics : str
        +keywords : str
        +created_at : datetime
    }
    
    class SongModel {
        +id : int
        +prompt_id : int
        +library_id : int
        +song_name : str
        +shared_link : str
        +sharing_status : Status
        +song_url : str
        +description : str
        +lyrics : str
        +length : str
        +created_at : datetime
    }

    AbstractUser <|-- UserModel
    Model <|-- LibraryModel
    Model <|-- PromptModel
    Model <|-- SongModel

    %% Relationships
    UserModel "1" -- "1" LibraryModel : has
    UserModel "1" -- "0..*" PromptModel : has
    LibraryModel "1" -- "0..*" SongModel : has
    PromptModel "1" -- "1" SongModel : has

    %% Enumerations
    class Mood {
        <<enumeration>>
        Happy
        Sad
        Romantic
        Angry
        Energetic
        Calm
    }
    class Genre {
        <<enumeration>>
        Pop
        Rock
        Heavy_metal
        Soft_rock
        Pop_rock
        Country
    }
    class Generation {
        <<enumeration>>
        Pending
        Text_Success
        First_Success
        Success
        Error
    }
    class Status {
        <<enumeration>>
        Public
        Private
    }

    PromptModel ..> Mood
    PromptModel ..> Genre
    PromptModel ..> Generation
    SongModel ..> Status

    %% Views
    class UserLoginView {
        +get(request)
        +post(request)
    }
    class LogoutView {
        +get(request)
        +post(request)
    }
    class CreateLibraryView {
        +get(request)
        +post(request)
    }
    class SearchLibraryView {
        +get(request)
    }
    class CreatePromptMockupView {
        +get(request)
        +post(request)
    }
    class CreateGenerateSongView {
        +get(request)
        +post(request)
    }
    class DeleteSongView {
        +get(request)
    }
    class SongView {
        +get(request, pk)
    }
    class PublicSongView {
        +get(request)
    }

    %% Strategy Pattern Components
    class SongGenerationContext {
        -_strategy : SongGenerationStrategy
        +__init__()
        +execute(request)
    }
    class SongGenerationStrategy {
        <<interface>>
        +generate(request)*
    }
    class MockSongGeneratorStrategy {
        +generate(request)
    }
    class SunoSongGeneratorStrategy {
        +generate(request)
    }

    CreatePromptMockupView ..> SongGenerationContext : uses
    CreateGenerateSongView ..> SongGenerationContext : uses
    SongGenerationContext o-- SongGenerationStrategy : configures
    MockSongGeneratorStrategy ..|> SongGenerationStrategy : implements
    SunoSongGeneratorStrategy ..|> SongGenerationStrategy : implements
    
    %% View Dependencies (Conceptual)
    UserLoginView ..> UserModel : access
    CreateLibraryView ..> LibraryModel : access
    SearchLibraryView ..> LibraryModel : access
    CreatePromptMockupView ..> PromptModel : access
    CreateGenerateSongView ..> PromptModel : access
    DeleteSongView ..> SongModel : access
    SongView ..> SongModel : access
    PublicSongView ..> SongModel : access
```

### 🔄 Sequence Diagram (Song Generation Flow)
The following sequence diagram shows the execution flow when a user requests to generate a song:

```mermaid
sequenceDiagram
    actor User
    participant View as View (Mock/Generate)
    participant Context as SongGenerationContext
    participant Env as .env
    participant Strategy as Strategy (Mock/Suno)
    participant API as Database / Suno API
    
    User->>View: POST /generate (form data)
    View->>Context: init SongGenerationContext()
    Context->>Env: Read GENERATOR_STRATEGY
    Env-->>Context: "mock" or "suno"
    
    alt is "suno"
        Context->>Context: set strategy = SunoSongGeneratorStrategy()
    else is "mock"
        Context->>Context: set strategy = MockSongGeneratorStrategy()
    end
    
    View->>Context: execute(request)
    Context->>Strategy: generate(request)
    
    Strategy->>API: Process request (Call API / Save DB)
    API-->>Strategy: Return result / Task ID
    
    Strategy-->>Context: HttpResponseRedirect
    Context-->>View: HttpResponseRedirect
    View-->>User: Redirect to generate page / library
```
