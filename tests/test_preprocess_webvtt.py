from unittest.mock import patch, mock_open, MagicMock
from preprocess_webvtt import process_vtt, main
import pytest


class TestFragments:
    @pytest.fixture
    def log(self):
        return MagicMock()

    @patch("preprocess_webvtt.webvtt.read")
    @patch("builtins.open", new_callable=mock_open)
    def test_join_lines(self, mock_file, mock_webvtt_read, log):
        caption = MagicMock()
        caption.start = "00:00:08.459"
        caption.end = "00:00:12.459"
        caption.text = "She had that level\nof love and care."
        caption.raw_text = "She had that level\nof love and care."
        mock_webvtt_read.return_value = [caption]

        process_vtt("testfile", log)

        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        expected = (
            "⎡⎡00:00:08.459 --> 00:00:12.459⎦⎦ She had that level of love and care. \n"
        )

        assert written == expected

    @patch("preprocess_webvtt.webvtt.read")
    @patch("builtins.open", new_callable=mock_open)
    def test_simple_cue(self, mock_file, mock_webvtt_read, log):
        caption = MagicMock()
        caption.start = "00:00:16.125"
        caption.end = "00:00:20.542"
        caption.text = "I was in shock."
        caption.raw_text = "I was in shock."
        mock_webvtt_read.return_value = [caption]

        process_vtt("testfile", log)

        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        expected = "⎡⎡00:00:16.125 --> 00:00:20.542⎦⎦ I was in shock. \n"

        assert written == expected

    @patch("preprocess_webvtt.webvtt.read")
    @patch("builtins.open", new_callable=mock_open)
    def test_join_multiple_cues(self, mock_file, mock_webvtt_read, log):
        caption1 = MagicMock()
        caption1.start = "00:00:04.667"
        caption1.end = "00:00:06.667"
        caption1.text = "Does Alesia have time to do\nthe crew mess at the moment"
        caption1.raw_text = "Does Alesia have time to do\nthe crew mess at the moment"

        caption2 = MagicMock()
        caption2.start = "00:00:06.667"
        caption2.end = "00:00:08.459"
        caption2.text = "because she's on\nthe hamster wheel."
        caption2.raw_text = "because she's on\nthe hamster wheel."

        mock_webvtt_read.return_value = [caption1, caption2]

        process_vtt("testfile", log)

        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        expected = (
            "⎡⎡00:00:04.667 --> 00:00:06.667⎦⎦ Does Alesia have time to do the crew mess at the moment "
            "⎡⎡00:00:06.667 --> 00:00:08.459⎦⎦ because she's on the hamster wheel. \n"
        )

        assert written == expected

    @patch("preprocess_webvtt.webvtt.read")
    @patch("builtins.open", new_callable=mock_open)
    def test_multiple_speakers(self, mock_file, mock_webvtt_read, log):
        caption = MagicMock()
        caption.start = "00:00:23.042"
        caption.end = "00:00:24.918"
        caption.text = "-A hostel in New York?\n-Yeah."
        caption.raw_text = "-A hostel in New York?\n-Yeah."
        caption.lines = ["-A hostel in New York?", "-Yeah."]
        mock_webvtt_read.return_value = [caption]

        process_vtt("testfile", log)

        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        expected = (
            "⎡⎡00:00:23.042 --> 00:00:24.918⎦⎦ "
            "⎡⎡Speaker ⎦⎦ A hostel in New York?\n"
            "⎡⎡Speaker ⎦⎦ Yeah. \n"
        )
        print(written)
        assert written == expected

    @patch("preprocess_webvtt.webvtt.read")
    @patch("builtins.open", new_callable=mock_open)
    def test_multiple_speakers_with_name(self, mock_file, mock_webvtt_read, log):
        caption = MagicMock()
        caption.start = "00:02:18.125"
        caption.end = "00:02:21.292"
        caption.text = "-Hi, everyone. How are you?\n-TANISHA: Cold."
        caption.raw_text = "-Hi, everyone. How are you?\n-TANISHA: Cold."
        caption.lines = ["-Hi, everyone. How are you?", "-TANISHA: Cold."]
        mock_webvtt_read.return_value = [caption]

        process_vtt("testfile", log)

        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        expected = (
            "⎡⎡00:02:18.125 --> 00:02:21.292⎦⎦ "
            "⎡⎡Speaker ⎦⎦ Hi, everyone. How are you?\n"
            "⎡⎡Speaker TANISHA:⎦⎦ Cold. \n"
        )
        print(written)
        assert written == expected

    @patch("preprocess_webvtt.webvtt.read")
    @patch("builtins.open", new_callable=mock_open)
    def test_named_speaker_no_dash(self, mock_file, mock_webvtt_read, log):
        caption = MagicMock()
        caption.start = "00:00:00.167"
        caption.end = "00:00:03.792"
        caption.text = 'BANANAS: Previously on\n"House of Villains"...'
        caption.raw_text = 'BANANAS: Previously on\n"House of Villains"...'
        # Simulate lines as they would be split by webvtt.models.Caption
        caption.lines = ["BANANAS: Previously on", '"House of Villains"...']
        mock_webvtt_read.return_value = [caption]

        process_vtt("testfile", log)

        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        expected = (
            "⎡⎡00:00:00.167 --> 00:00:03.792⎦⎦ "
            '⎡⎡Speaker BANANAS:⎦⎦ Previously on "House of Villains"... \n'
        )
        print(written)
        assert written == expected

    @patch("preprocess_webvtt.webvtt.read")
    @patch("builtins.open", new_callable=mock_open)
    def test_multiple_speakers_and_sounds(self, mock_file, mock_webvtt_read, log):
        # First caption
        caption1 = MagicMock()
        caption1.start = "00:00:55.125"
        caption1.end = "00:00:57.083"
        caption1.text = "-You guys' fashion sucks.\n-[buzzer]"
        caption1.raw_text = "-You guys' fashion sucks.\n-[buzzer]"
        caption1.lines = ["-You guys' fashion sucks.", "-[buzzer]"]

        # Second caption
        caption2 = MagicMock()
        caption2.start = "00:00:57.083"
        caption2.end = "00:00:59.792"
        caption2.text = "-[cackling]\n-Whoo!"
        caption2.raw_text = "-[cackling]\n-Whoo!"
        caption2.lines = ["-[cackling]", "-Whoo!"]

        mock_webvtt_read.return_value = [caption1, caption2]

        process_vtt("testfile", log)

        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        expected = (
            "⎡⎡00:00:55.125 --> 00:00:57.083⎦⎦ ⎡⎡Speaker ⎦⎦ You guys' fashion sucks.\n"
            "⎡⎡Speaker ⎦⎦ [buzzer] \n"
            "⎡⎡00:00:57.083 --> 00:00:59.792⎦⎦ ⎡⎡Speaker ⎦⎦ [cackling]\n"
            "⎡⎡Speaker ⎦⎦ Whoo! \n"
        )
        assert written == expected


