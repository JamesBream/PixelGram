# PixelGram
CS Team Project - Socially driven wallpaper sharing.

## Getting Started

The following need to be installed to get started with developing for PixelGram from a clean install on Windows... Don't give me that look. It's necessary.

    - Install Git (https://git-scm.com/downloads)
        - Create a folder for the project, navigate to this folder using cd.
        - (cmd) git clone https://github.com/JamesBream/PixelGram.git

The best way to learn how to use Git is probably by using this resource https://try.github.io/

    - Install Python 3.5.x
    - (cmd) pip3 install flask
    - (cmd) pip3 install flask-mysqldb
    - (cmd) pip3 install pillow
    
    
No troubles? Awesome.

    - Install MariaDB 10.1.x
    - Set root password (For security)
    
Finally, some utilities... (Yeah, we're getting there, almost I think.)

    - Install Adobe Brackets 
    - Install MySQL Workbench

If everything instaleld, you should be able to do `python3 app.py` in the terminal to run the server. This can be left running in the background and is set up to automatiaclly detect changes in the `.py` files so you don't need to restart the server when changes are made.