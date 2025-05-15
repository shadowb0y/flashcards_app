# flashcards_manager.py
import json
import os
from pathlib import Path

DATA_FILE = Path("data/flashcards.json")
IMAGE_FOLDER = Path("flashcard_images")
IMAGE_FOLDER.mkdir(exist_ok=True, parents=True)

class FlashcardManager:
    def __init__(self):
        self.sections = {}
        self.load_data()

    def load_data(self):
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.sections = json.load(f)
            except json.JSONDecodeError:
                self.sections = {}
        else:
            self.sections = {}
            self.save_data()

    def save_data(self):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.sections, f, indent=2, ensure_ascii=False)

    def add_section(self, path):
        levels = path.split("/")
        current = self.sections
        for level in levels:
            current = current.setdefault(level, {})
        self.save_data()

    def get_section(self, path):
        if not path:
            return self.sections
        levels = path.split("/")
        current = self.sections
        for level in levels:
            current = current.get(level, {})
        return current

    def add_card(self, section_path, question, answer, deck="1", question_images=None, answer_images=None):
        section = self.get_section(section_path)
        if deck not in section:
            section[deck] = []
        section[deck].append({
            "question": question,
            "answer": answer,
            "question_images": question_images or [],
            "answer_images": answer_images or []
        })
        self.save_data()

    def get_all_sections(self):
        return list(self.sections.keys())
