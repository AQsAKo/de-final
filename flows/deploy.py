from prefect.deployments import Deployment

from query_gtfs_api import test_flow

local_dep = Deployment.build_from_flow(
    flow = test_flow, 
    name='deploy',  
    entrypoint="/home/final/flows/query_gtfs_api.py:test_flow")

# , schedule =(CronSchedule(cron="5 0 1 * *", timezone="America/Chicago")

if __name__=="__main__":
    """Builds the Deployment and Applies the Deployment by parameterizing the flow"""
    local_dep.apply()