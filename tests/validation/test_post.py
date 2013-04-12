from popolo.post import PopoloPost


def test_invalid_post_entry():
    """ Test to make sure we reject invalid posts """
    post = PopoloPost("guid", "Chef, etc, etc", "some-hex-string", "Chef")
    post.validate()
    post['label'] = None

    try:
        assert "garbage string" == post.validate()
    except ValueError:
        pass
