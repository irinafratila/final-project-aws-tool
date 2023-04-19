Link to access the website: http://auditing-report-tool.s3-website-us-east-1.amazonaws.com/ 

1. Folder python-scripts-from-awsLambda: 
Contains the two Python scripts which are executed serverless-ly by AWS's service Lambda.   
    1.1. File: python-scripts-from-awsLambda/auditingtool-updateInstancesAndImagesBuckets.py  
    A Python script which keeps the data in storage up to date. It uses the library Boto3 to get all necessary data about running machine instances and         images and stores it in two separate S3 buckets. With every execution, the data is deleted and re-written in storage to keep it fresh.   
    
    1.2. File: python-scripts-from-awsLambda/website-request-handler.py  
    The script that is triggered when a request comes through the API from the website. Using the library Boto3 it will invoke the script above () to 
    update the data in storage, get the data from each S3 bucket, format it accordingly to a JSON object, and send it back though the API to be displayed       on the webiste. 

2. Folder web-app:
Has the two client-side scripts needed to implement the website.   
    2.1. File: web-app/index.html  
    HTML script which builds the webisite interface(two tables, search bar, title etc.). With every page refresh, a call to the API
    is made, data is obtained, formatted, and displayed in two separate tables. JQuery is used to implement real-time
    search functionality and sorting of the data. Bootstrap is also used to style the website. 
    
    2.2. File: web-app/script.js  
    The JavaScript file which implements the functionality of the website. This includes populating the table with data,
    sorting dates in an ascending or descending order, using the moment libray to classify items older or younger than 30, and more. 
  
