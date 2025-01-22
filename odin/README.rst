Getting Started with Odin 101
#############################

:Author: 
    Louis Richard

:Version: 1.0 of 2025-01-16

Install VSCode on your computer
*******************************

To install Visual Studio Code (VSCode) on your computer, follow the instructions on the `VSCode website <https://code.visualstudio.com/download>`_.


Setup SSH connection
*********************

Install the SSH FS extension for VSCode as follow:

* Open VSCode
* Click on Extensions in the Manage icon on the bottom left side of the screen.
* Search for Remote - SSH
* Click on Install

Alternatively, you can install the extension from the `VSCode Marketplace <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh>`_.


Connect to Odin from IRF-U/IRF-U VPN
=====================================

Add Odin to the list of Remotes
-------------------------------

Once you have installed the Remote - SSH extension, you can add Odin to the list of Remotes by following these steps:

* Click on the Remote Explorer icon on the left side of the screen.
* Click on the + icon (New Remote).
* Enter SSH Connection command: `ssh <username>@odin.irfu.se`
* Select the configuration file to save the connection (e.g., `/Users/<username>/.ssh/config`).

Connect to Odin
---------------

To connect to Odin:

* Click on the Odin connection in the Remote Explorer.
* Click on Connect to Host in Current Window/Connect to Host in New Window.
* Enter your password.

Connect to Odin from outside of IRF-U/IRF-U VPN
===============================================

For remote connection (outside of IRF-U) you'll need to connect to Brain first. For that you'll need to add brain to the list of Remotes

Add Brain to the list of Remotes
-------------------------------

To add brain to the list of Remotes follow these steps:

* Click on the Remote Explorer icon on the left side of the screen.
* Click on the + icon (New Remote).
* Enter SSH Connection command: `ssh <username>@brain.irfu.se`
* Select the configuration file to save the connection (e.g., `/Users/<username>/.ssh/config`).


To connect to Odin through Brain you'll need to add the following line to your SSH configuration file:

* Open your SSH configuration file (e.g., `/Users/<username>/.ssh/config`).
* Add the following line: `ProxyJump brain.irfu.se` under the Odin configuration.

Connect to Odin through Brain
-----------------------------

To connect to Odin:

* Click on the Odin connection in the Remote Explorer.
* Click on Connect to Host in Current Window/Connect to Host in New Window.
* Enter your password a first time. This will connect you to Brain.
* Enter your password a second time. This will connect you to Odin.


Setup Python Environment
************************

Since you are unlikely to have root access on Odin, you'll need to create a virtual environment to install Python packages. To do so, follow these steps:

* Connect to Odin in a new window.
* In the start menu, select Open.
* Open your main repository folder (e.g., `/homelocal/<username>/`).
* Open a terminal (Terminal > New Terminal).
* Create a virtual environment: 

.. code-block:: console
    
        python3 -m venv <env_name>
        

* Activate the virtual environment: `source <env_name>/bin/activate`.

You can now install Python packages using pip. For example, to install numpy, run `pip install numpy`. To deactivate the virtual environment, run `deactivate`. To reactivate the virtual environment, run `source <env_name>/bin/activate`.

.. note::

    When you are done working on Odin, remember to deactivate the virtual environment by running `deactivate`. You can choose to always activate the virtual environment when you connect to Odin by adding the activation command to your `~/.bashrc` file.



Working with Odin
*****************

To start working with Odin, follow these steps:

* Connect to Odin in a new window, and open your main repository folder.
* Create a new repository folder for your project (e.g., `mkdir odin-tuto` in a Terminal or use New Folder in the Explorer).
* Download the example Jupyter Notebook using the following command: `curl -o /homelocal/<username>/odin-tuto/example_mms_b_e_j.ipynb https://raw.githubusercontent.com/louis-richard/irfu-python/refs/heads/devel/docs/examples/01_mms/example_mms_b_e_j.ipynb`
* If you have not already done so, install the Python and Jupyter extension for VSCode.
* If you have not already done so, activate the virtual environment.
* Open the Jupyter Notebook in VSCode.
* Run the first cell of the Notebook to import the necessary packages. If you encounter an error, install the missing package using pip. For example, to install pyrfu, run `pip install pyrfu`. Then, run the cell again.
* On the first excution of the Notebook, you will be asked to select a kernel. Choose the Python kernel corresponding to your virtual environment `<env_name>/bin/python`
* Run the remaining cells of the Notebook.


*Enjoy working with Odin!*

Support
*******
If you encounter any issues or have any questions, please contact Louis Richard on Slack or by email at :email:`louisr@irf.se`.





