"""------------------------------------------------------------------------------
                                Chronology Tests
------------------------------------------------------------------------------"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from chronodata.chronology import Chronology
from chronodata.utils.constants import String, Number, Msg, Datetime, Key, Calendar
    
"""------------------------------------------------------------------------------
                                DataFrame Tests
------------------------------------------------------------------------------"""

def test_test():
    df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df2 = pd.DataFrame({'a': [1, 2], 'b': [3.0, 4.0]})
    assert_frame_equal(df1, df2, check_dtype=False)