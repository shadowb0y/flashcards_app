# flashcards_manager.py
import json
import os
import random
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

    def extract_random_card(self, section_path):
        section = self.get_section(section_path)
        if not section:
            return None

        for deck in ["1", "2", "3", "4"]:
            if deck in section and section[deck]:
                cards = section[deck]
                index = random.randint(0, len(cards) - 1)
                return deck, cards[index], index
        return None

    def move_card(self, section_path, current_deck, card_index, direction="up"):
        section = self.get_section(section_path)
        if not section or current_deck not in section:
            return

        decks = ["1", "2", "3", "4"]
        current_idx = decks.index(current_deck)

        if direction == "up" and current_idx < 3:
            target_deck = decks[current_idx + 1]
        elif direction == "down" and current_idx > 0:
            target_deck = decks[current_idx - 1]
        else:
            return

        card = section[current_deck].pop(card_index)
        section.setdefault(target_deck, []).append(card)
        self.save_data()

    def get_all_sections(self):
        return list(self.sections.keys())
    
    def delete_card(self, section_path, deck, index):
        section = self.get_section(section_path)
        if deck in section and 0 <= index < len(section[deck]):
            del section[deck][index]
            self.save_data()

    def update_card(self, section_path, deck, index, new_q, new_a):
        section = self.get_section(section_path)
        if deck in section and 0 <= index < len(section[deck]):
            section[deck][index]['question'] = new_q
            section[deck][index]['answer'] = new_a
            self.save_data()

    def delete_section(self, path):
        def recursive_delete(current, levels):
            if len(levels) == 1:
                if levels[0] in current:
                    del current[levels[0]]
            else:
                if levels[0] in current:
                    recursive_delete(current[levels[0]], levels[1:])
                    # pulizia se diventa vuoto
                    if not current[levels[0]]:
                        del current[levels[0]]
    
        levels = path.split('/')
        recursive_delete(self.sections, levels)
        self.save_data()
