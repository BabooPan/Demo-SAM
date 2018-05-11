import boto3

def lambda_handler(event, context):
    print(event)
    deploymentId = event["DeploymentId"]
    lifecycleEventHookExecutionId = event["LifecycleEventHookExecutionId"]

    is_ok = True
    
    response = boto3.client('codedeploy').put_lifecycle_event_hook_execution_status(
        deploymentId=deploymentId,
        lifecycleEventHookExecutionId=lifecycleEventHookExecutionId,
        status='Succeeded' if is_ok else 'Failed'
    )  

    return response["lifecycleEventHookExecutionId"]