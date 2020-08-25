# track-import
Track python module import and time cost.

This may help you figure out whick module load slow, and show import call stack.

Usages:
  As code in example.py, will print something like this:
```bash
+test_package
	+test_package.test_inner_package
		+test_package.test_inner_package.hello
		|test_package.test_inner_package.hello 0ms 
	|test_package.test_inner_package 1ms #
|test_package 2ms ##
```
