from kivy.app import App
from kivy.uix.button import Button 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
#add
import json, os, re

class AI:
    def __init__(self):
        self.file = "brain.json"
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as file:
                self.brain = json.load(file)
        else:
            self.brain = {"привіт": "І тобі привіт! Чим я можу допомогти?"}
            with open(self.file, "w", encoding="utf-8") as file:
                json.dump(self.brain, file, ensure_ascii=False, indent=4)
    def words(self, text):
        text = text.lower()
        words = re.findall(r"[а-яіїєa-z0-9]+", text)
        stop_words = {"і", "й", "та", "це","що", "як", "у", "в"}
        result = set()
        for word in words:
            if word not in stop_words:
                result.add(word)
        return result
    def similarity(self, text1, text2):
        words1 = self.words(text1)
        words2 = self.words(text2)
        if not words1 or not words2:
            return 0
        r = len(words1.intersection(words2))/max(len(words1), len(words2))
        return r
    def get_answer(self, question):
        best_answer = None
        best_score = 0
        for saved_question , answer in self.brain.items():
            score = self.similarity(question, saved_question)
            if score > best_score:
                best_score = score
                best_answer = answer
        if best_score >= 0.35:
            return (best_answer, best_score)
        else:
            return (None, best_score)
    def teach(self, question, answer):
        self.brain[question.lower()] = answer
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(self.brain, file, ensure_ascii=False, indent=4)
#add

class ChatBoormolda(App):
    def build(self):
        #add
        self.ai = AI()
        self.learning_mode = None
        self.learning_question = None
        #add
        main = BoxLayout(orientation = "horizontal")
        sidebar = BoxLayout(orientation = "vertical", size_hint_x = 0.25, padding = 10,
                            spacing = 10)
        logo = Label(text = "ChatBoormolda", font_size = 22, size_hint_y = None, height = 50)
        sidebar.add_widget(logo)
        new_chat = Button(text = "+ New Chat", size_hint_y = None, height = 45)
        new_chat.bind(on_press = self.new_chat)
        sidebar.add_widget(new_chat)
        #add
        teach_button = Button(text = "навчити ШІ", size_hint_y = None, height = 40)
        teach_button.bind(on_press = self.start_learning)
        sidebar.add_widget(teach_button)
        #add
        for text in ["Python", "Kivy", "Навчання"]:
            chat = Button(text = text, size_hint_y = None, height = 40)
            sidebar.add_widget(chat)
        sidebar.add_widget(Label())
        content = BoxLayout(orientation = "vertical", padding = 20)
        header = Label(text = "ChatBoormolda", font_size = 26, size_hint_y = None, height = 60)
        content.add_widget(header)
        self.message = BoxLayout(orientation = "vertical", size_hint_y = None, spacing = 15)
        self.message.bind(minimum_height = self.message.setter('height'))
        #correct
        self.scroll = ScrollView()
        self.scroll.add_widget(self.message)
        content.add_widget(self.scroll)
        #correct
        bottom = BoxLayout(size_hint_y = None, height = 55, spacing = 10)
        self.input = TextInput(hint_text = "Enter your prompt...", multiline = False)
        #add
        self.input.bind(on_text_validate = self.send_message)
        #add
        send = Button(text = ">", size_hint_x =None, width = 55)
        send.bind(on_press = self.send_message)
        bottom.add_widget(self.input)
        bottom.add_widget(send)
        content.add_widget(bottom)
        main.add_widget(sidebar)
        main.add_widget(content)
        #add
        self.add_message("Boormolda\nГотов відповісти на будь-яке питання")
        #add
        return main
    #add
    def start_learning(self, instance):
        self.learning_mode = "question"
        self.learning_question = None
        self.add_message("Boormolda\n Навчи мене!")
    #add
    def send_message(self, instance):
        text = self.input.text.strip()
        if not text:
            return
        self.add_message("You\n" + text)
        self.input.text = ""
        #add
        if self.learning_mode == "question":
            self.learning_question = text
            self.learning_mode = "answer"
            self.add_message("ChatBoormolda:\nEnter correct answer")
            return
        if  self.learning_mode == "answer":
            self.ai.teach(self.learning_question, text)
            self.add_message("ChatBoormolda:\nI got it! 👌")
            self.learning_question = None
            self.learning_mode = None
            return
        answer , score = self.ai.get_answer(text)
        if answer:
            self.add_message(f"ChatBoormolda:\n{answer}\nVitsotok:{int(score*100)}%")
        else:
            self.learning_question = text
            self.learning_mode = "answer"
            self.add_message("ChatBoormolda:\nI don`t know\nEnter correct answer")
        #add
    def add_message(self, text):
        label = Label(text = text, size_hint_y = None, halign = "left", valign = "top")
        self.message.add_widget(label)
        #add
        self.scroll.scroll_y = 0
        #add

    # get_answer ВИДАЛЯЄМО

    def new_chat(self, instance):
        self.message.clear_widgets()
        #add
        self.learning_mode = None
        self.learning_question = None
        self.add_message("Boormolda\nНовий чат створенно")
        #add
ChatBoormolda().run()