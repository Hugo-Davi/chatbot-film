import customtkinter as ctk
import spacy
from difflib import SequenceMatcher

# Carregar o modelo de português
nlp = spacy.load('pt_core_news_sm')

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Snob Roboto")
        master.geometry("600x500")

        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)

        ctk.set_appearance_mode("light")  # "light" ou "dark"
        ctk.set_default_color_theme("dark-blue")

        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=500, height=300, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Saudações! Eu sou o Snob Roboto, sua central para recomendação de filmes. Insira um tema de filme para eu recomendar.\n")
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite sua pergunta aqui...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

        # Dados da tabela
        self.table_data = {
            'nome': ['Poderoso Chefão', 'Persona', 'Vá e Veja', 'Antes do Amanhecer', 'Meu Amigo Totoro', 'Pagador de Promessas 1962', 'Possessão 1981'],    
            'tema': ['mafia', 'psicologico', 'guerra', 'romance', 'infantil', 'nacional', 'terror']
        }

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Você: " + user_input + "\n")

        response = self.get_bot_response(user_input)
        self.text_area.insert(ctk.END, "Snob Roboto: " + response + "\n")

        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)

    def get_bot_response(self, user_input):
        # Processar o input com spaCy
        doc = nlp(user_input.lower())
        # Extrair tokens lematizados sem pontuações e palavras de parada
        tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]

        # Tentar encontrar uma correspondência com as colunas
        for index, data in enumerate(self.table_data["tema"]):
            # comparar temas com token
            for token in tokens:
                similarity = self.similarity(token, data)
                if similarity > 0.7:
                    response = f"Eu recomendo: {self.table_data["nome"][index]}"
                    return response
                
        if any(greeting in tokens for greeting in ["olá", "oi"]):
            return "Olá! Eu venho à Terra em paz"
        elif any(farewell in tokens for farewell in ["tchau", "adeus", "até logo"]):
            return "Até mais! Se precisar de algo, estou aqui."
        elif "ajuda" in tokens or "socorro" in tokens:
            return "Claro! Qual tema de filme você quer ver?"
        else:
            return "Desculpe, não entendi. Poderia reformular a pergunta?"

    def similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":
        root = ctk.CTk()
        chatbot = Chatbot(root)
        root.mainloop()