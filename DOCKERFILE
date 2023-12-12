FROM python:alpine
ADD main.py .
RUN pip3 uninstall PyCrypto
RUN pip3 install -U PyCryptodome
CMD ["python3", "./main.py"]
