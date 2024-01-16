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

    
