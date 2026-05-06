import tkinter as tk
import json
import os

# --- Настройки ---
DATA_FILE = "movies.json" # Файл, где будут храниться фильмы

# --- Глобальные переменные ---
movies = [] # Список всех фильмов
current_filter_genre = "" # Текущий фильтр по жанру
current_filter_year = ""   # Текущий фильтр по году

# --- Работа с файлом JSON ---
def load_data():
    """Загружает фильмы из файла при запуске."""
    global movies
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                movies = json.load(f)
        except Exception as e:
            print("Ошибка чтения файла:", e)
            movies = []
    else:
        print("Файл данных не найден. Будет создан новый.")

def save_data():
    """Сохраняет список фильмов в файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

# --- Проверка введенных данных (Валидация) ---
def is_valid_year(year_str):
    """Проверяет, что год — это число в разумном диапазоне."""
    try:
        year = int(year_str)
        return 1890 < year < 2030
    except ValueError:
        return False

def is_valid_rating(rating_str):
    """Проверяет, что рейтинг — это число от 0 до 10."""
    try:
        rating = float(rating_str)
        return 0 <= rating <= 10
    except ValueError:
        return False

# --- Обновление списка на экране (Вывод в таблицу) ---
def update_listbox_display():
    """
    Очищает список и выводит фильмы в виде таблицы с ровными столбцами.
    """
    movie_listbox.delete(0, tk.END)
    
    filtered_movies = filter_movies()
    
    if not filtered_movies:
        movie_listbox.insert(tk.END, "--- Фильмов не найдено ---")
        return

    # Ширина столбцов для красивого вывода
    title_width = 35
    genre_width = 15
    year_width = 6
    rating_width = 10

    # Заголовок таблицы
    header = f"{'Название':<{title_width}} | {'Жанр':<{genre_width}} | {'Год':>{year_width}} | {'Рейтинг':>{rating_width}}"
    movie_listbox.insert(tk.END, header)
    
    # Разделительная линия
    separator = "-" * (title_width + genre_width + year_width + rating_width + 7)
    movie_listbox.insert(tk.END, separator)

    # Выводим каждый фильм
    for m in filtered_movies:
        title = (m['title'][:title_width-2] + '..') if len(m['title']) > title_width else m['title']
        genre = (m['genre'][:genre_width-2] + '..') if len(m['genre']) > genre_width else m['genre']

        line = f"{title:<{title_width}} | {genre:<{genre_width}} | {m['year']:>{year_width}} | {m['rating']:>{rating_width}.1f}"
        movie_listbox.insert(tk.END, line)

# --- Логика фильтрации ---
def filter_movies():
    """
    Возвращает список фильмов, отфильтрованный по жанру и/или году.
    """
    filtered = movies.copy()
    
    # Фильтр по жанру
    if current_filter_genre:
        filtered = [m for m in filtered if current_filter_genre.lower() in m["genre"].lower()]
    
    # Фильтр по году
    if current_filter_year.isdigit():
        year_int = int(current_filter_year)
        filtered = [m for m in filtered if m["year"] == year_int]
    
    return filtered

# --- Логика добавления фильма ---
def add_movie():
    """Берем данные из полей, проверяем их и добавляем в список."""
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()
    
    # Проверка: все ли поля заполнены?
    if not (title and genre and year and rating):
        print("Ошибка: Заполните все поля!")
        return
    
    # Проверка: Корректный ли год?
    if not is_valid_year(year):
        print("Ошибка: Год должен быть числом (например, 2010)!")
        return
    
    # Проверка: Корректный ли рейтинг?
    if not is_valid_rating(rating):
        print("Ошибка: Рейтинг должен быть числом от 0 до 10!")
        return

    # Если всё верно — добавляем фильм в список
    new_movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": float(rating)
    }
    
    movies.append(new_movie)
    
    # Сохраняем в файл и обновляем экран
    save_data()
    update_listbox_display()
    
    # Очищаем поля ввода для следующего фильма
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

# --- Логика применения фильтров ---
def apply_filters():
    """Берем текст из полей фильтра и обновляем список."""
    global current_filter_genre, current_filter_year
    
    current_filter_genre = filter_genre_entry.get()
    current_filter_year = filter_year_entry.get()
    
    update_listbox_display()

def reset_filters():
    """Очищаем поля фильтра и сбрасываем глобальные переменные."""
    global current_filter_genre, current_filter_year
    
    current_filter_genre = ""
    current_filter_year = ""
    
    filter_genre_entry.delete(0, tk.END)
    filter_year_entry.delete(0, tk.END)
    
    update_listbox_display()


# --- Главная часть: создание окна и виджетов ---
if __name__ == "__main__":

     # Создаем главное окно программы
     root = tk.Tk()
     root.title("Movie Library")
     
     # Загружаем сохраненные фильмы из файла (если они есть)
     load_data()


     # --- Блок 1: Поля для ввода нового фильма ---
     input_frame = tk.Frame(root)
     input_frame.pack(padx=10, pady=10, fill="x")
     
     tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="e", pady=2)
     title_entry = tk.Entry(input_frame)
     title_entry.grid(row=0, column=1, sticky="we", padx=2, pady=2)
     
     tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="e", pady=2)
     genre_entry = tk.Entry(input_frame)
     genre_entry.grid(row=1, column=1, sticky="we", padx=2, pady=2)
     
     tk.Label(input_frame, text="Год:").grid(row=2, column=0, sticky="e", pady=2)
     year_entry = tk.Entry(input_frame)
     year_entry.grid(row=2, column=1, sticky="we", padx=2, pady=2)
     
     tk.Label(input_frame, text="Рейтинг:").grid(row=3, column=0, sticky="e", pady=2)
     rating_entry = tk.Entry(input_frame)
     rating_entry.grid(row=3, column=1, sticky="we", padx=2, pady=2)
     
     input_frame.columnconfigure(1, weight=1) # Делаем поле ввода растянутым


     # --- Блок 2: Кнопка "Добавить фильм" ---
     button_frame = tk.Frame(root)
     button_frame.pack(pady=5, fill="x")
     
     add_button = tk.Button(button_frame, text="Добавить фильм", command=add_movie)
     add_button.pack(side="left", padx=5)


     # --- Блок 3: Поля для фильтрации ---
     filter_frame = tk.Frame(root)
     filter_frame.pack(pady=5, fill="x")
     
     tk.Label(filter_frame, text="Жанр:").pack(side="left")
     filter_genre_entry = tk.Entry(filter_frame)
     filter_genre_entry.pack(side="left", padx=2)
     
     tk.Label(filter_frame, text="Год:").pack(side="left")
     filter_year_entry = tk.Entry(filter_frame)
     filter_year_entry.pack(side="left", padx=2)
     
     apply_btn = tk.Button(filter_frame, text="Применить", command=apply_filters)
     apply_btn.pack(side="left", padx=5)
     
     reset_btn = tk.Button(filter_frame, text="Сбросить", command=reset_filters)
     reset_btn.pack(side="left")


      # --- Блок 4: Список для вывода фильмов (Таблица) ---
     list_frame = tk.Frame(root)
     list_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True) 
      
     movie_listbox = tk.Listbox(list_frame) 
     movie_listbox.pack(side="left", fill="both", expand=True)
      
     scrollbar = tk.Scrollbar(list_frame)
     scrollbar.pack(side="right", fill="y")
      
     movie_listbox.config(yscrollcommand=scrollbar.set)
     scrollbar.config(command=movie_listbox.yview)


      # Выводим фильмы при запуске программы
     update_listbox_display()


     root.mainloop()
