class Const:
    def __init__(self, idn):
        self.SANDBOX = "sandbox{}".format(idn)
        self.INPUT = "{}/input.txt".format(self.SANDBOX)
        self.OUTPUT = "{}/out.txt".format(self.SANDBOX)
        self.CREATE_DIR = "mkdir {}".format(self.SANDBOX)

        self.TIMEOUT = "5"

        self.COMPILE = "firejail --noprofile  --private={} --net=none -c  timeout {} {} {} 2> {}"
        self.RUN = "firejail --noprofile  --private={} --net=none -c  timeout {} {} {} <{} > {} 2>&1"

        self.PYTHON = "python3"
        self.GCC = "gcc"
        self.JAVAC = "javac"
        self.JAVA = "java"

        self.JAVA_FILE_COMPILE = "Main.java"
        self.JAVA_FILE_COMPILED = "Main"
        self.PYTHON_FILE_COMPILED = "Main.py"
        self.GCC_FILE_COMPILE = "Main.cpp"
        self.GCC_FILE_COMPILED = "./a.out"

        self.JAVA_FILE_CREATE = "{}/{}".format(self.SANDBOX, self.JAVA_FILE_COMPILE)
        self.PYTHON_FILE_CREATE = "{}/{}".format(self.SANDBOX, self.PYTHON_FILE_COMPILED)

        self.C_FILE_CREATE = "{}/{}".format(self.SANDBOX, self.GCC_FILE_COMPILE)

        self.CLEANUP = "rm {} -r"

    def compile_java(self):
        return self.COMPILE.format(self.SANDBOX, self.TIMEOUT, self.JAVAC, self.JAVA_FILE_COMPILE, self.OUTPUT)

    def run_java(self, test_case):
        return self.RUN.format(self.SANDBOX, self.TIMEOUT, self.JAVA, self.JAVA_FILE_COMPILED, self.INPUT + test_case,
                               self.OUTPUT)

    def cleanup(self):
        return self.CLEANUP.format(self.SANDBOX)

    def compile_cpp(self):
        return self.COMPILE.format(self.SANDBOX, self.TIMEOUT, self.GCC, self.GCC_FILE_COMPILE, self.OUTPUT)

    def run_cpp(self, test_case):
        return self.RUN.format(self.SANDBOX, self.TIMEOUT, ' ', self.GCC_FILE_COMPILED, self.INPUT + test_case,
                               self.OUTPUT)

    def run_python(self, test_case):
        return self.RUN.format(self.SANDBOX, self.TIMEOUT, self.PYTHON, self.PYTHON_FILE_COMPILED,
                               self.INPUT + test_case, self.OUTPUT)
