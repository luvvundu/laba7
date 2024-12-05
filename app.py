from flask import Flask, request, jsonify
from flask_limiter import Limiter
import json
import os

app = Flask(__name__)
limiter = Limiter(app)

DATA_FILE = 'data.json'

# функция для загрузки данных из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# функция для сохранения данных в файл
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        # сохранение содержимого переданного словаря в файл
        json.dump(data, f)

# загрузка данных при старте приложения
data = load_data()

# сохранение ключ-значение
@app.route('/set', methods=['POST'])
@limiter.limit("10/minute")
def set_value():
    # получаем значения key и value из JSON тела запроса
    key = request.json.get('key')
    value = request.json.get('value')
    if key is None or value is None:
        return jsonify({"error": "Ключ и значение обязательны"}), 400
    # сохранение полученного значения в словаре data под указанным ключом
    data[key] = value
    # отправка обновленных данных в файл
    save_data(data)
    return jsonify({"message": "Ключ-значение успешно сохранены! Ура!"}), 201

# получение значения по ключу
@app.route('/get/<key>', methods=['GET'])
@limiter.limit("100/day")
def get_value(key):
    # поиск значение по переданному ключу
    value = data.get(key)
    if value is None:
        return jsonify({"error": "Ключ не найден"}), 404
    return jsonify({"key": key, "value": value}), 200

# удаление ключа
@app.route('/delete/<key>', methods=['DELETE'])
@limiter.limit("10/minute")
def delete_value(key):
    # проверка наличия ключа в словаре data
    if key in data:
        del data[key]
        save_data(data)
        return jsonify({"message": "Ключ удален"}), 200
    return jsonify({"error": "Ключ не найден"}), 404

# проверка наличия ключа
@app.route('/exists/<key>', methods=['GET'])
@limiter.limit("100/day")
def exists_value(key):
    # проверка существования ключа в словаре
    exists = key in data
    return jsonify({"exists": exists}), 200

if __name__ == '__main__':
    app.run(debug=True)





