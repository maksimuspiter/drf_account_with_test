FROM node:16.13.0-alpine3.11 as build-stage
WORKDIR /app/
COPY project/frontend/package.json /app/
RUN npm cache verify
RUN npm install
COPY project/frontend /app/
RUN npm run build

# prod
FROM nginx:latest as production-stage

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist /dist/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]