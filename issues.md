Lab 5: Static Code Analysis — Issues and Fixes

1. Objective

The objective of this exercise was to improve the quality, maintainability, correctness, and security of the Hostel Room Allocation program using Pylint, Flake8, and Bandit.

The initial program was analyzed, the reported issues were reviewed, appropriate corrections were implemented, and all three tools were executed again to verify the improvements.

2. Issues Identified and Fixes Applied

No.	Issue	Type	Original Location	Description	Fix Applied
1	Unsafe YAML loading	Security	Line 21	yaml.load() with the unsafe Loader can construct arbitrary Python objects from untrusted YAML data.	Replaced it with yaml.safe_load() and added configuration validation.
2	Mutable default argument	Code quality / Bug	Line 29	Using preferred=[] as a default argument can cause the same list to be shared across function calls.	Replaced the mutable default with None and initialized the list inside the function.
3	Incorrect type comparison	Code quality	Line 30	Using type(year) != int is less flexible than an appropriate isinstance() check.	Implemented explicit type validation using isinstance() and input validation.
4	Unused function parameter	Code quality	Line 29	The gender parameter was not being used to enforce room eligibility.	Implemented gender-based room eligibility checks.
5	Incorrect room capacity condition	Logic error	Manual code review	The original capacity check allowed a room to exceed its permitted occupancy.	Corrected the capacity check so a full room cannot accept another student.
6	Duplicate student allocation	Logic error	Manual code review	A student could be allocated more than once.	Added validation to prevent duplicate allocations.
7	Incorrect room vacancy handling	Logic error	Manual code review	Vacating a room removed the allocation but did not remove the student from the room’s occupant list.	Updated the vacating operation to remove the student from both records.
8	Hardcoded password	Security	Line 66	A password embedded in source code can be exposed when the code is shared or committed.	Replaced the hardcoded password with an environment variable.
9	Remote logging configuration listener	Security	Line 72	An exposed logging configuration listener can create a security risk if untrusted clients can access it.	Removed the remote logging configuration listener.
10	Flask debug mode enabled	Security	Line 80	Running a web application with debug mode enabled in a deployment can expose sensitive debugging information.	Disabled debug mode in the application startup configuration.
11	Weak random-number generator for lottery	Security / Code quality	Line 56	The original lottery used the general-purpose random module.	Replaced it with secrets.SystemRandom() for stronger randomness.
12	Incorrect priority ordering	Logic error	Manual code review	The original priority ordering did not match the intended seniority-first ordering.	Changed the ordering so higher-year students receive higher priority.
13	Incorrect vacant-bed calculation	Logic error	Manual code review	The original implementation counted completely empty rooms rather than all available beds.	Updated the calculation to sum the unused capacity of all rooms.
14	Unused imports	Code quality	Initial Pylint report	Unused imports increase clutter and reduce readability.	Removed unused imports.
15	Naming and documentation issues	Code quality	Initial Pylint report	Non-standard function names and missing documentation reduced readability and maintainability.	Improved function naming, documentation, and code organization.
16	Formatting violations	Code style	Initial Flake8 report	The original file contained long lines, spacing violations, and other PEP 8 style problems.	Corrected formatting and whitespace issues.

Note: Line numbers refer to the original source where identified in the initial reports. Issues discovered through manual execution and code review do not necessarily correspond to a static-analysis finding.

3. Initial and Final Analysis Results

Tool	Initial Result	Final Result
Pylint	5.84/10	10.00/10
Flake8	19 reported findings	No findings
Bandit	5 reported security findings	No issues identified

4. Conclusion

The exercise improved the Hostel Room Allocation program by addressing security weaknesses, input validation problems, incorrect allocation behavior, and code-quality issues.

The final Pylint score of 10.00/10 indicates that the program satisfies the checks performed by the configured Pylint version. Flake8 reported no remaining style violations, and Bandit identified no remaining issues in its security scan.

These results demonstrate the value of combining static analysis tools with manual code review and runtime testing.