class TestMain:
    @patch("preprocess_webvtt.helpers.logging.create_log")
    @patch("preprocess_webvtt.process_vtt")
    @patch("preprocess_webvtt.glob.glob")
    @patch("preprocess_webvtt.os.path.isdir")
    @patch("preprocess_webvtt.os.path.isfile")
    @patch("preprocess_webvtt.argparse.ArgumentParser.parse_args")
    def test_main_single_file(
        self,
        mock_parse_args,
        mock_isfile,
        mock_isdir,
        mock_glob,
        mock_process_vtt,
        mock_create_log,
    ):
        mock_logger = MagicMock()
        mock_create_log.return_value = mock_logger
        # Simulate single file
        mock_parse_args.return_value = MagicMock(path="file.webvtt")
        mock_isfile.return_value = True
        mock_isdir.return_value = False
        main()
        mock_process_vtt.assert_called_once_with("file.webvtt", mock_logger)
        mock_logger.info.assert_any_call("Starting preprocessing", path="file.webvtt")

    @patch("preprocess_webvtt.helpers.logging.create_log")
    @patch("preprocess_webvtt.process_vtt")
    @patch("preprocess_webvtt.glob.glob")
    @patch("preprocess_webvtt.os.path.isdir")
    @patch("preprocess_webvtt.os.path.isfile")
    @patch("preprocess_webvtt.argparse.ArgumentParser.parse_args")
    def test_main_directory(
        self,
        mock_parse_args,
        mock_isfile,
        mock_isdir,
        mock_glob,
        mock_process_vtt,
        mock_create_log,
    ):
        mock_logger = MagicMock()
        mock_create_log.return_value = mock_logger
        # Simulate directory with files
        mock_parse_args.return_value = MagicMock(path="dir")
        mock_isfile.return_value = False
        mock_isdir.return_value = True

        mock_glob.return_value = ["dir/a.webvtt", "dir/b.webvtt"]

        main()
        mock_process_vtt.assert_any_call("dir/a.webvtt", mock_logger)
        mock_process_vtt.assert_any_call("dir/b.webvtt", mock_logger)
        assert mock_process_vtt.call_count == 2
        mock_logger.info.assert_any_call("Starting preprocessing", path="dir")

    @patch("preprocess_webvtt.helpers.logging.create_log")
    @patch("preprocess_webvtt.argparse.ArgumentParser.parse_args")
    @patch("preprocess_webvtt.os.path.isfile")
    @patch("preprocess_webvtt.os.path.isdir")
    def test_main_invalid_path(
        self, mock_isdir, mock_isfile, mock_parse_args, mock_create_log
    ):
        mock_logger = MagicMock()
        mock_create_log.return_value = mock_logger
        mock_parse_args.return_value = MagicMock(path="invalid")
        mock_isfile.return_value = False
        mock_isdir.return_value = False

        with pytest.raises(Exception) as excinfo:
            main()
        assert "Path invalid is not valid." in str(excinfo.value)
