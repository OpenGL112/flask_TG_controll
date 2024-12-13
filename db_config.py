import sqlite3
import json

DATABASE = f"/instance/test.db"

import sqlite3
import json

DATABASE = f"/instance/test.db"


# Функция для получения доступных слотов (синхронная версия)
def get_available_slots(date):
    try:
        # Подключаемся к базе данных
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT time, booker FROM slots WHERE date = ? 
            """, (date,))

            rows = cursor.fetchall()

            # Формируем список слотов с нужным форматом времени и состоянием booked как True/False
            slots = []
            for time, booker in rows:
                # Форматируем время, если это необходимо (например, "21:00 - 22:00")
                # Предположим, что в поле `time` у вас уже хранится нужный формат, например, '21:00'
                slot_time = f"{time} - {str(int(time.split(':')[0]) + 1)}:{time.split(':')[1]}"

                # Добавляем слот в список с состоянием booked
                slots.append({
                    "time": slot_time,
                    "booked": bool(booker)  # True, если слот занят, False если свободен
                })

            # Возвращаем результат в формате JSON
            return json.dumps(slots)

    except sqlite3.Error as e:
        # В случае ошибки подключения или выполнения запроса
        return json.dumps({"error": f"Database error: {str(e)}"})
