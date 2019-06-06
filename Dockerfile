from python:3.6-alpine
ENV PATH="/home/telepot/.local/bin:${PATH}"
ENV TOKEN="${TOKEN}"

RUN addgroup -S telepot && adduser -S telepot -G telepot && mkdir -p /usr/src && chown telepot.telepot /usr/src

USER telepot
COPY . /usr/src
RUN pip install --user --no-cache-dir -r /usr/src/requirements

CMD ["/usr/local/bin/python", "/usr/src/run.py"]
