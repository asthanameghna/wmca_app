# West Midlands Combined Authority (WMCA) and Pure LeapFrog Dashboard

For a quick demo, please follow the [LINK HERE](https://asthanameghna-wmca-app-main-5xxw2q.streamlitapp.com/)


CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Recommended modules
 * Installation
 * Configuration
 * Troubleshooting
 * FAQ
 * Maintainers

INTRODUCTION
------------

The project provides a dashboard for visualising and finding clean energy potential 
areas in the WMCA local authority. The tool acts as a frontend to the all the machine 
learning models build to pin point areas of interest in a local authority. The project
and code is open sourced and can be used by any local authority in the U.K. and other 
countries, given they have the correct data.

The repository for the machine learning algorithms can be accessed [here](https://github.com/mikecoughlan/DSSG_WMCA).

   
REQUIREMENTS
------------

This module requires the following modules:

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

   
 TROUBLESHOOTING
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
   users).
   
MAINTAINERS & COLLAOBRATORS
-----------

Please reach out to us if you have any questions:
 * Meghna Asthana (University of York) https://www.cs.york.ac.uk/people/asthana
 * Li-Lian Ang (Minerva University) https://www.linkedin.com/in/anglilian/

This project has been sponsored by:
 * Data Science For Social Good Program at University of Warwick
   Visit [DSSG Warwick](https://warwick.ac.uk/research/data-science/warwick-data/dssgx/) for more information.
