FROM bamos/openface

RUN pip install flask jsonschema pymongo

EXPOSE 5000

COPY api.py /root/openface

CMD ["python", "-u", "/root/openface/api.py"]