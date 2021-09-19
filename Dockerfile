FROM python:3
RUN pip install requests pymongo haversine
COPY . .
CMD [ "python", "./src/app.py" ]