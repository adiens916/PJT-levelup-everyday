FROM python:3.10.4

WORKDIR /app/

# Copy package list from context folder to image
ADD requirements.txt /app/
# Install packages
RUN pip install -r requirements.txt
# Copy other files
ADD . /app/

# (Optional) Remove stdout delay
ENV PYTHONUNBUFFERED 0