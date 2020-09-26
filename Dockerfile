FROM registry.redhat.io/ubi8/python-36

# Install flask
RUN pip3 install flask

# Copy in our code
COPY src /opt/app-root/src

# Allow on the fly diags by letting our user edit the .py
RUN chmod -R g+w /opt/app-root/src

# set default flask app and environment
ENV FLASK_APP main.py

EXPOSE 5000

USER 1000

CMD flask run --host=0.0.0.0

