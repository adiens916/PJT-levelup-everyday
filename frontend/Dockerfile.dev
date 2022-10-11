# https://velog.io/@nuri00/docker-compose로-react-배포하기
FROM node:16.15.0

WORKDIR /app

COPY package*.json ./
RUN npm install --force

COPY . .
CMD [ "npm", "start" ]

EXPOSE 3000