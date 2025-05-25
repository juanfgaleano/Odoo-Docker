FROM odoo:17

USER root

# Instala dependencias adicionales si tienes requirements.txt
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt || echo "No hay requirements.txt"

# Copia tu archivo de configuración y módulos personalizados
COPY ./odoo.conf /etc/odoo/odoo.conf
COPY ./addons /mnt/extra-addons

# Ajusta permisos para el usuario odoo
RUN chown -R odoo:odoo /mnt/extra-addons /etc/odoo

USER odoo
