import os
import re
import praw
import argparse
import ollama
from tqdm import tqdm
from datetime import datetime, timezone
from statistics import mean
from dotenv import load_dotenv

load_dotenv()
# Fetch values from environment
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=client_id, client_secret=client_secret, user_agent=user_agent
)


def extract_username(url):
    match = re.search(r"reddit\.com/user/([^/]+)/?", url)
    return match.group(1) if match else None


def fetch_reddit_data(username, comment_limit=30, post_limit=15):
    try:
        user = reddit.redditor(username)
        content = []

        for comment in tqdm(user.comments.new(limit=comment_limit), desc="Comments"):
            content.append(
                {
                    "type": "comment",
                    "text": comment.body,
                    "score": comment.score,
                    "created": datetime.fromtimestamp(
                        comment.created_utc, tz=timezone.utc
                    ),
                    "edited": bool(comment.edited),
                }
            )

        for post in tqdm(user.submissions.new(limit=post_limit), desc="Posts"):
            content.append(
                {
                    "type": "post",
                    "text": f"{post.title} {post.selftext}".strip(),
                    "score": post.score,
                    "created": datetime.fromtimestamp(
                        post.created_utc, tz=timezone.utc
                    ),
                    "nsfw": post.over_18,
                    "spoiler": post.spoiler,
                    "is_self": post.is_self,
                }
            )

        return content
    except Exception as e:
        print("Error:", e)
        return []


def analyze_user_behavior(content):
    comments = [c for c in content if c["type"] == "comment"]
    posts = [p for p in content if p["type"] == "post"]

    def active_time_period(items):
        if not items:
            return "Unknown"
        avg_hour = round(mean(item["created"].hour for item in items))
        if 5 <= avg_hour < 12:
            return "Morning (5am–12pm UTC)"
        elif 12 <= avg_hour < 17:
            return "Afternoon (12pm–5pm UTC)"
        elif 17 <= avg_hour < 21:
            return "Evening (5pm–9pm UTC)"
        else:
            return "Night (9pm–5am UTC)"

    return {
        "total_posts": len(posts),
        "total_comments": len(comments),
        "active_period": active_time_period(content),
        "avg_post_score": round(mean([p["score"] for p in posts]), 1) if posts else 0.0,
        "avg_comment_score": round(mean([c["score"] for c in comments]), 1)
        if comments
        else 0.0,
        "nsfw_percent": round(
            100 * sum(p.get("nsfw", False) for p in posts) / len(posts), 1
        )
        if posts
        else 0.0,
        "spoiler_percent": round(
            100 * sum(p.get("spoiler", False) for p in posts) / len(posts), 1
        )
        if posts
        else 0.0,
        "original_content_percent": round(
            100 * sum(p.get("is_self", False) for p in posts) / len(posts), 1
        )
        if posts
        else 0.0,
        "edited_comment_percent": round(
            100 * sum(c.get("edited", False) for c in comments) / len(comments), 1
        )
        if comments
        else 0.0,
    }


def generate_persona(username, stats, content):
    persona = f"# Reddit User Persona: {username}\n\n"
    persona += "## Overview\n"
    persona += f"- Username: {username}\n"
    persona += f"- Total Posts: {stats['total_posts']}\n"
    persona += f"- Total Comments: {stats['total_comments']}\n"
    persona += f"- Most Active Period: {stats['active_period']}\n"
    persona += f"- Average Post Score: {stats['avg_post_score']}\n"
    persona += f"- Average Comment Score: {stats['avg_comment_score']}\n"
    persona += f"- NSFW Post Percentage: {stats['nsfw_percent']}%\n"
    persona += f"- Spoiler Post Percentage: {stats['spoiler_percent']}%\n"
    persona += f"- Original Content Percentage: {stats['original_content_percent']}%\n"
    persona += f"- Edited Comment Percentage: {stats['edited_comment_percent']}%\n\n"

    # Prepare sample content for LLM (text only)
    sample_data = ""
    for item in content[:10]:
        snippet = item["text"].strip().replace("\n", " ")
        sample_data += f"{snippet[:300]}...\n\n"

    prompt = f"""
Analyze the user's Reddit activity and generate a brief persona with the following traits:

1. **Topics of Interest**
2. **Motivations & Values**
3. **Frustrations & Pain Points**
4. **Personality Traits**
5. **Behaviour and Habits**
6. **Goals and Needs**

Base each point on Reddit content samples below. Mention key phrases or short snippets as citation instead of links.

### Reddit Activity Samples:
{sample_data}
"""

    try:
        response = ollama.chat(
            model="mistral", messages=[{"role": "user", "content": prompt}]
        )
        insights = response["message"]["content"]
    except Exception as e:
        insights = f"LLM Error: {str(e)}"

    persona += "## Inferred Insights\n"
    persona += insights.strip()

    return persona


def save_to_file(username, persona_text):
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona_text)
    return filename


def main():
    parser = argparse.ArgumentParser(description="Reddit User Persona Generator")
    parser.add_argument("url", help="Reddit profile URL")
    args = parser.parse_args()

    username = extract_username(args.url)
    if not username:
        print("Invalid Reddit URL")
        return

    print(f"Processing user: {username}")
    content = fetch_reddit_data(username)
    stats = analyze_user_behavior(content)
    persona_text = generate_persona(username, stats, content)
    output_path = save_to_file(username, persona_text)
    print(f"Persona file saved at: {output_path}")


if __name__ == "__main__":
    main()
