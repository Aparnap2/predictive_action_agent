FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

# Copy source code
COPY . .

# Expose port
EXPOSE 5173

# Run the application
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
