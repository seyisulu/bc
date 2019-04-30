FROM python:3.7.2-alpine3.9

RUN mkdir /code
WORKDIR /code
RUN apk add --no-cache nodejs nodejs-npm

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
ENV PROJECT "britecore"

COPY . .
RUN python manage.py collectstatic
RUN python manage.py makemigrations --noinput --merge
RUN python manage.py migrate --noinput
RUN python manage.py initadmin

EXPOSE 8000

HEALTHCHECK --interval=5m --timeout=3s --start-period=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8000/health || exit 1
ENTRYPOINT ["./scripts/serve.sh"]
