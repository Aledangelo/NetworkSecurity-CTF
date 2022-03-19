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

**Union-Based SQL Injection**
This type of injection utilises the **SQL UNION** operator alongside a **SELECT** statement to return additional results to the page. This method is the most common way of extracting large amounts of data via an SQL Injection vulnerability.



## Command Injection

## Privilege Escalation

## Cracking Password
