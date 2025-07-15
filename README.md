# Reddit User Persona Generator 🧠

This project extracts and analyzes a Reddit user's public activity (posts and comments) to generate a **User Persona** based on behavioral and content patterns. The persona includes key psychological and activity-based insights with references to the user's own content.

---
## 🎬 Demo Video

[![Watch the video](https://img.youtube.com/vi/-RW85a-uk7E/0.jpg)](https://www.youtube.com/watch?v=-RW85a-uk7E)

## 📋 Table of Contents

1. [Features](#-features)
2. [Technologies Used](#-technologies-used)
3. [Installation & Setup](#-installation--setup)
4. [Usage](#-usage)
5. [Sample Outputs](#-sample-outputs)
6. [Configuration](#-configuration)
7. [Customization](#-customization)
8. [Contributing](#-contributing)
9. [License](#-license)
10. [Support](#-support)

---

## 🚀 Features

- Scrapes a user's **posts** and **comments** from Reddit.
- Analyzes activity data:
  - Posting/commenting timestamps (active periods)
  - Content scores (upvotes)
  - NSFW & spoiler percentage
  - Edit behavior and original content ratio
- Generates **human-centric persona insights** using a local LLM (e.g., Mistral via Ollama).
- Saves persona as a well-structured `.txt` file in the `outputs/` directory.
- Includes **inline citations** (short text snippets) from Reddit activity.
- Modular, PEP8-compliant, and easy to extend.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- [PRAW](https://praw.readthedocs.io/) – Python Reddit API Wrapper
- [Ollama](https://ollama.com/) – Local LLM inference
- `python-dotenv` – Environment variable management
- `tqdm` – Progress bars for scraping
- Standard libraries: `argparse`, `re`, `datetime`, `statistics`

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/EshwarAdduri/reddit-persona-generator.git
cd reddit-persona-generator
```

### 2. Create & Activate a Virtual Environment (Recommended)

```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your Reddit API credentials:

```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent_string
```

Obtain credentials by creating a Reddit application at: https://www.reddit.com/prefs/apps

---

## 🧪 Usage

Run the main script with a Reddit user URL:

```bash
python main.py https://www.reddit.com/user/kojied/
```

This will:

1. Scrape recent posts and comments (default limits: 15 posts, 30 comments).
2. Analyze activity metrics and content patterns.
3. Invoke the LLM to generate persona insights.
4. Save the persona file to `outputs/{username}_persona.txt`.

Example output path:

```
outputs/kojied_persona.txt
```

---

## 📝 Sample Outputs

Pre-generated persona files for demonstration:

- `outputs/kojied_persona.txt`
- `outputs/Hungry-Move-6603_persona.txt`

---

## ⚙️ Configuration

- **Comment/Post Limits:** Modify `comment_limit` and `post_limit` in `fetch_reddit_data()`.
- **LLM Model:** Change the model name in `generate_persona()`, e.g.:
  ```python
  response = ollama.chat(model="mistral", messages=[...])
  ```
- **Output Directory:** Default is `outputs/`. Can be changed in `save_to_file()`.

---

## 🎨 Customization

- Add additional persona traits or metrics in `analyze_user_behavior()`.
- Extend citation to include direct links by storing `comment.permalink`.
- Integrate with other LLM providers by abstracting the `ollama.chat` call.

---

## 🤝 Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss your ideas.

---
