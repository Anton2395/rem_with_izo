# FROM node:lts-slim
# FROM node:latest
FROM node:14.15.4
WORKDIR /code
# ADD package.json .
# RUN npm install 
ADD . .
# RUN npm run build && npm run generate
EXPOSE 8011
# ENTRYPOINT "npm" "run" "start"