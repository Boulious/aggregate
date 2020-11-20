
#!/usr/bin/python
# This code is for demo and learning purposes. It is not itended for any other usage! 
import awswrangler as wr
import boto3
import pandas as pd
import sys
from calendar import monthrange

def aggregateByDay(bucket,month,day):
    day_filter= lambda p: True if p["date_time"]==day else False
    df = wr.s3.read_parquet( 's3://'+bucket+'/transactiondb/transactions', partition_filter=day_filter, dataset=True)
    df.rename(columns={'account_from': 'account'}, inplace=True)   
    grouped_out = df.groupby('account').agg(amount_out=pd.NamedAgg(column='amount', aggfunc='sum'))
    df.rename(columns={'account': 'account_from','account_to': 'account'}, inplace=True)
    grouped_in = df.groupby('account').agg(amount_in=pd.NamedAgg(column='amount', aggfunc='sum'))
    grouped_all = grouped_out.join(grouped_in, how='outer').fillna(0) 
    grouped_all['balance']=grouped_all['amount_in']-grouped_all['amount_out']
    wr.s3.to_csv(df=grouped_all,path='s3://'+bucket+'/transactiondb/aggregates/'+month+'/balance_'+day+'.csv',
        dataset=True,
        mode="overwrite",
        database="transactiondb",
        table='balance_'+day)
    return grouped_all
def aggregateMonth(bucket,month):
    df = aggregateByDay(bucket, month, month+'01').drop(columns=['amount_out', 'amount_in'])
    for i in range(2,10):
        df = df.join(aggregateByDay(bucket, month, month+'0'+str(i)).drop(columns=['amount_out', 'amount_in']), how='outer', lsuffix='_x', rsuffix='_y').fillna(0) 
        df['balance']=df['balance_x']+df['balance_y']
        df.drop(columns=['balance_x', 'balance_y'], inplace=True)
    for i in range(10,monthrange(int(sys.argv[3][0:4]), int(sys.argv[3][4:6]))[1]+1):
        df = df.join(aggregateByDay(bucket, month, month+str(i)).drop(columns=['amount_out', 'amount_in']), how='outer', lsuffix='_x', rsuffix='_y').fillna(0) 
        df['balance']=df['balance_x']+df['balance_y']
        df.drop(columns=['balance_x', 'balance_y'], inplace=True)
    df.sort_values(by='balance', inplace=True, ascending=False)
    wr.s3.to_csv(df=df,path='s3://'+bucket+'/transactiondb/aggregates/'+month+'/balance.csv',
    dataset=True,
    mode="overwrite",
    database="transactiondb",
    table='balance_'+month)
def main():
    if len(sys.argv)>3:
        boto3.setup_default_session(region_name=sys.argv[1])
        bucket = sys.argv[2]
        month = sys.argv[3]
        aggregateMonth(bucket,month)
 
if __name__ == "__main__":
    main() 