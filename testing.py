import pytest
import app
import pandas as pd


class Test_data_class():
#Arrange
    test_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    test_name = "data"
    test_location = "HCE"

    def test_getter(self):
#Act
        client = app.Data(data = self.test_df, name = self.test_name, location = self.test_location)
        name = client.get_name()   
        location = client.get_location()
#Assert
        assert name == "data"
        assert location == "HCE"

    def test_setter(self):
#Act
        client = app.Data(data = self.test_df, name = self.test_name, location = self.test_location)
        client.set_name("new_name")
        client.set_location("new_location")
        name = client.get_name()   
        location = client.get_location()
#Assert 
        assert name == "new_name"
        assert location == "new_location"

    def test_display(self, capsys):
#Act
        client = app.Data(data = self.test_df, name = self.test_name, location = self.test_location)
        display = client.display()
#Assert
        captured = capsys.readouterr()          
        assert captured.out == "data\nHCE\n" + self.test_df.to_string() + "\n"
        assert captured.err == ""
        

class Test_avg_diff():
#Arrange
    first_test_df = pd.DataFrame({'col1': [1, 2, 3, 4, 5]})
    second_test_df = pd.DataFrame({'col1': [6, 7, 8, 9, 10]})
    
    def test_result(self):
#Act
        result = app.avg_differences(self.first_test_df, self.second_test_df)
#Assert
        assert result == 5

class Test_denan():
#Arrange
    test_df = pd.DataFrame({'col1': [1, 2, 3, 4, 5]})
    test_df_nan = pd.DataFrame({'col1': [1, 2, 3, 4, 5, float('nan')]})

    def test_result(self):
#Act
        result = app.deNaN_dataframe(self.test_df_nan)
#Assert 
        assert result == self.test_df 


