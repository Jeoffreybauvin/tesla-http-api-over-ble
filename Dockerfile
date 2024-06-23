FROM --platform=${BUILDPLATFORM:-linux/amd64} python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY *.py /code
EXPOSE 8000
CMD ["fastapi", "run", "main.py"]