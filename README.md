<b> Project 1 – File Drive </b>

<b> University Name: San Jose State University </b>

http://www.sjsu.edu/
 
<b> Course: Cloud Technologies </b>

<b> Professor: Sanjay Garje </b>

<b> ISA: Anushri Srinath Aithal </b>

<b> Student: Amrutha Singh Balaji Singh </b>

<b> LinkedIn: </b> https://www.linkedin.com/in/amruthasinghb/


<b> Project Introduction </b>

FileDrive is a python-based file upload and storage web application. It is hosted on Amazon Web Services. It utilizes AWS Simple Storage Service which is an object storage service to store the user’s files.
It can be used to upload, download, delete and update files with description. It records updated time, uploaded time, file type etc.
It also displays logged in user’s first name, lastname and username.
It is integrated with facebook and google for the ease of logging in via social media. It also has a custom login and register page. It limits the file upload size to 10 MB. It uses content delivery network during the download to enhance the user performance and to reduce the latency. It is built using the APIs for different actions such as upload, download, delete. 


<b> Architecture Diagram: </b>

 ![project1-filedrive 2](https://user-images.githubusercontent.com/42703827/47680694-cc075a00-db84-11e8-89a8-23d020b3fe63.png)

<b> Instructions to run the application: </b>

1.	FileDrive application runs on https. Please ensure that the application page is always on https. 
For example:

 https://amruthasingh.info/login

https://amruthasingh.info/register

https://amruthasingh.info/files


2.	Before running the application, ensure that you are not logged into either Facebook or Google. If logged in, sign out and then access the application.

3.	If there are any cached errors while running the application, open an incognito browser on chrome, ensure that you are signed out from Facebook and Google and then access the application.

4. Install dependencies: pip install -r requirements.txt

<b> Sample Demo Screenshots </b>

1.	Home page: 

The home page has links to login, register and to view privacy policy. 

![image](https://user-images.githubusercontent.com/42703827/47670532-aa997480-db6a-11e8-9d1d-506824714705.png)

2.	Custom register page:

![image](https://user-images.githubusercontent.com/42703827/47670540-af5e2880-db6a-11e8-8b34-d11b7d86b40a.png)

3.	Login page: has links to custom login and login via Facebook and Google.

  ![image](https://user-images.githubusercontent.com/42703827/47670532-aa997480-db6a-11e8-9d1d-506824714705.png)

Login with Facebook: 

![image](https://user-images.githubusercontent.com/42703827/47670554-b71dcd00-db6a-11e8-921c-9839ab35d812.png)


Login with Google:

 ![image](https://user-images.githubusercontent.com/42703827/47670562-bb49ea80-db6a-11e8-9a58-00af7b554d28.png)


4.	After logging in, uploading file successfully:

 ![image](https://user-images.githubusercontent.com/42703827/47670567-bf760800-db6a-11e8-9a5e-9de2558e2870.png)


5.	Deleting the files successfully:

![image](https://user-images.githubusercontent.com/42703827/47670578-c56be900-db6a-11e8-9071-6040161cd2a9.png)

6.	Update option: Download -> Edit -> Upload

![image](https://user-images.githubusercontent.com/42703827/47670583-c9980680-db6a-11e8-9206-48a85880a20a.png)
 
7.	Browsing through files while uploading:

![image](https://user-images.githubusercontent.com/42703827/47670592-cef55100-db6a-11e8-9c76-96ab7a87a842.png)

 
8.	Admin view:

![image](https://user-images.githubusercontent.com/42703827/47670602-d3216e80-db6a-11e8-9a80-b8c8fbc43879.png) 

9.	S3 bucket containing user files:

![image](https://user-images.githubusercontent.com/42703827/47670607-d87eb900-db6a-11e8-82d5-a6d155afc62e.png)

 
