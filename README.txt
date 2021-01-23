██╗     █████╗█████████╗   █████████╗██████╗███╗   ██╗██████╗      ██╗            ██████╗ 
██║    ██╔══██╚══███╔╚██╗ ██╔██╔════██╔═══██████╗  ████╔════╝     ███║           ██╔═████╗
██║    ███████║ ███╔╝ ╚████╔╝█████████║   ████╔██╗ ████║  ███╗    ╚██║           ██║██╔██║
██║    ██╔══██║███╔╝   ╚██╔╝ ╚════████║   ████║╚██╗████║   ██║     ██║           ████╔╝██║
█████████║  █████████╗  ██║  ███████╚██████╔██║ ╚████╚██████╔╝     ██║    ██╗    ╚██████╔╝
╚══════╚═╝  ╚═╚══════╝  ╚═╝  ╚══════╝╚═════╝╚═╝  ╚═══╝╚═════╝      ╚═╝    ╚═╝     ╚═════╝ 
                                                                                                                                                       
 _____           _        _ _       _   _             
|_   _|         | |      | | |     | | (_)            
  | |  _ __  ___| |_ __ _| | | __ _| |_ _  ___  _ __  
  | | | '_ \/ __| __/ _` | | |/ _` | __| |/ _ \| '_ \ 
  | |_| | | \__ | || (_| | | | (_| | |_| | (_) | | | |
|_____|_| |_|___/\__\__,_|_|_|\__,_|\__|_|\___/|_| |_|
                                                       
Any Linux distribution and MacOs System <---

1. open the terminal
2. check python3 --version (better if you have a version >= 3.7), if you have an older versione you can type and execute: sudo apt-get update, sudo apt-get install python 3.9
3. check pip3 --version, if there isn't any pip3 type and execute: sudo apt install python3-pip
4. pip3 install nltk
5. pip3 install PySimpleGUI
6. sudo apt-get install python3-tk
7. pip3 install autocorrect 
8. Wordnet Installation:
	a. python3
	b. import nltk
	c. nltk.download('wordnet')
	d. exit()
9. sudo apt-get update 
10. python3 LazySong.py
                                                                                                                                                         
Spyder4 (for Windows, Linux, MacOs) <---

Type and execute inside the console
1. pip install PySimpleGUI
2. pip install autocorrect
3. import nltk
4. nltk.download('wordnet')
                                                                                                                                                         
 _______       _   
|__   __|     | |  
   | | ___ ___| |_ 
   | |/ _ / __| __|
   | |  __\__ | |_ 
   |_|\___|___/\__|
                    
1. Click on "Browse"
2. Select a Folder containing some .txt files, for example "Lyrics" folder (after *unzip it), then press OK
3. Press "Build Index" and wait some seconds
4. Type a word or a phrase in the search bar, then press "Search"   
5. The reseult with the highest value is the best for your query
                                          
(*)Unzip zip file from terminal:
- sudo apt-get install unzip
- unzip Lyrics.zip
 ____                  
|  _ \                 
| |_) |_   _  __ _ ___ 
|  _ <| | | |/ _` / __|
| |_) | |_| | (_| \__ \
|____/ \__,_|\__, |___/
               _/ |    
             |___/     

- .DS_Store File on MacOs System: if the program close immediatly itself after you press "Build Index", there are good chances that you have .DS_Store file in the folder that you are using to build the Inverted Index. We have set an automate tool that can exploit this problem, but if it doesn't work you need to open the terminal within the data folder and type: find . -name '.DS_Store' -type f -delete. What is .DS_Store and why is so annoying for our program? https://it.wikipedia.org/wiki/.DS_Store when our program start the indexing process it opens up every document in the folder that you have choosen, but if there's this little hidden file, all the process just stop immediatly! If you don't now that there's this file, you end up loosing your mind trying to fix it :(. This often occours on Mac Os system, but when you remove that file everything works like a charm!
- No module named autocorrect: if you try to run the program via terminal (python3 LazySong.py) on macOS Big Sur 11.1, you could encounter an error with that module. We invite you to use Spyder or Atom with the IDE Python Package installed.


  _____       _   _             ___ _      _    __                  
 |_   ____ __| |_(_)_ _  __ _  | _ | |__ _| |_ / _|___ _ _ _ __  ___
   | |/ -_(_-|  _| | ' \/ _` | |  _| / _` |  _|  _/ _ | '_| '  \(_-<
   |_|\___/__/\__|_|_||_\__, | |_| |_\__,_|\__|_| \___|_| |_|_|_/__/
                        |___/                                       
                        
1. Ubuntu 20.04, Kernel Version 5.8.0-38-generic. Hardware Specs: Intel Core i5-6600, 16 gb ram ddr4, gtx 1060 6gb
2. Virtual Machine running on the computer of point 1: Debian 9, Kernel Version 4.9
3. Acer Swift 3 Laptop with Windows 10 version 20H2, equipped with Intel Core i5-8250U, 8gb ram ddr4, no dedicated gpu
4. MacBook Pro late 2013 with MacOs Big Sur 11.1, equipped with Intel Core i5 (dual core version running at 2,4 GHz), 8 gb ram ddr3, integrated gpu Intel Iris with 1536MB


  ___       __     
 |_ _|_ _  / _|___ 
  | || ' \|  _/ _ \
 |___|_||_|_| \___/
                   
Contact Us for any other technical issue! 
- 257544@studenti.unimore.it
- 236330@studenti.unimore.it



