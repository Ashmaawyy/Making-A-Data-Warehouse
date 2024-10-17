# Sparkify Data Warehouse

![Amazon Redshift]('https://th.bing.com/th/id/R.5f935c319dd0a1cadc49bf9a01733152?rik=CxQEjmU82z4pWQ&riu=http%3a%2f%2fwww.freelogovectors.net%2fwp-content%2fuploads%2f2018%2f07%2famazon-redshift-logo-900x351.png&ehk=Vppdgci2dKP9%2fAXpwwB6KyyHuCiAiMNf1CB9mVEFr%2bI%3d&risl=&pid=ImgRaw&r=0')

## Using Amazon Redshift I:

- Moved Database to the cloud for scalability and performance.
- Loaded Data from S3 bucket to Spark.
- Wrote database tables into HDFS.

## To run project scripts

1. Run the following command in your terminal: <br> <pre><code>pip install -r requirements.txt</code></pre>
2. Run create_tables.py to connect to the Redshift cluster and create Database tables if they don't exist, and if they exist they will be dropped and re-created. <br> WARNING: will drop tables if they exist when intiated.
3. Run etl.py to load the data to the created Database.
