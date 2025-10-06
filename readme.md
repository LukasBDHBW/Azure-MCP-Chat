# Azure GPT MCP Chatbot

Ein interaktiver Chatbot mit Azure OpenAI (GPT) und MCP-Tool-Integration, gebaut mit Streamlit und LangGraph.

## Features

- Chatbot-UI mit Streamlit
- Chatverlauf bleibt erhalten
- Anbindung an Azure OpenAI (GPT-4o oder anderes Modell)
- Nutzung von MCP-Tools (z.B. Addieren, Geheimnis abrufen)
- Einfache Anpassung und Erweiterung

## Voraussetzungen

- Python 3.10+
- Zugang zu Azure OpenAI (API-Key, Endpoint, Deployment)
- MCP-Server (wird automatisch als Subprozess gestartet)

## Installation

1. **Repository klonen**
    ```bash
    git clone <REPO-URL>
    cd <REPO-ORDNER>
    ```

2. **Abhängigkeiten installieren**
    ```bash
    pip install -r requirements.txt
    ```

3. **.env Datei anlegen**

    Erstelle eine `.env`-Datei im Projektordner mit folgendem Inhalt (ersetze durch deine Werte):

    ```
    AZURE_OPENAI_API_KEY=dein-azure-openai-key
    AZURE_OPENAI_ENDPOINT=https://dein-endpoint.openai.azure.com/
    OPENAI_API_VERSION=2025-01-01-preview
    AZURE_OPENAI_DEPLOYMENT=gpt-4o
    ```

## Starten

1. **MCP-Server und Chatbot starten**
    ```bash
    streamlit run app.py
    ```

    Die App öffnet sich im Browser (standardmäßig unter http://localhost:8501).

## Dateien

- `app.py` – Streamlit-Frontend, startet den MCP-Server und verbindet den Chatbot mit Azure OpenAI.
- `agent.py` – Beispiel für die Agent-Logik (CLI, nicht für Streamlit nötig).
- `server.py` – MCP-Server mit Beispiel-Tools (`add`, `get_secret`).
- `.env` – Umgebungsvariablen für Azure OpenAI.
- `requirements.txt` – Alle benötigten Python-Pakete.

## Beispiel-Tools

- **add(a, b):** Addiert zwei Zahlen.
- **get_secret():** Gibt das Geheimnis zurück (z.B. 45).

## Hinweise

- Das „Deploy“-Badge oben rechts ist ein Streamlit-Feature und kann lokal ggf. nicht entfernt werden.
- Die MCP-Tools können beliebig erweitert werden (siehe `server.py`).

## Lizenz

None
