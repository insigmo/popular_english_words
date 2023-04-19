FROM python:3.11-alpine

ENV HOME=/app
ENV USER=english_bot
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir $HOME
RUN adduser $USER -h $HOME -S -D

RUN pip install supervisor --no-warn-script-location

WORKDIR $HOME
ENV PYTHONPATH=$HOME

COPY ./ /app/
RUN pip install --upgrade pip  --no-warn-script-location && pip install -r requirements.txt --no-warn-script-location

COPY build/supervisord/supervisord.conf /etc/supervisor/supervisord.conf
RUN echo_supervisord_conf >> /etc/supervisor/supervisord.conf

ENTRYPOINT ["supervisord", "--nodaemon"]
