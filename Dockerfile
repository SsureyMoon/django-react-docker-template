FROM ssureymoon/docker-image-build-centos7-python34-psql94:1.2

MAINTAINER Ssuery Moon (ssureymoon@gmail.com)

# create app dir & copy project folder
RUN mkdir -p /var/www/appserver

RUN npm cache clean

RUN npm install node-gyp@"^3.5" -g

COPY package.json /tmp/package.json

COPY . /var/www/appserver

WORKDIR /var/www/appserver

RUN pip3.4 install -r requirements/local.txt

EXPOSE 8000

CMD ["sh", "/var/www/appserver/config/supervisor/run_supervisord.sh"]
