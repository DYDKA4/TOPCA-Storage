

#RUN wget https://github.com/tliron/puccini/releases/download/v0.21.0/puccini_0.21.0_linux_amd64.tar.gz  \
#    && mkdir -p /home/tulin/go/bin/ && tar -xf puccini_0.21.0_linux_amd64.tar.gz -C /home/tulin/go/bin/ && \
#    rm puccini_0.21.0_linux_amd64.tar.gz && apt update && apt install glibc-source -y

FROM golang:1.20 AS puccini

WORKDIR /usr/src/app
RUN wget https://github.com/tliron/puccini/archive/refs/tags/v0.21.0.tar.gz
RUN tar -xf v0.21.0.tar.gz
RUN rm v0.21.0.tar.gz
RUN ls
RUN /usr/src/app/puccini-0.21.0/scripts/build


FROM python:3.10.6

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY --from=puccini /go/bin/ .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD ["python", "main.py"]