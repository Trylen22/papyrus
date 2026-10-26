# Papyrus

A collection of local assistant experiments combining an animated ASCII skull, streamed language-model responses, voice interaction, and email-related tools.

## Entry points

| File | Role |
|---|---|
| `main.py` | Pygame fullscreen skull interface and keyboard conversation |
| `rendering.py`, `state_manager.py` | Drawing and avatar state |
| `text_streamer.py`, `local_model.py` | Streamed model interaction |
| `run.py` | Starts the voice server on port 8001 and API on port 8000 |
| `voice_server.py`, `voice.py`, `tts_manager.py` | Speech and voice-service experiments |
| `api.py`, `email_agent.py` | API and email-related integration |

The browser file is named `lndex.html` in this revision. The older `readme.txt` describes a proposed layout rather than the actual repository structure.

## Status

This is an experimental snapshot with several entry points and machine-specific model, audio, and authentication assumptions. It does not yet provide a verified clean-install workflow. `main.py` opens a fullscreen graphical window; `run.py` starts network services and initializes voice components. Read their imports and configuration before launching them.

For development, use a dedicated Python environment and inspect `requirements.txt` against the entry point you intend to run. Model files, audio devices, local services, and credentials are separate prerequisites; installing Python packages alone does not establish a working assistant.

## Data and validation

Keep mailbox credentials, message logs, conversation memory, and model files local. Use synthetic data when preparing a public recording. This documentation update did not connect to a mailbox, activate a microphone, or publish a video of an unverified workflow.

A useful next step is to separate the avatar, model adapter, voice service, and email adapter into independently runnable components with sanitized example configuration. The current repository should be treated as research code rather than a deployed personal assistant.
