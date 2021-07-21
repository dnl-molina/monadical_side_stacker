cd back
docker build -t back .
docker stop back & docker rm back & docker run --name back -p 3001:3001 -p 3002:3002 back