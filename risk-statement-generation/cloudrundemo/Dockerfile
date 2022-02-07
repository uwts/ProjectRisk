FROM python:3.7

ENV APP_HOME /app
WORKDIR $APP_HOME

#RUN apk add --no-cache build-base libffi libffi-dev && pip install cffi
RUN pip install Flask requests gevent nltk gunicorn transformers
#RUN pip install -r requirements.txt
RUN pip install torch==1.8.0+cpu torchvision==0.9.0+cpu torchaudio===0.8.0 -f https://download.pytorch.org/whl/torch_stable.html
COPY . $APP_HOME

# prevent libreoffice from querying ::1 (ipv6 ::1 is rejected until istio 1.1)
#RUN mkdir -p /etc/cups && echo "ServerName 127.0.0.1" > /etc/cups/client.conf

#Old command (replaced with gunicorn)
#CMD ["python", "to-pdf.py"]

CMD gunicorn --timeout 1000 --bind :$PORT app:app
