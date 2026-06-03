FROM python:3.12-slim

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /App
COPY App ./App

EXPOSE 5000

CMD [ "python", "App/App.py" ]