# 1. Project Overview

## A Video Demo

[link to video demo!](https://youtu.be/Z7kAxq_26Ik)

## Why we have chosen github?

The reason why we have chosen github is not just because of how reputable it is. In fact, one of the main reasons why we have picked github is because of how easy it is for the public to contribute to our project. Github offers a wiki as well as a issues tracker that would make it easier for us to include a more indepth documentation and gather feedback for our project. Not only so, github is not just a website for documentations and instructions, however, a repository, which means that it would allow us to keep updating ,make changes or improve our project easily. Additionally, github is widely supported by numerous services and operating systems, demonstrating great versatility. 

## What have we uploaded?

We have uploaded all the source codes required for our project, as well as a clear and concise documentation on how our project functions as well as how any user can replicate our project if they intend to do so. A diagram on how a user should position their raspberry pis outside their house will also be provided if the user wishes to fully replicate our project.

## What is the application about?

Nowadays, there is a trend that most of us would invest in high-end sneakers or shoes. Because of their high prices, we would be afraid to leave them unguarded, therefore bring them into the house. However, it is a chore to clean the shoes so that we do not dirty our house each time we bring it in. As such, our application intends to solve this. Our application will provide a form of security for your shoes, as well as implement a gate security that is convenient for both guests and home owners.  

## Summary

1. Overview (*Project introduction*)
2. Hardware requirements (*Hardware required for this project*)
3. Hardware Set-up (*Set-up that hardware required for the project*)
4. Application Prerequisites (*All packages or directories that are needed for this project.*)
5. AWS IoT Core (MQTT) (*Set-up Amazon Web Service IoTcore*)
6. AWS DynamoDB (*Set-up Amazon Web Service NoSQL DynamoDB*)
7. AWS S3 (*Set-up Amazon Web Service Image Repository S3*)
8. Telegram Bot (*Set-up Telegram Bot*)
9. OpenCV Facial Recognition (*Set-up OpenCV Facial Recognition*)
10. Code the Programs (*Code the Application *)
11. Test the Programs (*Test all the Applications*)

## How will the final RPI set-up look like?

Gate Security RPI
<img src="https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/1.jpg" width="100px">

Shoe Security RPI
<img src="https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/2.jpg" width="100px">

## Web Application Look and Feel

![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/3.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/4.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/5.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/6.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/7.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/8.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/9.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/10.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/11.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/12.jpg)
![Image of web interface](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/13.jpg)

# 2. Hardware Requirements 
## Hardware Checklist
* 3x Button
* 1x LDR
* 4x Resistors (10K ohms)
* 2x Resistors (330 ohms)
* 1x Buzzer
* 2x piCam
* 1x i2c LCD Screen

# 3. Hardware Set-up

## a) Gate Security RPI
**Final Set-up**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/23.jpg)
**Connect the Buzzer**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/24.jpg)
**Connect the LEDs**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/25.jpg)
**Connect the Buttons**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/26.jpg)
**Connect the LCD**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/27.jpg)

## b) Shoe Security RPI
**Final Set-up**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/28.jpg)
**Connect the LEDs**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/29.jpg)
**Connect the Buzzer**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/30.jpg)
**Connect the Buttons**
![Image of Gate security RPI set-up](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/31.jpg)

