FROM python:3.13-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8501

EXPOSE 8501

CMD ["streamlit", "run", "_👋_Accueil.py"]