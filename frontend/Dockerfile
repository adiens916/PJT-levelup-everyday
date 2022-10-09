# https://velog.io/@nuri00/docker-compose로-react-배포하기
FROM node:16.15.0

WORKDIR /app

COPY package*.json ./
RUN npm install --force
RUN npm install -g serve

COPY . .
RUN npm run build:on-server
CMD [ "serve", "build" ]

EXPOSE 3000