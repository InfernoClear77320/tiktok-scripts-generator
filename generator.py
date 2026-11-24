"""Prompt construction and small helpers for TikTok Scripts Generator."""

from __future__ import annotations


def build_prompt(
    *,
    topic: str,
    audience: str,
    platform: str,
    niche: str,
    language: str,
    tone: str,
    duration_seconds: int,
    max_characters: int,
    key_message: str = "",
    extra_instructions: str = "",
    include_cta: bool = True,
    include_shot_list: bool = True,
    include_captions: bool = True,
    include_hashtags: bool = True,
) -> str:
    """Build a detailed, constrained prompt for a short-form video script."""
    cta_rule = "Include a natural, non-pushy call to action." if include_cta else "Do not include a call to action."
    shot_rule = "Include a concise shot list, one visual idea per beat." if include_shot_list else "Do not include a shot list."
    caption_rule = "Include 3 short on-screen caption suggestions." if include_captions else "Do not include on-screen captions."
    hashtag_rule = "Include 5 relevant hashtags." if include_hashtags else "Do not include hashtags."

    return f"""
You are an experienced short-form video scriptwriter and editor.
Create one original, ready-to-record script for {platform}.

CREATOR BRIEF
Topic: {topic}
Target audience: {audience}
Niche: {niche}
Output language: {language}
Tone: {tone}
Target runtime: about {duration_seconds} seconds
Maximum spoken-script length: {max_characters} characters, including spaces
Key takeaway: {key_message or "Choose one useful, specific takeaway that fits the topic."}
Additional instructions: {extra_instructions or "None"}

WRITING RULES
- Open with a compelling, specific hook in the first sentence. Avoid generic intros like "Hey guys".
- Keep the spoken script natural and easy to say aloud.
- Use short sentences and a clear progression: hook, value, payoff.
- Focus on one main idea. Avoid filler, fake urgency, fabricated statistics, and unsupported claims.
- Do not promise guaranteed views, virality, money, health outcomes, or other results.
- Respect the requested character limit for spoken words. Production notes do not count toward that limit.
- Keep spoken narration clearly separate from captions, shot notes, hashtags, and CTA.
- {cta_rule}
- {shot_rule}
- {caption_rule}
- {hashtag_rule}

Return these headings in Markdown:
## Hook
## Spoken Script
## Character Count
## On-screen Captions
## Shot List
## Hashtags
## CTA

For any section not requested, write "Not requested". Do not add an introduction before the headings.
""".strip()


def extract_spoken_script(markdown: str) -> str:
    """Extract text under the Spoken Script heading, stopping at the next heading."""
    lines = markdown.splitlines()
    in_script = False
    collected: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("## spoken script"):
            in_script = True
            continue
        if in_script and stripped.startswith("## "):
            break
        if in_script:
            collected.append(line)
    return "\n".join(collected).strip()


def count_spoken_characters(text: str) -> int:
    """Count characters including spaces, excluding line-break characters."""
    return len(text.replace("\n", "").replace("\r", ""))
