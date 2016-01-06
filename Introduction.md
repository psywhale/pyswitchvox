# How to run things #
It's really pretty simple. Run each of the programs in the bin directory, each one will print out usage directions to the terminal. Pretty simple, eh?

# Python requirements #
  * Version 0.1 available in downloads (and tags section of source) has been tested with Python 2.4, 2.5, and 2.6.
  * The version available in the trunk section of the source repository works with all of the above plus Python 3.0 and 3.1.

# Operating System #
I've done tests on Linux and Windows.  Both work.  I would be very surprised if OS X doesn't also work.

# Dependencies (general) #
  * If you're not running Python 2.6 or later, you need **simplejson**.

# Dependencies (for version 0.1) #
  * With Stephen's changes, wget is no longer required.  However, the wget dependency described in the next bullet is still true of the version 0.1.
  * You also need **Wget**. It turned out (thanks in large part to David Podolsky's blog entry on using Wget with Switchvox's API) that using Wget was easier than dealing with the Python standard library's handling of SSL/https. And I didn't want to require a separate Python module. So, Wget is now a dependency. This should only really be an issue for people running Windows. I'd expect every other platform will have Wget. Windows users can find Wget binaries pretty easily with a quick Google search.  Make sure Wget is on the system path, or else the program won't be able to find Wget.