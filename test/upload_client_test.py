from unittest import mock, TestCase

from test import create_bynder_client


class UploadClientTest(TestCase):
    """ Test the Upload client.
    """

    def setUp(self):
        self.bynder_client = create_bynder_client()

        self.upload_client = self.bynder_client.upload_client
        self.upload_client.session.get = mock.MagicMock()
        self.upload_client.session.post = mock.MagicMock()

    def tearDown(self):
        self.bynder_client = None
        self.asset_bank_client = None

    def test_prepare(self):
        """ Test if when we call _prepare it will use the correct params
        for the
        requests.
        """
        self.upload_client._prepare()
        self.upload_client.session.post.assert_called_with(
            '/v7/file_cmds/upload/prepare', is_fs_endpoint=True
        )

    def test_upload_chunks(self):
        """ Test if when we call _upload_chunks it will use the correct params
        for the requests. Also test the chunks_count returned.
        """
        file_path = 'resources/image.png'
        file_id = 1111
        chunks_count, file_size = \
            self.upload_client._upload_chunks(
                file_path, file_id)
        self.assertEqual(chunks_count, 1)
        self.upload_client.session.post.assert_called()

    def test_finalise_file(self):
        """ Test if when we call _finalise_file it will use the correct params
        for the requests.
        """
        file_id = 1111
        file_name = 'image.png'
        file_size = 4000
        chunks_count = 1
        self.upload_client._finalise_file(file_id, file_name, file_size,
                                          chunks_count)
        self.upload_client.session.post.assert_called_with(
            '/v7/file_cmds/upload/{}/finalise'.format(file_id),
            need_response_json=False,
            is_fs_endpoint=True,
            data={
                'fileName': file_name,
                'fileSize': file_size,
                'chunksCount': chunks_count
            })

    def test_save_media(self):
        """ Test if when we call _save_media it will use the correct params
        for the requests. Test both cases when the file_id is passed and
        when not passed.
        """
        file_id = 1111
        data = {'brandId': "89898989898-89898989-8989"}
        self.upload_client._save_media(file_id, data)
        self.upload_client.session.post.assert_called_with(
            '/v4/media/{}/save/'.format(file_id), data=data)
        self.upload_client._save_media(None, data)
        self.upload_client.session.post.assert_called_with(
            '/v4/media/save', data=data)