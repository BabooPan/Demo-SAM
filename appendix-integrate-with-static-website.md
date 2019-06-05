## Appendix: Integrate with static website
This section walks you create a static website on S3 and how to integrate the API endpoint with it.

<p align="center">
    <img src="images/Static-website-on-s3.png">
</p>

### Before you begin

>Make sure you've created pipeline for CICD. If not, please create it first with [Run-Serverless-CICD-Pipeline-with-AWS-CodeStar-and-Develop-with-AWS-Cloud9](/README.md).

>Make the region are in US East (N. Virginia), which short name is us-east-1, or select to the right region you deployed.

## Hosting a Static Website on Amazon S3
You can host a static website on Amazon Simple Storage Service (Amazon S3). </br>
On a static website, individual webpages include static content. They might also contain client-side scripts. </br>
To host a static website, you configure an Amazon S3 bucket for website hosting, and then upload your website content to the bucket.

### Create a S3 bucket
The web page need to be stored and performed with apache server. </br>
In this case, we'll create a S3 bucket for it and also enable public access that allow outcoming request. 

* Open the [Amazon S3 console](https://console.aws.amazon.com/s3/home).
* Choose **Create Bucket**.
* For Bucket Name, type a **Unique DNS-compliant name** for your bucket.
* For Region, choose **US East(N.Virginia)**.
* Choose **Create** button on lower left side to create S3 bucket and skip details setting.
* Choose **Next** </br></br>
* On the **Configure options** page, leave it as default and choose **Next**.
> You can configure the following properties and Amazon CloudWatch metrics for the bucket. Or, you can configure these properties and CloudWatch metrics later, after you create the bucket. </br>

* On the **Set permissions** page, you manage the permissions that are set on the bucket that you are creating.
* Under **Public access settings for this bucket**, cancel the default settings that are listed under **Manage public access control lists (ACLs) for this bucket** or **Manage public bucket policies for this bucket**.

> Because of this would lead you store web page on S3, the bucket should be open to world. </br>
> Otherwise, We highly recommend that you keep the default access settings for blocking public access to the bucket that you are creating.

<p align="center">
    <img src="images/s3-enable-public-access.jpg" width="80%" height="80%">
</p>

* Choose **Next**.
* On the **Review** page, verify the settings. And then choose **Create bucket**.

### Get Web File
In this step, we'll get the webpage and modify it.

* Open the webpage file, **index.html**, in your Cloud9 environment.
* There's `httpReq.open("GET", "<YOUR_API_GATEWAY_ENDPOINT>", true);` in line 48, </br>
Please modify ***\<YOUR_API_GATEWAY_ENDPOINT\>*** to your endpoint.
> The endpoint created in [Run-Serverless-CICD-Pipeline-with-AWS-CodeStar-and-Develop-with-AWS-Cloud9](/README.md).
* Then save the file.

### Upload web page to S3 Bucket
We'll upload the web file to the S3 bucket just created via AWS CLI.

* In the Cloud9 terminal, type the command below, the command copy the file into S3 bucket.
```
aws s3 cp ~/environment/<YOUR_PROJECT_NAME>/index.html s3://<YOUR_BUCKET_NAME>
```
> Please modify both ***\<YOUR_PROJECT_NAME\>*** and ***\<YOUR_BUCKET_NAME\>*** to yours.
* Back to the S3 console, and select the bucket just created.
* Check the status of the object and exists in S3 bucket or not.


### Enable Static website hosting
Follow these steps to enable website hosting for your bucket.

* Select **Properties** tab.
* Click **Static website hosting**.
* Select **Use this bucket to host a website**.
* Type **index.html** for the index document, then click **Save**.

<p align="center">
    <img src="images/website-hosting.jpg" width="60%" height="60%">
</p>

* Verify the status of **Bucket hosting**.</br></br>

* Choose **Bucket Policy** tab in **Permissions** tab.
> When you configure a bucket as a website, you must make the objects that you want to serve publicly readable. 

* Copy below bucket policy, and paste it into the field. Make sure you have replaced **`<YOUR_BUCKET_NAME>`** with the bucket name then click **Save**.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::<YOUR_BUCKET_NAME>/*"
            ]
        }
    ]
}
```
<p align="center">
    <img src="images/bucket-policy.jpg" width="80%" height="80%">
</p>

### Access website

* Choose **Static website hosting** in **Properties** tab.
* Click the **Endpoint** on the top of window. 
> The endpoint is like ***\<YOUR_BUCKET_NAME\>.s3-website-\<REGION\>.amazonaws.com***.
* You will see the website as below:

<p align="center">
    <img src="images/website.jpg" width="60%" height="60%">
</p>

* Click **Check it out**, it would pop out alert with the response from API endpoint.

<p align="center">
    <img src="images/website-alert.jpg" width="60%" height="60%">
</p>

## Clean Up
To delete the AWS resources, perform the tasks below in order:
* Select the bucket for this tutorial in S3 console, then choose **Delete bucket**.
* In the **Delete bucket** dialog box, type the name of the bucket for confirmation, and then choose **Confirm**.

## Conclusion

Congratulations! You now have learned how to:
* Create a static website hosting through S3
* Integrate API Gateway endpoint with static website




