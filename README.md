Website based on Software Development Tools


# Project Overview
This project takes what I have learned in Software Development Tools to another level, by presenting the anaylsis on a csv file in a Python web application and publishing to the internet. It utilizes Github as the file repository and Render (SAAS platform) to host the application and publish to the Internet.


## Development and Testing
1. The application will rely on 6 main files.
   - requirements.txt
   - app.py
   - EDA.py
   - EDA.ipynb
   - .streamlit/config
   - vehicles_us.csv
3. Create Github repository, ensuring license that is selected will make repo accessible to the public
4. Mirror the Github repo on local machine.
5. Use use jupyter to create notebook for app development.
    - As this application will be used in a browser, Plotly was selected over Matplotlib to render the graphs to the screen
6. Create requirements.txt and add libraries. This file will ensure that only specific Python libraries are used, optimizing the application's performance.
7. Convert the notebook to a .py file using jupyter nbconvert command. This will place the command in a flat Python file which can then be imported into the app.py file in order to access its functions.
```bash
jupyter nbconvert -- to script notebooks/EDA.ipynb
```
9. Create the streamlit configuration file which will tell the server which port to use to publish the application. If not specified the default is port 10000

## Testing on local machine
Publish site with command below. Open a web browser and enter the following url: localhost:10000
```bash
streamlit run app.py 
```

## Update Github main repo
With the application having worked locally, this creates the confidence that it should also work in a remote environment. Push the files to Guthub.

## Deploy to Render
Using the Render GUI, connect to the Github repo to deploy the app. As this python website is using streamlit to server the site, ensure the correct command to start the server is placed in the GUI. Also include the command to install streamlit and the relevant python libraries, in the event they are not installed on the Render SAAS server.

```bash
pip install streamlit & pip install -r requirements.txt
```

```bash
streamlit run app.py 
```


## Launching the app
Open a web browser and enter the following url: https://my-webapp-vjjh.onrender.com/


## License
MIT License was selected for Github repo as this allows any person that obatained a copy of the software to use without restriction. That is the person is allowed to use, copy, modify publish and distribute the software.



# Questions for the Professor
Can you assist in explaining why the app would work only with the default port 8501 for local testing? Conversely it worked only with port 10000 when published in the cloud
# my-webapp