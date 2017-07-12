# Test Cases for WRY

All the unittests here derive from the TestBase.TestBase class with monkey-patches the post method in the requests library.

The replacement method passes the posted data back to the unittest for validation (the UUID is removed to avoid obvious differences). The a canned response is sent back through the full stack.

The CLITools with -x can be used to extract the XML for building new tests. (That's mostly how I did it)
