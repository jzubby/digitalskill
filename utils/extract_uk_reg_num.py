from typing import Tuple, List,Dict
import re
import os
import csv
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class ExtractUKRegNumberFromGivenTxtFile():
    """
    The function will encapsulate the logic to extract UK registration number from a given text
    file constructed in human natural language
    typically a UK registration number specification can be summed us as follows:
    1. Starts with two uppercase letters
    2. followed by 2 digits
    3. followed by optional (single) space
    4. Ends with 3 uppercase letters
    """

    def __init__(self, input_file_path: str = "input_file_loc",  out_put_file_path: str = "output_file_loc", verify_if_existing_in_output_file: bool = False):
        """

        :param text_file_path: name of the directory containing the input file or actual input file name,
                 if directory is given, all files in the directory will be searched ,
                 searches relative to BASE_PATH (...../digitalskills), else full path can be given
        :param verify_if_existing_in_output_file flag to indicate if we need to verify that every extracted entry in input file
               there is corresponding entry in the output file
        :param out_put_file_path name of the directory containing the output file or actual output file name,
                 if directory is given, all files in the directory will be searched ,
                 searches relative to BASE_PATH (...../digitalskills), else full path can be given
        """
        self.input_text_path = input_file_path
        self.pattern_matcher = r'\b[A-Z]{2}[0-9]{2}\s?[A-Z]{3}\b'
        self.verify_if_existing_in_output_file = verify_if_existing_in_output_file
        self.out_put_file_path = out_put_file_path
        if self.verify_if_existing_in_output_file:
            assert self.out_put_file_path is not None

    @staticmethod
    def read_text_file(file_path: str) -> str:
        """
        function to read text input file giving, relative to BASE_PATH
        :param file_path the input file directory or file name
        :return: content
        """
        content = ""
        try:
            if os.path.isfile(os.path.join(BASE_PATH, file_path)):
                with open(os.path.join(BASE_PATH, file_path), 'r') as txt_file:
                    content = txt_file.read()
            elif os.path.isdir(os.path.join(BASE_PATH, file_path)):
                for each_file in os.listdir(os.path.join(BASE_PATH, file_path)):
                    with open(os.path.join(BASE_PATH, file_path, each_file), 'r') as txt_file:
                        content += txt_file.read()
            else:
                 if os.path.isfile(file_path):
                     with open(os.path.join(file_path), 'r') as txt_file:
                         content = txt_file.read()
                 else:
                     raise FileNotFoundError
        except FileNotFoundError:
            print(f"Files does not exist, check the given path ===> '{file_path}'.")
        except Exception as file_read_error:
            print(f"Unable to read file error occurred: {file_read_error}")
        return content

    @staticmethod
    def read_output_file_to_dict(output_file_path: str) -> List[Dict[str, str]]:
        """
        read the output file and convert to dictionary
        :param output_file_path:
        :return:
        """
        output_data = []
        try:
            if os.path.isfile(os.path.join(BASE_PATH, output_file_path)):
                with open(os.path.join(BASE_PATH, output_file_path), 'r') as output_file:
                    reader = csv.DictReader(output_file)
                    output_data = [row for row in reader]
            elif os.path.isdir(os.path.join(BASE_PATH, output_file_path)):
                for each_file in os.listdir(os.path.join(BASE_PATH, output_file_path)):
                    with open(os.path.join(BASE_PATH, output_file_path, each_file), 'r') as output_file:
                        reader = csv.DictReader(output_file)
                        output_data += [row for row in reader]
            else:
                if os.path.isfile(output_file_path):
                    with open(os.path.join(BASE_PATH, output_file_path), 'r') as output_file:
                        reader = csv.DictReader(output_file)
                        output_data = [row for row in reader]
                else:
                    raise FileNotFoundError
        except FileNotFoundError as output_error:
            print(f"File does not exist, check the given path ===> '{output_file_path}' not found. Error: {output_error}")
        except Exception as output_error:
            print(f"An error occurred: {output_error}")
        return output_data

    def extract_uk_reg_number(self) -> Tuple[List[str], List[Dict[str, str]]] | None:
        """
        extract the reg, read the output file into a dict and optionally check if the extracted reg and reg(s) found
         in output file are all present
        :return:
        """

        contents = self.read_text_file(self.input_text_path)
        if contents:
            reg_no = re.findall(self.pattern_matcher, contents)
            # if directory (or file) is given their may be duplicates, so clean out duplicates
            unique_input_reg_number = set(reg_no)
            output_content_dict = self.read_output_file_to_dict(self.out_put_file_path)
            if self.verify_if_existing_in_output_file:
                # strip spaces between Reg number to be able to validly compare against output values.
                # output file seems to have no optional space either by design or luck!!
                striped_unique_input_reg_number = set([x.replace(" ", "") for x in reg_no])
                unique_output_reg_number = set([each_car["VARIANT_REG"] for each_car in output_content_dict])
                diff_reg = striped_unique_input_reg_number.symmetric_difference(unique_output_reg_number)
                # if there are differences in the vehicle registration found in input and out files , what do we do, for now we just warn and ignore check later in test
                if diff_reg:
                    print(f"Found differences between the extracted Registration number from input file and output file {diff_reg}")
            return list(unique_input_reg_number), output_content_dict
        return None
