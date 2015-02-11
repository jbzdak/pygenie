# pygenie

This is a wrapper to Canberra Genie library (sold as S560 Programing library), 
this library allows easy reading of gamma spectra files. 

Some time ago a done the same thing in Java: https://github.com/jbzdak/genie-connector, 
but this one is much easier to use and saner. 

This does not wrap whole library, but only the part I needed, 
adding new functions should be easy enough (feel free to add a PR). 

# Installation

1. There is no ``setup.py`` (I didn't need one).
2. Clone this repository, install dependencies 
   (cffi and numpy)
3. You're done    

# Usage 

1. To use this library you'll need to initialize it 
   by: 
        
        from pygenie.init import initialize; initialize()
  
  Here you can provide path to Genie S560 Library
  
2. Good example usage is in ``example/example.py`` file. 

# How it works 

1. It uses cffi (which is a very nice library) to dynamically 
   compile C-Python extension that links directly to 
   Canveberra libraries. 
2. All information that can be extracted from 
   Library header files is extracted from there 
   **at runtime** --- so all parameter definitions 
   are avilable (see example). 
   


    
