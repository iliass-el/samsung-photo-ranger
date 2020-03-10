# Samsung Photo Ranger
automatic images organizing

# Problem
Since 2012 I used to store all my phone pictures on my laptop for several years under arbitrary folder names, so i made this script to organize automatically all the images into folders with the names of the images year.

The script range all images based on their names.
It walks through all sub folders to look for pictures and finally merge the images of the same year in one folder.

The script use regular expression to extract the images year.

# Usage
```
python photos.py -p "D:\Images" -l -m  
```
```
-p : specifie images directory  
-l : Create log file  
-m : Merge folders with same name(year)  
```

# Recongnized Patterns

* Screenshot_2013...
* 20180414_19.......
* IMG_2018_.........
* VID_2016_.........
* Name.2014.........
* WIN_2020..........

# Flow chart

![Traverse folder algo](dqdqdwqdq)

# Result
![organized images](result)