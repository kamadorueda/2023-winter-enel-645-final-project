# enel645_final

## Part 1: Getting started with TALC

Step 1: Open your terminal

To SSH into UCalgary TALC, you will need to open your terminal on your local machine. On a Mac or Linux machine, you can find the terminal in the Applications/Utilities folder. On Windows, you can use software like PuTTY to open a terminal.

Step 2: Enter the SSH command

Once you have opened your terminal, enter the following command:

```
Copy code
ssh <email>@talc.ucalgary.ca
Replace <email> with your own email (the same one you use to log in to other UCalgary systems, for me it would be vladyslav.timofyeyev for example).
```
Step 3: Enter your password

After entering the SSH command, you will be prompted to enter your password. Enter your UCalgary D2L password and press enter. You will not see the password as you type it, but rest assured that it is being entered.

Step 4: Accept the SSH fingerprint

The first time you SSH into UCalgary TALC, you will be prompted to accept the SSH fingerprint. Verify that the fingerprint matches the one listed on the UCalgary TALC website, then type "yes" to accept the fingerprint.

Step 5: Begin using the SSH session

Once you have successfully logged in, you can begin using the SSH session to access your UCalgary TALC account. You can navigate through your files and folders using commands like ls to list files and cd to change directories.

## Part 2: Upload files to TALC
Step 1: Open your terminal

To use SCP to upload a folder to UCalgary TALC, you will need to open your terminal on your local machine. On a Mac or Linux machine, you can find the terminal in the Applications/Utilities folder. On Windows, you can use software like PuTTY to open a terminal.

Step 2: Navigate to the folder you want to upload (enel645_final git repo)

Using the cd command, navigate to the folder that contains the files and folders you want to upload to UCalgary TALC. For example, if the folder is located on your desktop, you can navigate to it by entering the following command:

```
Copy code
cd ~/Desktop/folder_name
```
Replace folder_name with the name of the folder you want to upload.


Step 3: Use SCP to upload the folder

Once you are in the folder you want to upload, use the following command to upload the folder to UCalgary TALC:

```
Copy code
scp -r folder_name <UCID>@talc.ucalgary.ca:/path/to/destination/
```
Replace folder_name with the name of the folder you want to upload, <UCID> with your own UCID (the same one you use to log in to other UCalgary systems), and /path/to/destination/ with the path to the destination folder on UCalgary TALC. For example, if you want to upload the folder to your home directory on UCalgary TALC, you can use the following command:

```
Copy code
scp -r folder_name <UCID>@talc.ucalgary.ca:~
```
Step 4: Enter your password

After entering the SCP command, you will be prompted to enter your password. Enter your UCalgary TALC password and press enter. You will not see the password as you type it, but rest assured that it is being entered.

Step 5: Wait for the upload to complete

Once you have entered your password, the folder upload process will begin. You can monitor the progress of the upload in your terminal window. Depending on the size of the folder and your internet connection, the upload may take some time to complete.

You can check if your files have been uploaded by running `ls` in your talc terminal.

!!! Important

You should copy the .slurm out of the `enel645_final` folder into your home directory by running this in your talc terminal: `cp ~/enel645_final/run_asl_classifier.slurm ~run_asl_classifier.slurm`
You should also verify that you have an `als` conda environment in your TALC. If you don't, you get an error. Here's how you install it:

1. Verify anaconda is loaded by running `module load python/anaconda3-2018.12`
2. Check what environments you have with `conda info --envs`
3. If you only have the base environment, create the asl environment: `conda create -n asl python=3.9` and hit yes to continue - this takes about 15 minutes to load and install everything.

## Part 3: run the batch job
In your terminal, run `sbatch run_asl_classifier.slurm` - you can check if its working by typing `squeue`. All of the python outputs are saved to a `*.out` file in your enel645_final directory in TALC. 

have fun lmao