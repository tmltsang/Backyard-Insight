#Using python
FROM python:3.10-slim
WORKDIR /root/
# Using Layered approach for the installation of requirements
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn
#Copy files to your container
COPY . ./
COPY ./assets/fonts/ .font/
#Running your APP and doing some PORT Forwarding
CMD gunicorn -b 0.0.0.0:10000 app:server
