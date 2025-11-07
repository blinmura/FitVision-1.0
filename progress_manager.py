import json
import os

class ProgressManager:
    PROGRESS_FILE = "progress.json"
    ACCOUNTS_FILE = "accounts.json"

    @staticmethod
    def get_current_user():
        """Имя последнего вошедшего пользователя из accounts.json"""
        if os.path.exists(ProgressManager.ACCOUNTS_FILE):
            try:
                with open(ProgressManager.ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("last_logged_in", "guest")
            except json.JSONDecodeError:
                return "guest"
        return "guest"

    @staticmethod
    def load_progress():
        """Возвращает dict прогресса только для текущего пользователя."""
        user = ProgressManager.get_current_user()
        if os.path.exists(ProgressManager.PROGRESS_FILE):
            try:
                with open(ProgressManager.PROGRESS_FILE, "r", encoding="utf-8") as file:
                    all_progress = json.load(file)
                    if not isinstance(all_progress, dict):
                        all_progress = {}
            except json.JSONDecodeError:
                all_progress = {}
        else:
            all_progress = {}
        return all_progress.get(user, {})

    @staticmethod
    def save_progress(exercise_name, count):
        """Сохраняет count для exercise_name текущего пользователя."""
        user = ProgressManager.get_current_user()
        # load global
        if os.path.exists(ProgressManager.PROGRESS_FILE):
            try:
                with open(ProgressManager.PROGRESS_FILE, "r", encoding="utf-8") as file:
                    all_progress = json.load(file)
                    if not isinstance(all_progress, dict):
                        all_progress = {}
            except json.JSONDecodeError:
                all_progress = {}
        else:
            all_progress = {}

        # ensure user dict
        if user not in all_progress or not isinstance(all_progress[user], dict):
            all_progress[user] = {}

        all_progress[user][exercise_name] = count

        with open(ProgressManager.PROGRESS_FILE, "w", encoding="utf-8") as file:
            json.dump(all_progress, file, indent=4, ensure_ascii=False)

    @staticmethod
    def reset_user_progress():
        """Обнуляет прогресс текущего пользователя (удаляет все упражн. значения)."""
        user = ProgressManager.get_current_user()
        if os.path.exists(ProgressManager.PROGRESS_FILE):
            try:
                with open(ProgressManager.PROGRESS_FILE, "r", encoding="utf-8") as file:
                    all_progress = json.load(file)
                    if not isinstance(all_progress, dict):
                        all_progress = {}
            except json.JSONDecodeError:
                all_progress = {}
        else:
            all_progress = {}

        all_progress[user] = {}
        with open(ProgressManager.PROGRESS_FILE, "w", encoding="utf-8") as file:
            json.dump(all_progress, file, indent=4, ensure_ascii=False)
