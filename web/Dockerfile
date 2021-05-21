# FROM node:lts-slim
# FROM node:latest
FROM node:14.15.4
# ENV \
    # # BASE_URL=http://172.17.0.1:50001    \
    # PORT=3000                           \
    # HOST=0.0.0.0                        \
    # TITLE="MVLAB-DEBUG"
WORKDIR /code
COPY . .

RUN \
        npm install &&  npm run build && npm run generate

EXPOSE 8011

# ENTRYPOINT "npm" "run" "start"