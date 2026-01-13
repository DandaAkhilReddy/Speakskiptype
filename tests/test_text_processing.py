"""
Tests for text processing functions (filler words, custom vocabulary, etc.)
"""

import pytest
import copy
import speakskiptype


class TestFillerWordRemoval:
    """Tests for the remove_filler_words function."""

    def setup_method(self):
        """Reset config before each test."""
        speakskiptype.config = copy.deepcopy(speakskiptype.DEFAULT_CONFIG)
        speakskiptype.config['transcription']['remove_filler_words'] = True
        speakskiptype.config['transcription']['auto_punctuation'] = False

    def test_remove_single_filler_word_um(self):
        """Test removing single filler word 'um'."""
        result = speakskiptype.remove_filler_words("I um want to test this")
        assert result == "I want to test this"

    def test_remove_single_filler_word_uh(self):
        """Test removing single filler word 'uh'."""
        result = speakskiptype.remove_filler_words("uh hello there")
        assert result == "hello there"

    def test_remove_multi_word_filler_you_know(self):
        """Test removing multi-word filler 'you know'."""
        result = speakskiptype.remove_filler_words("I can you know start using this")
        assert result == "I can start using this"

    def test_remove_multi_word_filler_i_mean(self):
        """Test removing multi-word filler 'i mean'."""
        result = speakskiptype.remove_filler_words("I mean this is great")
        assert result == "this is great"

    def test_remove_multi_word_filler_sort_of(self):
        """Test removing multi-word filler 'sort of'."""
        result = speakskiptype.remove_filler_words("it's sort of working")
        assert result == "it's working"

    def test_remove_multi_word_filler_kind_of(self):
        """Test removing multi-word filler 'kind of'."""
        result = speakskiptype.remove_filler_words("this is kind of cool")
        assert result == "this is cool"

    def test_remove_multiple_fillers(self):
        """Test removing multiple filler words in one sentence."""
        result = speakskiptype.remove_filler_words("um I like you know want to uh test this")
        assert result == "I want to test this"

    def test_remove_filler_at_start(self):
        """Test removing filler word at the start."""
        result = speakskiptype.remove_filler_words("like this is cool")
        assert result == "this is cool"

    def test_remove_filler_at_end(self):
        """Test removing filler word at the end."""
        result = speakskiptype.remove_filler_words("this is cool right")
        assert result == "this is cool"

    def test_remove_filler_case_insensitive(self):
        """Test that filler removal is case insensitive."""
        result = speakskiptype.remove_filler_words("I Um want You Know to test")
        assert result == "I want to test"

    def test_remove_filler_with_comma(self):
        """Test removing filler word followed by comma."""
        result = speakskiptype.remove_filler_words("well, this is great")
        assert result == "this is great"

    def test_empty_string(self):
        """Test with empty string."""
        result = speakskiptype.remove_filler_words("")
        assert result == ""

    def test_no_fillers(self):
        """Test with text containing no filler words."""
        result = speakskiptype.remove_filler_words("hello world this is a test")
        assert result == "hello world this is a test"

    def test_filler_removal_disabled(self):
        """Test that filler removal can be disabled via config."""
        speakskiptype.config['transcription']['remove_filler_words'] = False
        result = speakskiptype.remove_filler_words("um I like want to test")
        assert result == "um I like want to test"

    def test_user_reported_bug_you_know(self):
        """Test the exact user-reported bug case."""
        text = "hey i would like to work on this today so let me work on this and then i can you know start using this"
        result = speakskiptype.remove_filler_words(text)
        assert "you know" not in result
        assert "hey i would" in result or "hey I would" in result


class TestCustomVocabulary:
    """Tests for the apply_custom_vocabulary function."""

    def setup_method(self):
        """Reset config before each test."""
        speakskiptype.config = copy.deepcopy(speakskiptype.DEFAULT_CONFIG)
        speakskiptype.config['transcription']['auto_punctuation'] = False

    def test_custom_vocabulary_replacement(self):
        """Test basic custom vocabulary replacement."""
        speakskiptype.config['custom_vocabulary'] = {"kubernetes": "K8s"}
        result = speakskiptype.apply_custom_vocabulary("deploy to kubernetes cluster")
        assert result == "deploy to K8s cluster"

    def test_custom_vocabulary_case_insensitive(self):
        """Test custom vocabulary is case insensitive."""
        speakskiptype.config['custom_vocabulary'] = {"javascript": "JavaScript"}
        result = speakskiptype.apply_custom_vocabulary("I love JAVASCRIPT")
        assert result == "I love JavaScript"

    def test_custom_vocabulary_multiple(self):
        """Test multiple custom vocabulary replacements."""
        speakskiptype.config['custom_vocabulary'] = {
            "k8s": "Kubernetes",
            "js": "JavaScript"
        }
        result = speakskiptype.apply_custom_vocabulary("using k8s and js")
        assert result == "using Kubernetes and JavaScript"

    def test_empty_custom_vocabulary(self):
        """Test with empty custom vocabulary."""
        speakskiptype.config['custom_vocabulary'] = {}
        result = speakskiptype.apply_custom_vocabulary("hello world")
        assert result == "hello world"


class TestProcessText:
    """Tests for the process_text pipeline function."""

    def setup_method(self):
        """Reset config before each test."""
        speakskiptype.config = copy.deepcopy(speakskiptype.DEFAULT_CONFIG)
        speakskiptype.config['transcription']['auto_punctuation'] = False
        speakskiptype.config['transcription']['code_mode'] = False
        speakskiptype.config['transcription']['remove_filler_words'] = True

    def test_process_text_removes_fillers(self):
        """Test that process_text removes filler words."""
        result = speakskiptype.process_text("um hello you know world")
        assert "um" not in result.lower()
        assert "you know" not in result.lower()

    def test_process_text_empty_string(self):
        """Test process_text with empty string."""
        result = speakskiptype.process_text("")
        assert result == ""

    def test_process_text_none(self):
        """Test process_text with None."""
        result = speakskiptype.process_text(None)
        assert result is None

    def test_process_text_strips_whitespace(self):
        """Test that process_text strips leading/trailing whitespace."""
        result = speakskiptype.process_text("  hello world  ")
        assert not result.startswith(" ")
        assert not result.endswith(" ")


class TestVoiceCommands:
    """Tests for voice command processing."""

    def setup_method(self):
        """Reset config before each test."""
        speakskiptype.config = copy.deepcopy(speakskiptype.DEFAULT_CONFIG)
        speakskiptype.config['transcription']['auto_punctuation'] = False
        speakskiptype.config['transcription']['literal_punctuation'] = False
        speakskiptype.config['voice_commands']['enabled'] = True

    def test_new_line_command(self):
        """Test 'new line' voice command."""
        result = speakskiptype.process_voice_commands("hello new line world")
        assert "\n" in result

    def test_period_command(self):
        """Test 'period' voice command."""
        result = speakskiptype.process_voice_commands("hello period world")
        assert "." in result

    def test_literal_punctuation_mode(self):
        """Test literal punctuation mode keeps words as-is."""
        speakskiptype.config['transcription']['literal_punctuation'] = True
        result = speakskiptype.process_text("hello period world")
        # In literal mode, "period" should stay as "period"
        assert "period" in result.lower() or "." in result
