FROM apache/airflow:2.7.1-python3.10

# Рабочая директория
WORKDIR /opt/airflow

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем DAGи, плагины и src
COPY airflow/dags/ ./dags/
COPY airflow/plugins/ ./plugins/
COPY src/ ./src/

# Копируем конфиг airflow.cfg, если нужно
COPY airflow/config/airflow.cfg ./airflow.cfg

# Устанавливаем переменные окружения (пример)
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# При необходимости копируем скрипт запуска (например airflow.sh)
COPY airflow/airflow.sh ./airflow.sh
RUN chmod +x ./airflow.sh

# Команда запуска (если нужна кастомная)
CMD ["./airflow.sh"]