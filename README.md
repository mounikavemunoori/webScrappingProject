# Step1: Open command prompt or terminal create Directory name as JonesRadiology.
```
  mkdir JonesRadiology
```
# Step2: Navigate to the directory where you want to create the virtual environment. 
# You can use the cd command to change directories.
```
   cd JonesRadiology
```
# Step3: Run the following command to create a virtual environment
```
python3 -m venv myenv
```
# Step:4 Activate the virtual environment.The process for activating the virtual environment depends on your operating system:
For Windows use below command to activate the virtual environment:
```
myenv\Scripts\activate
```
For macOS and Linux:
```
source myenv/bin/activate
```
# Step 5: Create a file name as requirements.txt to install the all the dependencies for the project
Copy the below dependencies in requirement.txt
1. requests
2. beautifulsoup4
3. lxml
4. pandas
5. rpa 

# Step 6: Run below command to install dependencies for execute our script
 ```
 pip3 install -r requirements.txt
 ```
# Step 7 Run the python script using below command
```
python RPA/medicareStatistics.py
```

