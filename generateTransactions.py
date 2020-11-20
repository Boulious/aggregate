#!/usr/bin/python
# This code is for demo and learning purposes. It is not itended for any other usage! 
import pandas as pd
import awswrangler as wr
import boto3
import numpy as np
import sys
from calendar import monthrange

def generateTransactions(bucket, date, chunks):
    for i in range(chunks):
        n=2000000
        df = pd.DataFrame({'date_time': date, 'account_from': np.random.randint(1000, 9999,n), 'account_to': np.random.randint(1000, 9999,n), 'amount':np.random.randint(10, 999999,n)})
        res = wr.s3.to_parquet(
            df=df,
            path='s3://'+bucket+'/transactiondb/transactions',
            database='transactiondb',
            table='transactions',
            dataset=True,
            partition_cols=["date_time"],
            mode="append"
        )

def main(): 
    chunks=10
    if len(sys.argv)>4:
        chunks=int(sys.argv[4])
    if len(sys.argv)>3:
        boto3.setup_default_session(region_name=sys.argv[1])
        bucket = sys.argv[2]
        try:
            wr.catalog.create_database(name='transactiondb')
        except:     
            None
        
        for i in range(1,10):
            generateTransactions(bucket, sys.argv[3]+'0'+str(i), chunks)
        for i in range(10,monthrange(int(sys.argv[3][0:4]), int(sys.argv[3][4:6]))[1]+1):
            generateTransactions(bucket, sys.argv[3]+str(i), chunks)

if __name__ == "__main__":
    main()    
