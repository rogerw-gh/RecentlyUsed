# RecentlyUsed
 Updated version of recused.py - original source https://askubuntu.com/users/72216/jacob-vlijm, first published in a response to a question about a drop-down tool to list recently used files.
 Original Question
 https://askubuntu.com/questions/803869/is-there-an-indicator-to-quickly-access-recently-used-files.
 
 This code worked with Ubuntu LTS 20.0.4, but not with LTS22.0.4 owing to library changes - naming and code changes to libraries.
 
 The version here, is an updated implementation applying fixes to makes this code work.
 
 ***
 
# Installation dependencies
 
 For Ubuntu [and probably Debian] desktop
 
  - python3-gi
  - libayatana-appindicator3-dev
 
libappindicator3-dev has been replaced with libayatana-appindicator3-dev, which also impacts the library calls.

Daemonising the thread has also changed as  setDaemon() is deprecated.

## Running the code once

  sudo python3 recused.py
  
  
## Running the code on startup

Ubuntu Tweaks provides a way of adding code to startup items.

##  Changing the number of files in the list

Edit the source code and look for

<code>
# --- set the number of recently used files to appear below
n = 300
</code>


