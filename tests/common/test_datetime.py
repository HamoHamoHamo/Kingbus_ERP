import pytest
from common.datetime import count_range_hits


class TestCases:
    # 4 ~ 10 일 때, 17 ~ 21일 때 카운트
    def test_count_range_hits(self):
        
        # count 0
        assert 0 == len(count_range_hits("2024-10-01 02:00", "2024-10-01 03:59"))
        assert 0 == len(count_range_hits("2024-10-01 10:01", "2024-10-01 16:59"))
        assert 0 == len(count_range_hits("2024-10-01 21:01", "2024-10-01 23:59"))

        # count 1
        assert 1 == len(count_range_hits("2024-10-01 02:00", "2024-10-01 04:00"))
        assert 1 == len(count_range_hits("2024-10-01 02:00", "2024-10-01 12:00"))
        assert 1 == len(count_range_hits("2024-10-01 02:00", "2024-10-01 16:59"))
        assert 1 == len(count_range_hits("2024-10-01 04:00", "2024-10-01 10:00"))
        assert 1 == len(count_range_hits("2024-10-01 05:00", "2024-10-01 12:00"))

        assert 1 == len(count_range_hits("2024-10-01 16:00", "2024-10-01 17:00"))
        assert 1 == len(count_range_hits("2024-10-01 16:00", "2024-10-01 22:00"))
        assert 1 == len(count_range_hits("2024-10-01 16:00", "2024-10-01 23:59"))
        assert 1 == len(count_range_hits("2024-10-01 17:00", "2024-10-01 21:00"))
        assert 1 == len(count_range_hits("2024-10-01 18:00", "2024-10-01 23:00"))

        # count 2
        assert 2 == len(count_range_hits("2024-10-01 03:00", "2024-10-01 17:00"))
        assert 2 == len(count_range_hits("2024-10-01 04:00", "2024-10-01 18:00"))
        assert 2 == len(count_range_hits("2024-10-01 05:00", "2024-10-01 22:59"))
        
        # count 3
        assert 3 == len(count_range_hits("2024-10-01 03:00", "2024-10-02 05:00"))
        assert 3 == len(count_range_hits("2024-10-01 17:00", "2024-10-02 18:00"))
        
        # count 4
        assert 4 == len(count_range_hits("2024-10-01 04:00", "2024-10-02 17:00"))
                

    
