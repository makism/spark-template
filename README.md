
# ETL

You could run some of the parts like

```bash
docker exec -it spark-master /bin/python3 /opt/etl/template/raw/compute.py
```

## Tests

```bash
docker exec -it spark-master /usr/local/bin/pytest -v /opt/etl_tests
```

