# CowNewsReader

## Description

CowNewsReader is a linux application indicator which listens to the news posted at [COW](https://cow.ceng.metu.edu.tr/News/) and posts Desktop Notifications. All unread news are stored and are accessible from `Open Main Window` button under the indicator's menu . Indicator icon color will change in two cases:

- A new news has arrived and it is not read yet, blue icon <img src="https://github.com/blediboss/CowNewsReader/blob/master/usr/share/cownewsreader/media/mail1.png" width="20" height="20" /> will appear
- There has arrived no news or all news are read, normal icon <img src="https://github.com/blediboss/CowNewsReader/blob/master/usr/share/cownewsreader/media/mail2.png" width="20" height="20" /> will appear

This application is intended to be used by people studying computer engineering at METU.

## Installation

First clone the project
```console
git clone https://github.com/blediboss/CowNewsReader
```
Build the debian package
```console
dpkg -b CowNewsReader
```
Install the package
```console
sudo dpkg -i CowNewsReader.deb
```

##Usage

The CowNewsReader application can be run from terminal with the command

```console
cownewsreader
```

To pin CowNewsReader indicator to the top panel of Ubuntu’s [Unity desktop environment](http://unity.ubuntu.com/) run

```console
cp /usr/share/applications/cownewsreader.desktop ~/.config/autostart/
```
so the application will autostart in log in.

First run log in window will come up. Cow account credentials should be used. If logging in will be successful this window will not appear in the next run. Otherwise an unsuccessful message will appear and the log in window will come up until logged in successfully. 

<img src="https://github.com/blediboss/CowNewsReader/blob/master/images/photo-3.png" /> 


Once logged in the application will start to run and the indicator will appear at the top panel with the normal icon <img src="https://github.com/blediboss/CowNewsReader/blob/master/usr/share/cownewsreader/media/mail2.png" width="20" height="20" />

<img src="https://github.com/blediboss/CowNewsReader/blob/master/images/photo-5.png" /> 

In the indicator menu `Open Main Window` button will bring up the main user interface. Initially empty.

<img src="https://github.com/blediboss/CowNewsReader/blob/master/images/photo-4.png" /> 

Then under `Edit` menu, `Preferences`button will present the list of all courses which can be selected. 

<img src="https://github.com/blediboss/CowNewsReader/blob/master/images/photo-6.png" /> 

If there are course changes the application will register them and start listening for new news accordingly.

Upon the arrival of new news, the icon will change to <img src="https://github.com/blediboss/CowNewsReader/blob/master/usr/share/cownewsreader/media/mail1.png" width="20" height="20" /> and a desktop notification will show up as in the below examples

<img src="https://github.com/blediboss/CowNewsReader/blob/master/images/photo-1.png" /> 
<img src="https://github.com/blediboss/CowNewsReader/blob/master/images/photo-2.png" /> 

### Known Issues

If you discover any bugs, feel free to create an issue on GitHub fork and
send a pull request.

## Authors

* Shkelqim Memolla (https://github.com/blediboss)
* Azat Djanybekov  (https://github.com/adjanybekov)


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request


## License

* [MIT License](http://opensource.org/licenses/MIT)
