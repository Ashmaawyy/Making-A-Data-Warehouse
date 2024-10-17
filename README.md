# Sparkify Data Warehouse

![Amazon Redshift]('https://cdn.freelogovectors.net/wp-content/uploads/2018/07/amazon-redshift-logo.png')

## Using Amazon Redshift I:

- Moved Database to the cloud for scalability and performance.
- Loaded Data from S3 bucket to Spark.
- Wrote database tables into HDFS.

## To run project scripts

1. Run the following command in your terminal: <br> <pre><code>pip install -r requirements.txt</code></pre>
2. Run create_tables.py to connect to the Redshift cluster and create Database tables if they don't exist, and if they exist they will be dropped and re-created. <br> WARNING: will drop tables if they exist when intiated.
3. Run etl.py to load the data to the created Database.
