import pytest
import util as app
import pandas as pd

class Test_data_class():
    # Arrange
    test_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    test_name = "data"
    test_location = "HCE"

    def test_getter(self):
        # Act
        client = app.Data(
            data=self.test_df,
            name=self.test_name,
            location=self.test_location
        )
        name = client.get_name()
        location = client.get_location()
# Assert
        assert name == "data"
        assert location == "HCE"

    def test_setter(self):
        # Act
        client = app.Data(
            data=self.test_df,
            name=self.test_name,
            location=self.test_location
        )
        client.set_name("new_name")
        client.set_location("new_location")
        name = client.get_name()
        location = client.get_location()
# Assert
        assert name == "new_name"
        assert location == "new_location"

    def test_display(self, capsys):
        # Act
        client = app.Data(
            data=self.test_df,
            name=self.test_name,
            location=self.test_location
        )
        display = client.display()
# Assert
        captured = capsys.readouterr()
        assert captured.out == "data\nHCE\n" + self.test_df.to_string() + "\n"
        assert captured.err == ""


class Test_avg_diff():
    # Arrange
    first_test_df = pd.DataFrame({'PM1.0': [1, 2, 3, 4, 5]})
    second_test_df = pd.DataFrame({'PM1.0': [6, 7, 8, 9, 10]})

    def test_result(self):
        # Act
        result = app.avg_differences(self.first_test_df, self.second_test_df)
# Assert
        assert result == (3.0, 8.0, 5.0)


class Test_numeric_decorator():
    # Arrange
    def simple_return_double(self, control_df, test_df):
        return control_df, test_df

    def simple_return_single(self, test_df):
        return test_df
    
    control_df = pd.DataFrame({'PM1.0': [1, 2, 3, 4, 5]})
    test_df = pd.DataFrame({'PM1.0': [1, 2, 3, 4, '5']})

    def test_result_double(self):
        # Act
        result, result2 = app.numeric_decorator_double(
            self.simple_return_double)(
            self.control_df, self.test_df
        )
# Assert
        assert result.dtype == result2.dtype


class Test_three_point():
    # Arrange
    test_df = pd.DataFrame({'PM1.0': [1, 2, 3, 5, 10, 15]})

    def test_result(self):
        # Act
        result = app.split_three_point_time(self.test_df)
# Assert
        assert result == (5.0, [3, 4, 5])
