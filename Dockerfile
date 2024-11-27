FROM python:3.10
EXPOSE 8443
WORKDIR /app
COPY requirements.txt .
# RUN pip install flask
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]