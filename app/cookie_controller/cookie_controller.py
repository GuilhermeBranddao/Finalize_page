import os
import json
from pathlib import Path
import streamlit as st

from app.utils.constants import COOKIE_SECRET
import random
# from streamlit_cookies_controller import CookieController as cookie_controller
import requests
# controller = cookie_controller()

session = requests.Session()

# class CookieController:
#     def __init__(self):
#         pass

#     def set(self, name, value):
#         """Define um cookie com o nome e valor especificados."""
#         # controller.set(name, value)
#         session.cookies.set(name, value)

#     def get(self, name):
#         """Obtém o valor de um cookie pelo nome."""
#         # return controller.get(name)
#         return session.cookies.get(name)

#     def remove(self, name):
#         """Remove um cookie pelo nome."""
#         # controller.remove(name)

#     def getAll(self):
#         """Retorna todos os cookies."""
#         # self.refresh()
        # return self.cookies


class CookieController:
    def __init__(self, filepath=Path("app/data/cookie.json")):
        self.filepath = filepath
        self._ensure_directory_exists()
        self.refresh()
        

    def refresh(self):
        self.cookies = self._load_cookies()

    def _ensure_directory_exists(self):
        """Garante que o diretório do arquivo exista."""
        directory = os.path.dirname(self.filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _load_cookies(self):
        """Carrega os cookies do arquivo local, se existir."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as file:
                    cookies = json.load(file)
                    print(f"Cookies carregados")  # Para depuração
                    return cookies
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Erro ao carregar cookies: {e}")  # Para depuração
                return {}  # Retorna um dicionário vazio caso ocorra um erro
        return {}

    def _save_cookies(self):
        """Salva os cookies no arquivo local."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as file:
            json.dump(self.cookies, file, indent=4)  # Usando json para salvar
            print(f"Cookies salvos: {self.cookies}")  # Para depuração

    def set(self, name, value):
        """Define um cookie com o nome e valor especificados."""
        self.cookies[name] = value
        self._save_cookies()
        self.refresh()

    def get(self, name):
        """Obtém o valor de um cookie pelo nome."""
        self.refresh()
        return self.cookies.get(name, None)

    def remove(self, name):
        """Remove um cookie pelo nome."""
        if name in self.cookies:
            del self.cookies[name]
            self._save_cookies()
            self.refresh()
            print(f"Cookie '{name}' removido.")  # Para depuração
        else:
            print(f"Cookie '{name}' não encontrado.")  # Para depuração

    def getAll(self):
        """Retorna todos os cookies."""
        self.refresh()
        return self.cookies
