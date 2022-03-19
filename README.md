# Network Security DSP

## Man In The Middle

## Cookie Stealing and Hijacking Session

## SQL injection

SQL (Structured Query Language) Injection, mostly referred to as SQLI, is an attack on a web application database server that causes malicious queries to be executed. When a web application communicates with a database using input form a user that hasn't been properly validated, there runs the potential of an attacker being able to steal, delete or alter private and customer data and also attack the web applications authentication methods to private or customer areas.
This is why as well as SQLI being one of the oldest web application vulnerabilities, it also can be most damaging.

In this scenario, it is possible to search among the products in the database using an html form. You can see that this is a GET request by looking at the URL:

* http://193.20.1.2:5000/search?nome=mela

From the URL above, you can see that the results comes from the "nome" parameter in the query string. The web application needs to retreive the article from the database and may use an SQL statement that looks something like the following:
* **[...] SELECT all FROM table WHERE nome=mela [...]**

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

**Command Injection** is an attacck in wich the goal is execution of arbitrary commands on the host operating system via a vulnerable application. These attacks are possible when an application passes unsafe user supplied data (forms, cookies, HTTP headers etc.) to a system shell. In this attack, the attacker-supplied operating system command are usually executed with the privileges of the vulnerable application. Command injection attacks are possible largely due to insufficient input validation.

## Privilege Escalation

## Cracking Password
