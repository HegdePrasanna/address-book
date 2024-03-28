FROM python:3.12

# COPY ./requirements.txt /opt/addressbook/requirements.txt
COPY . /opt/addressbook/

WORKDIR /opt/addressbook

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]