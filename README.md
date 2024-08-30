# Online Store Security Improvement Project

## Project Description

This project was developed for the "Segurança Informática e nas Organizações" course at the Universidade de Aveiro. The objective was to secure an online store web application built using Python and the Flask framework. The project involved identifying and addressing various security vulnerabilities in the original version of the application. The outcome is a secure version of the application where identified vulnerabilities were mitigated, following best practices in web security.

## Authors

- Francisco Gonçalves (Nº Mec: 1008538)

## Identified Vulnerabilities and Implemented Improvements

1. **Cross-Site Scripting (XSS) - CWE-79**
   - **Issue**: Vulnerability to XSS attacks in product reviews.
   - **Improvement**: Sanitized user input to ensure that any input is treated as plain text, eliminating the risk of XSS.

2. **SQL Injection - CWE-89**
   - **Issue**: Susceptibility to SQL Injection via the login form.
   - **Improvement**: Used parameterized queries to prevent SQL injection by separating user inputs from SQL statements.

3. **Weak Password Requirements - CWE-521**
   - **Issue**: Insufficient password complexity requirements.
   - **Improvement**: Enhanced password policies to require a mix of uppercase, lowercase, numbers, and special characters.

4. **Use of Hard-Coded Credentials - CWE-798**
   - **Issue**: Presence of hard-coded credentials in the source code.
   - **Improvement**: Moved sensitive credentials to environment variables for secure storage.

5. **Improper Restriction of Excessive Authentication Attempts - CWE-307**
   - **Issue**: Lack of protection against brute-force attacks.
   - **Improvement**: Implemented rate limiting and account lockout mechanisms after several failed login attempts.

6. **URL Redirection to Untrusted Site (Open Redirect) - CWE-601**
   - **Issue**: Potential for open redirect attacks due to unvalidated URL redirects.
   - **Improvement**: Added validation to ensure redirection only to trusted URLs.

7. **Unverified Password Change - CWE-620**
   - **Issue**: Allowed password changes without verifying the current password.
   - **Improvement**: Required users to enter their current password before allowing changes to their credentials.

8. **Cross-Site Request Forgery (CSRF) - CWE-352**
   - **Issue**: Vulnerability to CSRF attacks that could allow unauthorized actions.
   - **Improvement**: Introduced CSRF tokens to verify and validate user requests, preventing CSRF attacks.

## How to Run the Application

1. Install requirements.txt with pip install requirements.txt
2. Run app.py or app_sec.py
3. Go to http://127.0.0.1:5000
