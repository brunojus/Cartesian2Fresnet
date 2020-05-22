FROM python:3

ADD Cartesian2Fresnet.py /

ADD requirements.txt /

ADD reference_points.pb.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./Cartesian2Fresnet.py" ]