# 4. Application Prerequisites
## Doorbell RPI Task(s)
* Make a directory and save ALL files in the directory
	**mkdir ~/doorbell/**
* Make directories for application to save images
	**Mkdir -p /home/pi/Desktop/temp /home/pi/Desktop/thieftemp**
* Install Botocore and Boto3 (https://github.com/boto/boto)
	**sudo pip install boto3**
	**sudo pip install botocore**
* Install awscli
	**sudo pip install awscli**
* Install the Telegram API on your Raspberry Pi (http://telepot.readthedocs.io/en/latest/)
	**sudo pip install telepot**
* Install threading
	**sudo pip install threading**

## Shoe Cabinet RPI Task(s)
* Make a directory and save ALL files in the directory
	**mkdir ~/shoecabinet/**

# 5. AWS IoTcore (MQTT)
## Create a Thing in AWS
1. Login to aws using your credentials.

2. Click on Services and search for IoTcore 
![Image of S5step2](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/32.jpg)

3. Open the navigations on the left. Click on Manage, and then Things.
![Image of S5step3](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/33.jpg)

4. Click on “Create” on the top right corner. Then, click on Create a single thing
![Image of S5step4](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/34.jpg)

5. In the field for name, enter whichever name you desire. Leave the other fields as default. Then click “Next”

6. Proceed to create a certificate using the “One-Click Certificate Creation” 
![Image of S5step6](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/35.jpg)

7. Download the certificates, as well as the rootCA certificate and store them in the Project directory. After which, click on “Activate”.
![Image of S5step7](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/36.jpg)

8. When all is completed, click on “done” to return to the thing selection page. Then, click on the newly created thing. 
![Image of S5step8](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/37.jpg)

9. On the left hand side, click on interact, then copy the REST API endpoint onto a notepad for use later. 
![Image of S5step9](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/38.jpg)

# 6. AWS DynamoDB
## Set-up and store data in the light database
1. Login to aws using your credentials.
2. Open the AWS IOT console, click on “ACT” and click “Create”.
3. Name it as “light”, `“*”` for Attribute and “sensors/light” for Topic filter. Under “Set one or more actions”, click “Add Action” and select the “Split message into multiple columns of a database table (DynamoDBv2), then click “configure action”
![Image of S6step3](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/39.jpg)

4. Click on “Create a new resource” to create one. It will open up a new tab on DynamoDB console. Click on “Create table”. Fill the Table name as “Lights”, and Partition key/Primary key as “date”, and sort as “time”.
![Image of S6step4](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/40.jpg)

5. Click on “Create”. After create a table, back to your “configure action” and refresh that page. Select the “LightSensor” under the Table name and choose “my-iot-role” as for the IAM role name.  Then, click “Add Action”.
![Image of S6step5](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/41.jpg)

6. Login to aws using your credentials.

7. Open the AWS IOT console, click on “ACT” and click “Create”.

8. Name it as “logs”, `“*”` for Attribute and “sensors/facescan” for Topic filter. As before, under “Set one or more actions”, click “Add Action” and select the “Split message into multiple columns of a database table (DynamoDBv2), then click “configure action”
![Image of S6step8](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/42.jpg)

9. Click on “Create a new resource” to create one. It will open up a new tab on DynamoDB console. Click on “Create table”. Fill the Table name as “Logs”, and Partition key/Primary key as “date”, and sort as “event”.
![Image of S6step9](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/43.jpg)

10. Click on “Create”. After create a table, back to your “configure action” and refresh that page. Select the “Logs” under the Table name and choose “my-iot-role” as for the IAM role name.  Then, click “Add Action”.
![Image of S6step10](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/44.jpg)

## Set-up and store data in the passcode database
1. Login to aws using your credentials.

2. Open the AWS IOT console, click on “ACT” and click “Create”.

3. Name it as “passcode”, `“*”` for Attribute and “doorbell/pass” for Topic filter. As before, under “Set one or more actions”, click “Add Action” and select the “Split message into multiple columns of a database table (DynamoDBv2), then click “configure action”
![Image of S6step3](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/45.jpg)

4. Click on “Create a new resource” to create one. It will open up a new tab on DynamoDB console. Click on “Create table”. Fill the Table name as “Passcode”, and Partition key/Primary key as “passid".
![Image of S6step4](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/46.jpg)

5. Click on “Create”. After create a table, back to your “configure action” and refresh that page. Select the “Passcode” under the Table name and choose “my-iot-role” as for the IAM role name.  Then, click “Add Action”.
![Image of S6step5](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/47.jpg)

## Set-up and store data in the visitors log database
1. Login to aws using your credentials.

2. Open the AWS IOT console, click on “ACT” and click “Create”.

3. Name it as “visitors”, `“*”` for Attribute and “doorbell/img” for Topic filter. As before, under “Set one or more actions”, click “Add Action” and select the “Split message into multiple columns of a database table (DynamoDBv2), then click “configure action”
![Image of S6step3](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/48.jpg)

4. Click on “Create a new resource” to create one. It will open up a new tab on DynamoDB console. Click on “Create table”. Fill the Table name as “VisitorLogs”, and Partition key/Primary key as “date", and the sort key as “time”.
![Image of S6step4](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/49.jpg)

5. Click on “Create”. After create a table, back to your “configure action” and refresh that page. Select the “Passcode” under the Table name and choose “my-iot-role” as for the IAM role name.  Then, click “Add Action”.
![Image of S6step5](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/50.jpg)

# 7. AWS S3
1. Under the “Services” navigation, search “s3” and navigate to the AWS S3
![Image of S7step1](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/51.jpg)

2. Next, click on “Create Bucket”.
![Image of S7step2](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/52.jpg)

3. Enter a unique name for your new bucket. (Keep track of the bucket names that you enter.) After which, click on “Create” on the bottom left corner.
![Image of S7step3](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/53.jpg)

4. Next, repeat from step b) to create another container. (Keep track of both the container names as we will be using it later)

5. When the buckets are created, enter the bucket and upload any image into the bucket, then click on the image and take note of the “Link” in the overview. The “Link” without the image name will be your bucket url. For this case, my bucket url will be "https://s3-ap-southeast-1.amazonaws.com/dexjosh-doorcam/ ". Repeat this step for both buckets to get the bucket links that will be used later.
![Image of S7step5](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/54.jpg)

# 8. Telegram Bot
## Creating a telegram bot
1. Open Telegram app in your laptop or mobile and start “BotFather”
![Image of S8step1](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/55.jpg)

2. Type /newbot to create a new bot
![Image of S8step2](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/56.jpg)

3. Give a name to your bot that describes its purpose.
![Image of S8step3](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/57.jpg)

4. Give a username to your bot. Make sure it ends with `_bot`
![Image of S8step4](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/58.jpg)

5. Copy down the access token that is issued by BotFather
![Image of S8step5](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/59.jpg)

## Get own chat ID
1. Open Telegram app in your laptop or mobile and search for @get_id_bot
![Image of S8step1](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/60.jpg)

2. Type /start to get your chat id
![Image of S8step2](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/61.jpg)

3. Record down the chat id for later use. 
![Image of S8step3](https://github.com/joshualeejunyi/KremePi/blob/master/Documentation/Images/62.jpg)
