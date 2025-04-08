FROM python:3.11-slim



RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    libjpeg-dev \
    libpq-dev \
    gcc \
    g++ \
    git \
    curl \
    xz-utils \
    wkhtmltopdf \
    node-less \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/odoo -U -r -s /bin/bash odoo

COPY . /usr/src/odoo
WORKDIR /usr/src/odoo

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

RUN mkdir /var/lib/odoo && chown -R odoo: /var/lib/odoo

USER odoo

CMD ["./odoo-bin", "-c", "/etc/odoo/odoo.conf"]