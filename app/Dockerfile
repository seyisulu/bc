FROM node:10.15.1-alpine

ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH $NPM_CONFIG_PREFIX/bin:$PATH
RUN npm i -g react-scripts

RUN mkdir /home/node/app
WORKDIR /home/node/app

COPY package.json ./
RUN npm i --no-optional
RUN mv /home/node/app/node_modules/ /home/node/

USER node
EXPOSE 3000

CMD ["npm", "start"]
