cd front
cmd /c "npm run build"
docker build -t front .
docker stop front & docker rm front & docker run --name front -p 80:80 front