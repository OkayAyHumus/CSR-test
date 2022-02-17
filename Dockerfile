FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev 
RUN pip install opencv-python
# RUN pip3 uninstall psycopg2
RUN pip3 install psycopg2==2.8.6

ENV USER user1

RUN useradd -m ${USER}
RUN gpasswd -a ${USER} sudo
RUN echo  "${USER}:pass" | chpasswd

USER ${USER}



COPY . /code/
