FROM node:20-alpine

WORKDIR /app

COPY package.json postcss.config.js tailwind.config.js vite.config.js ./
COPY index.html ./
COPY src ./src

RUN npm install && npm run build

RUN npm install -g serve

EXPOSE 3000
CMD ["serve", "-s", "dist"]
