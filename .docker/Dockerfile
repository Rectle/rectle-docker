FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update -y && apt-get install -y \
    xvfb
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["src/start.sh"]


# USER root
# RUN apt-get update -y && apt-get install -y \
#     xvfb \
#     python-opengl \
#     python3.6 \
#     python3-pip 

# RUN python3.6 -m pip install pip --upgrade
# RUN python3.6 -m pip install wheel

# USER ${NB_USER}
# RUN pip3 install \
#     gym \
#     pyvirtualdisplay 

# RUN conda install swig
# RUN pip3 install box2d-py atari_py pystan


