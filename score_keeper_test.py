from score_keeper import ScoreKeeper


def test_constructor():
    score_keeper = ScoreKeeper('lw', "test_file.txt")
    assert score_keeper.scores == {"Emilia": 5,
                                   "Iago": 2,
                                   "Desdemona": 2,
                                   "Cassio": 1}
