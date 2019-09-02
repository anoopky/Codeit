import onlinecompiler.core.execution as exe


class Compiler:
    def __init__(self, code, lang, user_id, in_data):
        execute = exe.Execution(user_id)
        input_len = len(in_data)
        # creating input file for execution
        for test_case in range(input_len):
            execute.create_input_file(in_data[test_case], str(test_case))

        self.output = []
        self.time = 0
        # running the program

        for test_case in range(input_len):
            out = execute.compile_run(lang, code, str(test_case))
            self.time += execute.time.microseconds
            self.output.append(out)

        execute.cleanup()
