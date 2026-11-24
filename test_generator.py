import unittest

from src.generator import build_prompt, count_spoken_characters, extract_spoken_script


class GeneratorTests(unittest.TestCase):
    def test_prompt_contains_creator_settings(self):
        prompt = build_prompt(
            topic="3 confidence habits",
            audience="students",
            platform="TikTok",
            niche="Personal growth",
            language="English",
            tone="Funny",
            duration_seconds=30,
            max_characters=400,
        )
        self.assertIn("3 confidence habits", prompt)
        self.assertIn("30 seconds", prompt)
        self.assertIn("400 characters", prompt)

    def test_extract_spoken_script(self):
        text = "## Hook\nA hook\n## Spoken Script\nHello there.\nKeep going.\n## CTA\nFollow me."
        self.assertEqual(extract_spoken_script(text), "Hello there.\nKeep going.")

    def test_character_count_ignores_line_breaks(self):
        self.assertEqual(count_spoken_characters("ab\ncd\r"), 4)


if __name__ == "__main__":
    unittest.main()
