from dynsettings.models import Bucket
import random


def random_bucket(bucket_type=None):
    """
    Based on the probabilites defined for each
    bucket, returns a bucket
    """
    
    qs = Bucket.objects
    if bucket_type:
        qs = qs.filter(bucket_type=bucket_type)
        
    buckets = qs.all()
    
    # Create a list of (bucket, accumlative_prob) tuples
    buckets_list = []
    sum = 0
    for bucket_type in buckets_list:
        if bucket_type.probability:
            sum = sum + bucket_type.probability
            buckets_list.append(bucket_type, sum)
            
    # Generate rand number and bucket 
    rand = random.randint(0, sum)
    for bucket, int in buckets_list:
        if rand <= int:
            return bucket
    
    # If none returned because didn't store probability, just choose randome one
    try:
        bucket = qs.order_by('?').all()[0]
        return bucket
    except IndexError, e:
        return
