FROM --platform=linux/amd64 python:3.10.13-slim

EXPOSE 8080

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
COPY ./acptutorialpy ./acptutorialpy
ENV FLASK_APP=acptutorialpy:create_app

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080" ]

