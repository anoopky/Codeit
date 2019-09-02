import os
import onlinecompiler.core.const as const
import datetime


class Execution:
    def __init__(self, idn):
        self.commands = const.Const(idn)
        self.create_sandbox()
        self.time = 0
        self.writefile(self.commands.OUTPUT)

    def create_input_file(self, content, test_case):
        input_file = self.commands.INPUT + test_case
        self.writefile(input_file, content)

    def create_sandbox(self):
        self.execute_command(self.commands.CREATE_DIR)

    def compile_run(self, lang, code, test_case):
        self.write_code_file(lang, code)

        if lang == "Java":
            s = self.commands.compile_java()
            self.execute_command(s)
            err = self.output()
            if len(err):
                return err
            else:
                s = self.commands.run_java(test_case)
                self.execute_command(s)
                return self.output()

        elif lang == "C/C++":
            s = self.commands.compile_cpp()
            self.execute_command(s)
            err = self.output()
            if len(err):
                return err
            else:
                s = self.commands.run_cpp(test_case)
                self.execute_command(s)
                k = self.output()
                return k

        elif lang == "Python":
            s = self.commands.run_python(test_case)
            self.execute_command(s)
            return self.output()
        else:
            return None

    def execute_command(self, s):
        a = datetime.datetime.now()
        os.system(s)
        b = datetime.datetime.now()
        self.time = b - a

    def cleanup(self):
        self.execute_command(self.commands.cleanup())

    @staticmethod
    def writefile(name, content=''):
        f = open(name, "w")
        f.write(str(content))
        f.close()

    def write_code_file(self, lang, code):
        if lang == "Java":
            self.writefile(self.commands.JAVA_FILE_CREATE, code)
        elif lang == "C/C++":
            self.writefile(self.commands.C_FILE_CREATE, code)
        elif lang == "Python":
            self.writefile(self.commands.PYTHON_FILE_CREATE, code)

    @staticmethod
    def readfile(name):
        f = open(name)
        data = f.read()
        f.close()
        return data

    def output(self):
        return self.readfile(self.commands.OUTPUT)
