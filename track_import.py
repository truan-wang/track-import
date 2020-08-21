import imp
import os
import sys
import time


class TimeImport(object):
    def __init__(self, lib_root, fp):
        self._indent = 0
        self._lib_root = lib_root
        self.fp = fp

    def find_module(self, fullname, path=None):
        if path and path[0].startswith(self._lib_root):
            name = fullname.split(".")[-1]
            if os.path.exists(os.path.join(path[0], name)) or os.path.exists(os.path.join(path[0], name + ".py")):
                self.path = path
                return self
        return None

    def load_module(self, name_or_package):
        start = time.time()

        if name_or_package in sys.modules:
            return sys.modules[name_or_package]

        self.fp.write(
            ("\t" * self._indent) +
            "+%s\n" % name_or_package
        )
        self._indent += 1
        try:
            if "." in name_or_package:
                package = ".".join(name_or_package.split(".")[:-1])
                name = name_or_package.split(".")[-1]
                module = sys.modules[package]
                path = module.__path__
            else:
                name = name_or_package
                path = self.path

            file, pathname, description = imp.find_module(name, path)
            module = imp.load_module(name_or_package, file, pathname, description)
            sys.modules[name_or_package] = module
            return module
        except Exception, e:
            sys.stderr.write("IMPORT ERROR: %s " % e + "*" * 10)
            raise e
        finally:
            self._indent -= 1
            duration_ms = int(1000 * (time.time() - start))

            self.fp.write(
                ("\t" * self._indent) +
                "|%s %sms " % (name_or_package, duration_ms) +
                min(duration_ms, 100) * "#" +
                "\n"
            )


sys.meta_path.insert(0, TimeImport(
    "/Users/truan.wang/workspace/justing",
    sys.stdout
))
