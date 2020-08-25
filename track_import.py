import imp
import sys
import time


class TimeImport(object):
    def __init__(self, lib_root, fp):
        self._indent = 0
        self._lib_root = lib_root
        self.fp = fp

    def find_module(self, fullname, path=None):
        name = fullname.split(".")[-1]
        file, pathname, description = imp.find_module(name, path)
        if pathname and pathname.startswith(self._lib_root):
            self._path = path
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
                path = self._path

            file, pathname, description = imp.find_module(name, path)
            module = imp.load_module(name_or_package, file, pathname, description)
            sys.modules[name_or_package] = module
            return module
        except Exception as e:
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

