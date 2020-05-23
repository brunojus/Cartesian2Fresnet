FROM python:3

ADD Cartesian2Fresnet.py /

ADD test_Cartesian2Fresnet.py /

ADD requirements.txt /

ADD reference_points.pb.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./test_Cartesian2Fresnet.py" ]