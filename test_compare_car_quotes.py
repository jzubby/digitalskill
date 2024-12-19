import pytest
from utils.extract_uk_reg_num import ExtractUKRegNumberFromGivenTxtFile
from utils.car_valuation_sites import MotorWaySite

class TestVehicleValuation:
    """
    Test cases for vehicle valuation
    """
    @staticmethod
    def get_vehicle_reg_and_output():
        """
        we want to see the search results for all discovered vehicle reg number, so parametrize to run through all entires
        """
        extracted_reg_number = ExtractUKRegNumberFromGivenTxtFile(verify_if_existing_in_output_file=True)
        unique_reg_number, output_content_dict = extracted_reg_number.extract_uk_reg_number()
        reg_output_list = []
        for each_veh_reg in unique_reg_number:
            output_validation = [x for x in output_content_dict if
                             x["VARIANT_REG"].replace(" ", "").lower() == each_veh_reg.replace(" ", "").lower()]
            if not output_validation:
                print(f"Warning:==> Vehicle with registration number {each_veh_reg} have no corresponding output file entry, it will be ignored for testing")
                continue
            reg_output_list.append((each_veh_reg, dict(output_validation.pop(0))))
        for ele in reg_output_list:
            car_reg, out_val = ele
            yield car_reg, out_val


    @pytest.mark.parametrize("car_reg, output_validation_dict", get_vehicle_reg_and_output())
    def test_vehicle_valuation_for_motor_way_site(self, driver, global_wait_time_out, car_reg, output_validation_dict):
        """
        Test MotorWaySite valuation site
        :param driver: selenium driver
        :param global_wait_time_out: given timeout wait time
        :param car_reg: extracted car reg number
        :param output_validation_dict: extracted outfile dict containing the corresponding validation entries for car_reg
        """
        expected_page_title = "Sell My Car | Fast, Free, Get Your Highest Offer"
        motor_way_page_obj = MotorWaySite(driver=driver, reg_number=car_reg, global_wait_time_out=global_wait_time_out)
        print(f".....Testing with the following information: \n Extracted Vehicle Registration number: {car_reg}"
              f"\n Output Validation: {output_validation_dict} \n Valuation site: {motor_way_page_obj.site_key}.....\n".upper())

        found_page_tile = motor_way_page_obj.navigate_to_site()
        assert found_page_tile == expected_page_title, "Page may have not loaded correctly: page title got ===> " + found_page_tile

        vehicle_model = motor_way_page_obj.submit_reg_info_on_hope_page()
        assert vehicle_model is not None, "\n Vehicle Registration submission may have not been successful"

        vehicle_details = motor_way_page_obj.extract_vehicle_details()
        # find and print all mismatched attribute and fail (if any fails)
        # perform case-insensitive compare
        mismatch = 0
        for extracted_vehicle_attr, extracted_vehicle_value in vehicle_details.items():
            try:
                # VARIANT_REG fails because of optional space in reg number which is not uniform in extracted
                # values in input and the output file, from my perspective it is not a valid failure so i handle it explicitly
                if extracted_vehicle_attr.lower() == "VARIANT_REG".lower():
                    assert output_validation_dict[extracted_vehicle_attr].replace(" ", "").lower() == extracted_vehicle_value.replace(" ", "").lower()
                else:
                    assert output_validation_dict[extracted_vehicle_attr].lower() == extracted_vehicle_value.lower()
            except AssertionError:
                print(f"\n Extracted values for key: {extracted_vehicle_attr}: differs \n\t Extracted Value:{extracted_vehicle_value}"
                                  f" \n\t Output file Value:{output_validation_dict[extracted_vehicle_attr]}")
                mismatch += 1
                continue
            else:
                print(f"\n PASSED CHECK: \n\t {output_validation_dict[extracted_vehicle_attr].lower()} == {extracted_vehicle_value.lower()}")

        assert not mismatch , "There are mismatched attribute, Number of attributes: " + str(mismatch)


    def implement_other_vendors(self):
        pass