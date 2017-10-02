FROM bamos/openface

RUN pip install flask jsonschema

EXPOSE 5000

COPY api.py /root/openface

CMD python /root/openface/api.py