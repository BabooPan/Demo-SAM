
# Bootcamp-SAM-withCloud9andCodeStar
This Section walks you through the creating CICD pipeline on AWS & development environment using AWS Cloud9. This will provide you with a cloud-based integrated development environment (IDE) that will let you write, run, debug, and deploy serverless application using just a web browser.

## Prepare the C9 & CICD environment

>Make sure your are in US East (N. Virginia), which short name is us-east-1.

#### Create project via AWS CodeStar

* Sign in to the AWS Management Console, and then open the AWS CodeStar console at https://console.aws.amazon.com/codestar/.
* On the **AWS CodeStar** page, choose **Create a new project**.</br> (If you are the first user to create a project, choose Start a project.)
* On the **Choose a project template** page, choose **Python web application with Serverless** </br> ![](images/python-web-serverless.png)
* On the **Project details** page, type a name for this project. Select **AWS CodeComit** for repository and type the name for repository. Choose **Next**.
* Review the resources and configuration details. Choose **Create Project**, and continue to setup IDE editor.

#### Launch AWS Cloud9 environment

* On the **Pick how you want to edit your code** page, choose **AWS Cloud9** and choose **Next**. 
* On the **Set up your AWS Cloud9 environment**, leave it as default and choose **Next** to complete setup. </br> ![](images/cloud9-dashboard.png)
* After environment setup, click **IDE** on left negative bar, and choose **Open IDE** to access AWS Cloud9 IDE,.

## Overview

![](images/overview-structure.png)

## Initial with lab material
```
$ git clone https://github.com/KYPan0818/Demo-SAM.git
$ cd <Your-CodeStar-Project-Name>
$ rm -rf buildspec.yml index.py README.md template.yml tests
$ cp -R ../Demo-SAM/* ./
$ git add .
$ git status
$ git commit -m "First Deploy"
$ git push
```

## Local testing via SAM CLI

#### Confirm SAM version
```
$ sam --version
```
> Update SAM version to 0.3.0 (Optional)
>> https://github.com/awslabs/aws-sam-cli#upgrade-from-version-0-2-11-or-below

#### Test a function payload locally with Lambda function
```
$ sam local invoke --template api_template/sam_demo.yml --event event.json
2018/05/12 14:56:22 Invoking index.handler (python2.7)
2018/05/12 14:56:22 Mounting /home/ec2-user/environment/Demo-SAM/api_template/LambdaFunction as /var/task:ro inside runtime container
START RequestId: 65e52f65-324d-4b05-ac40-4b5da3930b55 Version: $LATEST
END RequestId: 65e52f65-324d-4b05-ac40-4b5da3930b55
REPORT RequestId: 65e52f65-324d-4b05-ac40-4b5da3930b55 Duration: 1 ms Billed Duration: 100 ms Memory Size: 128 MB Max Memory Used: 14 MB

{"body": "{\"output\": \"Hello, this is from LambdaFunction folder.\", \"timestamp\": \"2018-05-12T14:56:23.562719\"}", "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}, "statusCode": 200}
```
#### Spawn a local API Gateway to test HTTP request and response functionality
```
$ sam local start-api --template api_template/sam_demo.yml
2018/05/12 14:57:20 Connected to Docker 1.35
2018/05/12 14:57:20 Fetching lambci/lambda:python2.7 image for python2.7 runtime...
python2.7: Pulling from lambci/lambda
Digest: sha256:d35515d2938a5b7f24cba04d0034a37ebe0288602947a0d50828638538f4ad90
Status: Image is up to date for lambci/lambda:python2.7

Mounting index.handler (python2.7) at http://127.0.0.1:3000/ [GET]
```
##### Sent HTTP request in another terminal
```
$ curl http://127.0.0.1:3000/
{"output": "Hello, this is from LambdaFunction folder.", "timestamp": "2018-05-12T14:59:26.623211"}
```

## Deploy SAM

#### Add permissions to CloudFormation Role

The role name likes “CodeStarWorker-<CODESTAR_PROJECT_NAME>-CloudFormation” </br>
Policies:
* AWSLambdaFullAccess
* IAMFullAccess
* CloudWatchFullAccess
* AWSCodeDeployFullAccess

#### Commit & push to AWS CodeCommit 
```
$ git add .
$ git commit -m "First deploy SAM"
$ git push
```

After pushing, turn on AWS CodePipeline to verify by click on "CodePipeline" URL in the "Outputs" tab of CloudFormation.

#### Test

```
$ while true; do curl -s <API_ENDPOINT>; echo; sleep 1; done
```

## Deploy SAM with Canary Deployment


#### Modify "buildspec.yml", to use another SAM model 

```
$ vim buildspec.yml
```
```
version: 0.2
phases:
  build:
    commands:
      - pip install --upgrade awscli
      - aws cloudformation package --template api_template/sam_demo_deploy.yml --s3-bucket $S3_BUCKET --output-template template-export.yml
artifacts:
  type: zip
  files:
    - template-export.yml
```

#### Edit the output string of "api_template/LambdaFunction/index.py"
```
$ vim api_template/LambdaFunction/index.py
```
```
import json
import datetime


def handler(event, context):
    data = {
        'output': 'This is new version deploy.',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
```


#### Commit & push to AWS CodeCommit 
```
$ git add .
$ git commit -m "Deploy SAM with Canary"
$ git push
```

After pushing, turn on AWS CodePipeline to verify by click on "CodePipeline" URL in the "Outputs" tab of CloudFormation.

#### Test

```
$ while true; do curl -s <API_ENDPOINT>; echo; sleep 1; done
```


## Deploy SAM with error to trigger roll back

#### Modify "buildspec.yml", to use another SAM model 

```
$ vim buildspec.yml
```
```
version: 0.2
phases:
  build:
    commands:
      - pip install --upgrade awscli
      - aws cloudformation package --template api_template/sam_demo_deploy_alarm.yml --s3-bucket $S3_BUCKET --output-template template-export.yml
artifacts:
  type: zip
  files:
    - template-export.yml
```

#### Throw except to response as error
```
$ cat api_template/LambdaFunction_error/error.py
```
#### Commit & push to AWS CodeCommit 
```
$ git add .
$ git commit -m "Deploy SAM with error to trigger roll back"
$ git push
```

After pushing, turn on AWS CodePipeline to verify by click on "CodePipeline" URL in the "Outputs" tab of CloudFormation.

#### Test

```
$ while true; do curl -s <API_ENDPOINT>; echo; sleep 1; done
```

