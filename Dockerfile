FROM ssureymoon/docker-image-build-centos7-python34-psql94:1.2

MAINTAINER Ssuery Moon (ssureymoon@gmail.com)

# create app dir & copy project folder
RUN mkdir -p /var/www/capricorn

RUN npm cache clean

RUN npm install node-gyp@"^3.5" -g

COPY package.json /tmp/package.json

COPY . /var/www/capricorn

WORKDIR /var/www/capricorn

RUN pip3.4 install -r requirements/local.txt

EXPOSE 8000

CMD ["sh", "/var/www/capricorn/config/supervisor/run_supervisord.sh"]
