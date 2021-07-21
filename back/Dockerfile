FROM python
WORKDIR /app
COPY start.sh /app
COPY app.py /app
COPY requirements.txt /app
ADD src /app/src
ADD log /app/log
ADD test /app/test
RUN mkdir -p /log
EXPOSE 3001
EXPOSE 3002
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/bash"]
CMD ["start.sh"]
