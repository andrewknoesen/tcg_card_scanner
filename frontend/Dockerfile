# Stage 1: Build the React app
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Production environment
FROM nginx:alpine

# Copy the production build from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for nginx
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
