import json, os, re #add
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

# ДОДАНО: Клас AI для роботи з пам'яттю (JSON) та алгоритмом схожості слів
class AI:                                                                           # Оголошуємо клас AI для управління «пам'яттю» та пошуком відповідей
    def __init__(self):                                                             # Конструктор класу, який виконується при створенні об'єкта
        self.file = "brain.json"                                                    # Записуємо у змінну назву файлу, де зберігатиметься «пам'ять» ШІ
        if os.path.exists(self.file): self.load_brain()                             # Перевіряємо, чи існує файл пам'яті: якщо так — завантажуємо його
        else:                                                                       # Якщо файлу немає, створюємо базову пам'ять за замовчуванням
            self.brain = {"привіт": "Привіт! Радий тебе бачити 😊", 
                          "як справи": "У мене все добре! Я продовжую навчатися 🧠", 
                          "python": "Python — чудова мова програмування.", 
                          "kivy": "Kivy дозволяє створювати графічні застосунки."}
            self.save_brain()                                                       # Зберігаємо базовий словник у файл
    def load_brain(self):                                                           # Метод для завантаження пам'яті з JSON-файлу
        try:                                                                        # Намагаємося відкрити та прочитати файл
            with open(self.file, "r", encoding="utf-8") as file: self.brain = json.load(file)
        except: self.brain = {}                                                     # Якщо сталася помилка (файл пошкоджений), робимо словник порожнім
    def save_brain(self):                                                           # Метод для збереження поточного словника пам'яті у файл
        with open(self.file, "w", encoding="utf-8") as file: json.dump(self.brain, file, ensure_ascii=False, indent=4)
    def words(self, text):                                                          # Метод для розбиття тексту на окремі значущі слова
        text = text.lower()                                                         # Переводимо весь вхідний текст у нижній регістр
        words = re.findall(r"[а-яіїєґa-z0-9]+", text)                                # Шукаємо у тексті всі слова за допомогою регулярного виразу
        stop_words = {"і", "й", "та", "це", "що", "як", "у", "в", "на", "з", "до", "про", "мені", "ти"} # Набір непотрібних службових слів
        return set(word for word in words if word not in stop_words)                  # Повертаємо множину слів, виключаючи стоп-слова
    def similarity(self, text1, text2):                                             # Метод для обчислення схожості двох текстів
        words1, words2 = self.words(text1), self.words(text2)                       # Отримуємо множини слів для обох текстів
        if not words1 or not words2: return 0                                       # Якщо хоча б один текст не містить слів, схожість дорівнює 0
        return len(words1.intersection(words2)) / max(len(words1), len(words2))     # Рахуємо відношення спільних слів до максимальної довжини
    def get_answer(self, question):                                                 # Метод для пошуку найкращої відповіді на запитання
        best_answer, best_score = None, 0                                           # Змінні для збереження найкращої відповіді та її показника схожості
        for saved_question, answer in self.brain.items():                           # Перебираємо всі збережені питання та відповіді у пам'яті
            score = self.similarity(question, saved_question)                       # Обчислюємо схожість поточного запитання із збереженим
            if score > best_score: best_score, best_answer = score, answer          # Якщо знайдено кращий збіг, оновлюємо найкращий результат
        return (best_answer, best_score) if best_score >= 0.35 else (None, best_score) # Повертаємо відповідь, якщо схожість вище порогової (35%)
    def teach(self, question, answer):                                              # Метод для навчання ШІ — додавання нового запитання
        self.brain[question.lower()] = answer                                       # Зберігаємо у словник нове запитання (у нижньому регістрі) та відповідь
        self.save_brain()                                                           # Одразу оновлюємо (зберігаємо) файл пам'яті
