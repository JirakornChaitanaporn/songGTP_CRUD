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

### 🏗️ Class Diagram (Codebase Architecture & Strategy Pattern)
This diagram illustrates the classes exactly as they exist in the Django codebase, covering Models, Views, and the Strategy Pattern.

```mermaid
classDiagram
    %% Django Base Classes
    class Model {
        <<Django Model>>
    }
    class AbstractUser {
        <<Django Model>>
    }
    class View {
        <<Django View>>
    }
    class CreateView {
        <<Django View>>
    }
    
    %% Models
    class User {
        +id : int
        +username : str
        +email : str
        +created_at : datetime
    }
    
    class Library {
        +id : int
        +user_id : int
        +created_at : datetime
    }
    
    class Prompt {
        +id : int
        +task_id : str
        +user_id : int
        +song_name : str
        +song_genre : str
        +song_mood : str
        +generation_status : str
        +description : str
        +lyrics : str
        +keywords : str
        +created_at : datetime
    }
    
    class Song {
        +id : int
        +prompt_id : int
        +library_id : int
        +song_name : str
        +image_link : str
        +song_url : str
        +shared_code : str
        +sharing_status : str
        +description : str
        +lyrics : str
        +length : str
        +created_at : datetime
    }

    AbstractUser <|-- User
    Model <|-- Library
    Model <|-- Prompt
    Model <|-- Song

    %% Model Relationships
    User "1" -- "1" Library : has
    User "1" -- "0..*" Prompt : has
    Library "1" -- "0..*" Song : has
    Prompt "1" -- "1" Song : has

    %% Enumerations (TextChoices)
    class Mood {
        <<TextChoices>>
        HAPPY, SAD, ROMANTIC, ANGRY, ENERGETIC, CALM
    }
    class Genre {
        <<TextChoices>>
        POP, ROCK, HEAVY_METAL, SOFT_ROCK, POP_ROCK, COUNTRY
    }
    class Generation {
        <<TextChoices>>
        PENDING, TEXT_SUCCESS, FIRST_SUCCESS, SUCCESS, ERROR
    }
    class Status {
        <<TextChoices>>
        PUBLIC, PRIVATE
    }

    %% User Views
    class GoogleOAuthRedirectView
    class UserLoginView
    class LogoutView
    View <|-- GoogleOAuthRedirectView
    View <|-- UserLoginView
    View <|-- LogoutView

    %% Library Views
    class CreateLibraryView
    class SearchLibraryView
    class DeleteLibraryView
    class UpdateLibraryView
    class LibraryView
    CreateView <|-- CreateLibraryView
    View <|-- SearchLibraryView
    View <|-- DeleteLibraryView
    View <|-- UpdateLibraryView
    View <|-- LibraryView

    %% Prompt Views
    class CreatePromptMockupView
    class CreateGenerateSongView
    class ShowPrompt
    class SunoStatusViewController
    CreateView <|-- CreatePromptMockupView
    View <|-- CreateGenerateSongView
    View <|-- ShowPrompt
    View <|-- SunoStatusViewController

    %% Song Views
    class DeleteSongView
    class GetSongView
    class PatchSharingStatusView
    class GetPublicSongView
    class GetDownloadSongView
    View <|-- DeleteSongView
    View <|-- GetSongView
    View <|-- PatchSharingStatusView
    View <|-- GetPublicSongView
    View <|-- GetDownloadSongView

    %% Strategy Pattern Components
    class SongGenerationContext {
        -_strategy : SongGenerationStrategy
        +__init__()
        +execute(request)
    }
    class SongGenerationStrategy {
        <<ABC>>
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
