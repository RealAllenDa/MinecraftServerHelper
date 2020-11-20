# MCSH - A Minecraft server helper

Program version 0.0.1-InEDev. Docs version 0.1.0.

> Warning: This program is under very early development.
> 
> Any use except testing and development is strongly unrecommended.

MCSH is a server helper for Minecraft. It can use to create, manage, upgrade BE/JE servers.
By now, it only has CLI interface, considering its cross-platform compatibility. A web interface will come out soon.

# Installation
MCSH can run on Windows and Linux (Mac) platform, and on Python version 3.7 or higher.

You can clone the repository using the following command:

```bash
git clone https://github.com/RealAllenDa/MinecraftServerHelper.git
```

Then, cd to that directory and run 'mcsh-cli.py' using your Python:

```bash
cd MinecraftServerHelper
pip instal -r requirements.txt
python mcsh-cli.py
```

Now, a first-time run wizard should appear. Choose the language, and the program will close.

Run the program again, then you shall see the help message.

# Compatibility
The MCSH is (theoretically) compatible with all systems running Python, but for compatibility consideration, it's only
designed to be run in Linux, Windows, and Mac.

# Command line tools

## --version
Shows the version of the program.

## --help
Shows the help message of the program.

## --list
List all the server(s) installed in MCSH. You'll get a message like this:
```
Servername | Type | ServerState | ServerVersion
```
e.g. A 1.16 Java Edition server named 'Test' is running:
```
Test | JE | RUNNING | 1.16
```

## --install
A CLI interface should pop up.

## --remove