#add
class ChatGPT(App):
    def build(self):
        # ДОДАНО: Ініціалізація AI та змінних для режиму навчання
        #add
        self.ai = AI()                  # Створюємо екземпляр класу AI для роботи з пам'яттю та пошуком відповідей
        self.learning_mode = None       # Змінна для відстеження етапу навчання (None означає звичайний режим)
        self.learning_question = None   # Тимчасово зберігаємо тут питання, якому зараз навчаємо ШІ
        #add
        main = BoxLayout(orientation="horizontal")
        sidebar = BoxLayout(orientation="vertical", size_hint_x=0.25, padding=10, spacing=10)
        logo = Label(text="ChatGPT", font_size=22, size_hint_y=None, height=50)
        sidebar.add_widget(logo)
        
        new_chat = Button(text="+ New chat", size_hint_y=None, height=45)
        new_chat.bind(on_press=self.new_chat)
        sidebar.add_widget(new_chat)

        # ДОДАНО: Кнопка ручного запуску навчання у сайдбарі
        #add
        teach_button = Button(text="🧠 Навчити ШІ", size_hint_y=None, height=40)
        teach_button.bind(on_press=self.start_learning)
        sidebar.add_widget(teach_button)
        #add
        for text in ["Python", "Kivy", "Навчання"]:
            chat = Button(text=text, size_hint_y=None, height=40)
            sidebar.add_widget(chat)
        sidebar.add_widget(Label())
        content = BoxLayout(orientation="vertical", padding=20)
        header = Label(text="ChatGPT", font_size=26, size_hint_y=None, height=60)
        content.add_widget(header)
        self.messages = BoxLayout(orientation="vertical", size_hint_y=None, spacing=15)
        self.messages.bind(minimum_height=self.messages.setter("height"))

        # ЗМІНЕНО: Збережено у self.scroll для керування прокруткою
        #corerct
        self.scroll = ScrollView()
        self.scroll.add_widget(self.messages)
        content.add_widget(self.scroll)
        #corerct

        bottom = BoxLayout(size_hint_y=None, height=55, spacing=10)

        self.input = TextInput(hint_text="Message ChatGPT...", multiline=False)
        # ДОДАНО: Підтримка відправки повідомлення натисканням Enter
        #add
        self.input.bind(on_text_validate=self.send_message)
        #add

        send = Button(text="➤", size_hint_x=None, width=55)
        send.bind(on_press=self.send_message)
        bottom.add_widget(self.input)
        bottom.add_widget(send)
        content.add_widget(bottom)
        main.add_widget(sidebar)
        main.add_widget(content)
        # ДОДАНО: Початкове привітальне повідомлення
        #add
        self.add_message("ChatGPT\nПривіт! Я локальний ШІ з пам'яттю 🧠")
        #add
        return main

    # ДОДАНО: Метод запуску навчання з кнопок
    #add
    def start_learning(self, instance):
        self.learning_mode = "question"
        self.learning_question = None
        self.add_message("ChatGPT\nДобре 🧠 Напиши питання, якому хочеш мене навчити.")
    #add

    def send_message(self, instance):
        text = self.input.text.strip()
        if not text: 
            return
        self.add_message("You\n" + text)
        self.input.text = ""
        #add
        if self.learning_mode == "question":                                            # Перевіряємо, чи активовано перший етап навчання (очікування запитання)
            self.learning_question, self.learning_mode = text, "answer"                 # Зберігаємо введене запитання та перемикаємо режим на очікування відповіді
            self.add_message("ChatGPT\nТепер напиши правильну відповідь на це питання.")  # Виводимо в чат прохання ввести відповідь
            return                                                                      # Завершуємо виконання методу, щоб далі коди не виконувалися
        if self.learning_mode == "answer":                                              # Перевіряємо, чи активовано другий етап навчання (очікування відповіді)
            self.ai.teach(self.learning_question, text)                                 # Передаємо збережене запитання та нову відповідь у клас AI для збереження у файл
            self.add_message("ChatGPT\nГотово! 🧠 Я запам'ятав це.")                    # Виводимо повідомлення про успішне збереження знання
            self.learning_mode, self.learning_question = None, None                     # Скидаємо режими навчання назад у початковий (звичайний) стан
            return                                                                      # Завершуємо виконання методу
        answer, score = self.ai.get_answer(text)                                        # У звичайному режимі шукаємо відповідь на запитання через інтелектуальний метод AI
        if answer:                                                                      # Перевіряємо, чи вдалося знайти відповідь у пам'яті (схожість вища за поріг)
            self.add_message(f"ChatGPT\n{answer}\n\nСхожість: {int(score * 100)}%")       # Виводимо знайдену відповідь у чат разом із відсотком схожості
        else:                                                                           # Якщо відповідь не знайдена або схожість занизька
            self.learning_question, self.learning_mode = text, "answer"                 # Запам'ятовуємо поточне запитання і переходимо в режим очікування відповіді від користувача
            self.add_message("ChatGPT\nЯ ще не знаю відповіді на це питання 🤔\nНапиши правильну відповідь, і я її запам'ятаю.") # Просимо користувача навчити бот
        #add

    def add_message(self, text):
        label = Label(text=text, size_hint_y=None, halign="left", valign="top")
        label.bind(texture_size=lambda obj, size: setattr(obj, "height", size[1] + 20)) #add
        self.messages.add_widget(label)
        # ДОДАНО: Автоматична прокрутка чату вниз
        self.scroll.scroll_y = 0

    # ЗМІНЕНО: Старий метод get_answer видалено (його замінив клас AI)

    def new_chat(self, instance):
        self.messages.clear_widgets()
        # ДОДАНО: Очищення станів навчання та виведення повідомлення
        self.learning_mode = None
        self.learning_question = None
        self.add_message("ChatGPT\nНовий чат створено 🧠")

ChatGPT().run()