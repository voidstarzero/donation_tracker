import os

def environment(request):
    return {
        'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
        'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
    }
