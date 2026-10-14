# Lab 5: Static Code Analysis — Reflection

## 1. What did you learn from using static code analysis tools?

I learned that static code analysis helps identify potential bugs, security vulnerabilities, and coding-standard violations without requiring the program to be executed. Pylint helped me evaluate code quality and maintainability, Flake8 identified formatting and PEP 8 violations, and Bandit helped identify potentially insecure coding practices.

Using these tools together provided a broader view of the program's quality than relying on a single tool.

## 2. Which issues were the most important to fix, and why?

The most important issues were the unsafe YAML loading, hardcoded password, remote logging configuration listener, and enabled Flask debug mode because they could introduce security risks.

I also corrected functional problems involving room capacity, duplicate allocations, room vacancy handling, and input validation. These changes improve the correctness and reliability of the hostel allocation system.

## 3. How did static analysis improve your code?

Static analysis helped me identify weaknesses that were not immediately obvious from reading the program. I improved naming conventions, documentation, input validation, and formatting. I also corrected several logical problems identified during code review and runtime testing.

After making the changes, I reran all three tools. Pylint improved from 5.84/10 to 10.00/10, Flake8 reported no findings, and Bandit reported no issues.

## 4. What are the limitations of static code analysis?

Static analysis cannot guarantee that a program is completely correct or secure. A tool may miss logical errors that depend on runtime behavior, user input, or interactions between different components.

For example, a program can receive a clean static-analysis report and still contain an incorrect fee calculation or allocation rule. Therefore, static analysis should be combined with manual code review, functional testing, and appropriate security testing.

## 5. How will you use static analysis in future projects?

I will use static analysis regularly during development rather than waiting until a project is complete. I will run tools such as Pylint, Flake8, and Bandit before committing changes and consider integrating them into automated testing or continuous integration workflows.

This approach should help identify issues earlier, reduce debugging effort, improve maintainability, and encourage secure coding practices.