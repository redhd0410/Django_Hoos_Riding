# docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/spark.py

print("Begin Spark")
from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")
data = sc.textFile("/tmp/data/access.log", 2)    

# Read data in as pairs of (user_id, item_id clicked on by the user)
pairs = data.map(lambda line: line.split("\t"))   
pages = pairs.map(lambda pair: (pair[0], 1))     

# Distinct pairs
distinct = pairs.distinct()
distinct_output = distinct.collect()

for user, page_id in output:
    print ("user %s page_id %d" % (user, page_id))
print ("Distinct pairs done")

# Group data into (user_id, list of item ids they clicked on)
grouped = pages.groupByKey()

# Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
transform1 = grouped.map(lambda x: (x[0], list(x[1])))

output = transform1.collect()             
for user, items in output:
    print ("user %s items %d" % (user, items))
print ("Transform 1 done")

# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
distinct_grouped = distinct.groupByKey()
transform3 = grouped.map(lambda x: (x[0], len(x[1])))

# Filter out any results where less than 3 users co-clicked the same pair of items
