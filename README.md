# West Midlands Combined Authority (WMCA) and Pure LeapFrog Dashboard

For a quick demo, please follow the [LINK HERE](https://asthanameghna-wmca-app-main-5xxw2q.streamlitapp.com/)


CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Folder Structrue
 * Requirements
 * Installation on Local Device
 * Running on Local Device
 * Deploying your Dashboard
 * Recommended Tutorials
 * Maintainers

INTRODUCTION
------------

The project provides a dashboard for visualising and finding clean energy potential 
areas in the WMCA local authority. The tool acts as a frontend to the all the machine 
learning models build to pin point areas of interest in a local authority. The project
and code is open sourced and can be used by any local authority in the U.K. and other 
countries, given they have the correct data.

The repository for the machine learning algorithms can be accessed [here](https://github.com/mikecoughlan/DSSG_WMCA).


FOLDER STRUCTURE
------------
```
.
├── data                                           
│   ├── SJ9000.geojson                             # Map shapefile data
│   ├── full_dataset_outputs.csv                   # Map tabular data
│   ├── numerical_individual_columns_data_demo.csv # EPC Ratings data
│   ├── sample_outputs_demo.csv                    # Electric Heating data
│   └── sample_outputs_old_demo.csv                # Predicted Electric Heating data
├── images
│   ├── pure_leapfrog.png
│   ├── wmca.png
├── pages
│   ├── epc_rating.py                              # EPC Rating Prediction Model Page
│   ├── heating_type.py                            # Electric Heating Prediction Model Page
│   ├── heatmap.py                                 # Mother file for all heatmaps
│   ├── home.py                                    # Homepage
│   ├── map.py                                     # Mother file for all maps               
│   ├── solar_pv.py                                # Solar PV Prediction Model Page
├── LICENSE.md
├── README.md
├── main.py                                        # Main app runner file
└── requirements.txt                               # Required packages to run the app
```
   
REQUIREMENTS
------------

This project requires the following modules:

 * [pip](https://pip.pypa.io/en/stable/installation/)
 * [streamlit](https://pypi.org/project/streamlit/)
 * [pandas](https://pypi.org/project/pandas/)
 * [plotly express](https://pypi.org/project/plotly-express/)
 * [plotly](https://pypi.org/project/plotly/)
 * [streamlit options menu](https://pypi.org/project/streamlit-option-menu/)
 * [leafmap](https://pypi.org/project/leafmap/)
 * [numpy](https://pypi.org/project/numpy/)
 * [geopandas](https://geopandas.org/en/stable/getting_started/install.html)
 * [pydeck](https://pypi.org/project/pydeck/)
 * [shapely](https://pypi.org/project/Shapely/)
 * [matplotlib](https://pypi.org/project/matplotlib/)

For specific versions, please refer to [requirements](https://github.com/asthanameghna/wmca_app/blob/main/requirements.txt) file.

The data format is a .geojson file with the building footprint to view the 3D map. The code will parse the coordinates into an acceptable form for pydeck. The 3D map will reduce the speed of the web app, so if you opt to use a different map, please see `render_map.py`, to switch the form of the map.

INSTALLATION ON LOCAL DEVICE
------------
 
 * Download the entire project either using git clone or download as zip option.

 * Once the folder is on your local device, open a new terminal window check the version of python on you device using ```python -v``` and install the compatible pip version for it.
 
 * Now check version of pip using ```pip -version``` and navigate to your project folder
 
 * Install all the packages in requirements.txt using pip (links for each installation command provided above).
 
 * Check for correct installation in your desired folder using the following commands:
   ```$ python```
   and it will show the follwing message:
   ```
   Python 3.8.8 (default, Apr 13 2021, 12:59:45) 
   [Clang 10.0.0 ] :: Anaconda, Inc. on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   >>>
    ```
   Use command
   ```
   import streamlit
   ```
   If the respose does not provide any error you have successfully installed all the      dependencies.
   
RUNNING ON LOCAL DEVICE
-------------
 
 * Open a new Terminal window and navigate to the project folder. Use command
   ```
   streamlit main.py
   ```
   This would provide you a localhost link where the app is running. Something like this
   ```
   You can now view your Streamlit app in your browser.

   Local URL: http://localhost:8501
   Network URL: http://192.168.0.24:8501
   ```
 
 * Now you can navigate the app to explore more and create your own changes. (A preferable IDE for editing could be Visual Studio Code, PyCharm or Sublime).
 
 
 DEPLOYING YOUR DASHBOARD
------------
 
 * Sign up to [Streamlit Cloud](https://streamlit.io/cloud) using your GitHub account. It is invitation based so you might need to wait to get you account. It is advised to do this step in advance.

 * You will recieve an invitation to you github email and follow the steps as mentioned.
 
   <img width="586" alt="welcome_streamlitcloud" src="https://user-images.githubusercontent.com/34877328/186226007-54c95a18-7ce1-4ce1-adbd-334a4a991279.png">

 
 * If you have made any changes to the code and introduced new packages, you will need to update the ```requirements.txt``` file. For this, open a new terminal window and navigate to the project folder. Use the command  ```pip install pipreqs``` which will install the 
 [pipreqs](https://pypi.org/project/pipreqs/) for creating the ```requirements.txt``` file. Finally, use command ```pipreqs --force``` to overwrite the old ```requirements.txt``` file.
 
 * Update your GitHub repository with the current code on your local machine.
 
 * Now sign back in to your streamlit.io account and follow the instructions provided in the video below. (Instead of using ```streamlit_app.py``` as your Main Path use ```main.py``` - same as local device)
 

   https://user-images.githubusercontent.com/34877328/186225645-fb439789-ee4b-40e3-9c65-1362ec80d5b6.mp4


 * Once deployed, you should be able to share the dashboard using the url.
 
   <img width="1428" alt="Screenshot 2022-08-23 at 18 38 52" src="https://user-images.githubusercontent.com/34877328/186227305-c8225750-7605-42cd-a094-573d85f5ffe7.png">
   
   
RECOMMENDED TUTORIALS 
-------------

 * [A Beginner's Guide to Streamlit](https://www.youtube.com/playlist?list=PLM8lYG2MzHmRpyrk9_j9FW0HiMwD9jSl5)

 * [Developing a Streamlit Web App for Geospatial Applications](https://www.youtube.com/watch?v=fTzlyayFXBM)

   
<!--  TROUBLESHOOTING
---------------

 * If the menu does not display, check the following:

   - Are the "Access administration menu" and "Use the administration pages
     and help" permissions enabled for the appropriate roles?

   - Does html.tpl.php of your theme output the $page_bottom variable?

FAQ
---

Q: I enabled "Aggregate and compress CSS files", but admin_menu.css is still
   there. Is this normal?

A: Yes, this is the intended behavior. the administration menu module only loads
   its stylesheet as needed (i.e., on page requests by logged-on, administrative
   users). -->
   
MAINTAINERS & COLLAOBRATORS
-----------

Please reach out to us if you have any questions:
 * Meghna Asthana (University of York) https://www.cs.york.ac.uk/people/asthana
 * Li-Lian Ang (Minerva University) https://www.linkedin.com/in/anglilian/

This project has been sponsored by:
 * Data Science For Social Good Program at University of Warwick
   Visit [DSSG Warwick](https://warwick.ac.uk/research/data-science/warwick-data/dssgx/) for more information.
