FROM python:3.10-slim

COPY poetry.lock pyproject.toml README.md /working/

WORKDIR /working

RUN apt-get update \
    && apt-get upgrade -yq \
    && pip install pip poetry --upgrade \
    && rm -f /etc/localtime \
    && ln -s /usr/share/zoneinfo/America/New_York /etc/localtime \
    && poetry install \
    && rm -rf /tmp/* \
    && rm -rf /var/cache/apt/* \
    && rm -rf /var/tmp/*

ENTRYPOINT ["poetry", "run"]

CMD ["bash"]
