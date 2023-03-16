FROM spark-master as spark-worker

ENV SPARK_WORKLOAD="worker"

CMD /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker $SPARK_MASTER
