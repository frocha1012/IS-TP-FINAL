# Start from the official Go image
FROM golang:1.18-alpine

# Install git, required for fetching Go dependencies.
RUN apk add --no-cache git

# Set the working directory inside the container
WORKDIR /app

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Initialize go module and install dependencies
# Assuming your main package is in a directory called "watcher"
RUN go mod init watcher && go mod tidy

# Build the Go app
RUN go build -o main .

# Command to run the executable
CMD ["./main"]
