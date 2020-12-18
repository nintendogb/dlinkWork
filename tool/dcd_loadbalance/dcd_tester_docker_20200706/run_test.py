""" The main entry of this testing tool
  run this program by
  Python3 run_test.py --filename={tester.json}
"""
import argparse
import faulthandler
import json
import jsonschema
import description_schema
import test_description

#===================================================================================================
def load_command_line():
    """load_command_line
      return: ...
    """
    parser = argparse.ArgumentParser("DCD tester")
    parser.add_argument('--file_path', required=True)
    return parser.parse_args()

#===================================================================================================
def main():
    """main()
    """
    #print more information when we get SIGSEGV, SIGFPE, SIGABRT, SIGBUS, and
    #SIGILL signals.
    faulthandler.enable()

    #parse command line
    args = load_command_line()

    # load a file into test_case_description and validate it.
    test_description_content = None
    with open(args.file_path) as json_file:
        test_description_content = json.load(json_file)
        jsonschema.validate(test_description_content, description_schema.SCHEMA)

    #everything's well, let's create a instance.
    inst = test_description.TestDescription(test_description_content)
    inst.run()

#===================================================================================================
if __name__ == "__main__":
    main()
