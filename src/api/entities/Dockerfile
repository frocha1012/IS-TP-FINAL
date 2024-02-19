FROM node:21-alpine3.17

WORKDIR /usr/src/app

# Install Bash and Update npm
RUN apk add bash
RUN npm update npm -g

# Install global npm packages
RUN npm install nodemon -g
RUN npm install knex -g

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Generate Prisma client
RUN npx prisma generate

# Copy the rest of your application's source code
COPY . .

# Set the command to run your script
CMD (sed -i 's/\r$//' ./run.sh) ; (chmod +x ./run.sh) ; ./run.sh
