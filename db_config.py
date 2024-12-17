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
                # Логирование для отладки
                print(f"Time: {time}, Booker: {booker}")

                # Форматируем время (например, "21:00 - 22:00")
                hour, minute = map(int, time.split(':'))
                slot_time = f"{hour:02}:{minute:02} - {hour + 1:02}:{minute:02}"

                # Определяем состояние booked
                is_booked = booker is not None and booker.strip() != ""
                slots.append({
                    "time": slot_time,
                    "booked": is_booked  # True, если слот занят, False если свободен
                })

            # Возвращаем результат в формате JSON
            return json.dumps(slots)

    except sqlite3.Error as e:
        # В случае ошибки подключения или выполнения запроса
        return json.dumps({"error": f"Database error: {str(e)}"})
