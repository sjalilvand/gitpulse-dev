FROM node:20-alpine

WORKDIR /app

# تنظیم npm mirror برای دور زدن تحریم (اختیاری)
RUN npm config set registry https://registry.npmmirror.com

COPY package.json .
RUN npm install

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]