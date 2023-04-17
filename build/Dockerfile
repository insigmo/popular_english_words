FROM python:3.11-alpine

ENV HOME=/app
ENV USER=english_bot
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir $HOME
RUN adduser $USER -h $HOME -S -D

USER $USER
WORKDIR $HOME

COPY ./ ./
RUN pip install --upgrade pip && pip install -r requirements.txt --no-warn-script-location

ENTRYPOINT ["python", "server.py"]
