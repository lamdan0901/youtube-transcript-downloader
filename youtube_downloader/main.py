import sys
import os
import argparse
from youtube_transcript_api import YouTubeTranscriptApi

def list_available_languages(video_id):
    """List all available transcript languages for a video"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        print(f"Available languages for video {video_id}:")
        for transcript in transcript_list:
            print(f"  - {transcript.language} ({transcript.language_code})")
            if transcript.is_generated:
                print("    [Automatically generated]")
            else:
                print("    [Manually created]")

            # Show translation languages if available
            if transcript.is_translatable:
                print("    Available translations:")
                try:
                    for lang in transcript.translation_languages:
                        # Handle different object structures
                        if hasattr(lang, 'language') and hasattr(lang, 'language_code'):
                            # Direct attribute access
                            print(f"      - {lang.language} ({lang.language_code})")
                        elif isinstance(lang, dict) and 'language' in lang and 'language_code' in lang:
                            # Dictionary access
                            print(f"      - {lang['language']} ({lang['language_code']})")
                        else:
                            # Just print the language object as string
                            print(f"      - {str(lang)}")
                except Exception as translation_error:
                    print(f"    Error listing translations: {translation_error}")
        return True
    except Exception as e:
        print(f"Error listing languages: {e}")
        return False

def save_transcript_to_file(transcript, video_id, language, output_file=None):
    """Save transcript to a file"""
    if output_file is None:
        output_file = f"{video_id}_{language}.txt"

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in transcript:
                # Handle both dictionary-style entries and FetchedTranscriptSnippet objects
                if hasattr(entry, 'text'):
                    # This is a FetchedTranscriptSnippet object
                    f.write(f"{entry.text}\n")
                elif isinstance(entry, dict) and 'text' in entry:
                    # This is a dictionary with a 'text' key
                    f.write(f"{entry['text']}\n")
                else:
                    # Try to convert to string as a fallback
                    f.write(f"{str(entry)}\n")
        print(f"Transcript saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving transcript to file: {e}")
        return False

def get_transcript(video_id, language, translate_to=None):
    """Get transcript in specified language, with optional translation"""
    actual_language = language  # Keep track of which language we actually got

    try:
        # If translation is requested, we need to get the transcript object first
        if translate_to:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try to find a transcript in the requested language
            try:
                transcript_obj = transcript_list.find_transcript([language])
                print(f"Found transcript in {language}")
            except Exception:
                # If not found, try English
                if language != 'en':
                    print(f"Could not find transcript in {language}, trying English...")
                    try:
                        transcript_obj = transcript_list.find_transcript(['en'])
                        actual_language = 'en'
                        print("Found transcript in English")
                    except Exception:
                        # If English not found, get any available transcript
                        print("Could not find English transcript, getting any available transcript...")
                        transcript_obj = next(iter(transcript_list))
                        actual_language = transcript_obj.language_code
                        print(f"Found transcript in {transcript_obj.language}")
                else:
                    # If English was requested and not found, get any available transcript
                    print("Could not find English transcript, getting any available transcript...")
                    transcript_obj = next(iter(transcript_list))
                    actual_language = transcript_obj.language_code
                    print(f"Found transcript in {transcript_obj.language}")

            # Now translate the transcript
            try:
                print(f"Translating from {actual_language} to {translate_to}...")
                # Check if the language code is valid for translation
                valid_translation = False
                try:
                    # Check if the requested language is in the available translation languages
                    for lang in transcript_obj.translation_languages:
                        # Handle different object structures
                        lang_code = None
                        if hasattr(lang, 'language_code'):
                            lang_code = lang.language_code
                        elif isinstance(lang, dict) and 'language_code' in lang:
                            lang_code = lang['language_code']

                        if lang_code == translate_to:
                            valid_translation = True
                            break
                except Exception:
                    # If we can't check, we'll just try the translation anyway
                    valid_translation = True

                if valid_translation:
                    translated_transcript = transcript_obj.translate(translate_to)
                    transcript_data = translated_transcript.fetch()
                    print(f"Successfully translated to {translate_to}")
                    return transcript_data, translate_to
                else:
                    print(f"Language code '{translate_to}' is not available for translation")
                    print("Returning original transcript instead")
                    return transcript_obj.fetch(), actual_language
            except Exception as e:
                print(f"Translation failed: {e}")
                print("Returning original transcript instead")
                return transcript_obj.fetch(), actual_language

        # If no translation requested, just get the transcript directly
        else:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
                print(f"Successfully retrieved transcript in language: {language}")
                return transcript, language
            except Exception as lang_error:
                # If specified language fails, try English as fallback
                if language != 'en':
                    print(f"Could not find transcript in language '{language}': {lang_error}")
                    print("Trying to fall back to English...")
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    print("Successfully retrieved English transcript")
                    return transcript, 'en'
                else:
                    # If English was requested and failed, try to get any available transcript
                    print(f"Could not find English transcript: {lang_error}")
                    print("Trying to get any available transcript...")
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    print("Successfully retrieved transcript")
                    return transcript, 'unknown'
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Download YouTube video subtitles')
    parser.add_argument('video_id', help='YouTube video ID')
    parser.add_argument('--language', '-l', default='en', help='Language code (default: en)')
    parser.add_argument('--translate', '-t', help='Translate to this language code')
    parser.add_argument('--list', '-ls', action='store_true', help='List available languages')
    parser.add_argument('--output', '-o', help='Output file (default: video_id_language.txt)')
    args = parser.parse_args()

    video_id = args.video_id
    language = args.language
    translate_to = args.translate
    output_file = args.output

    # If list flag is provided, show available languages and exit
    if args.list:
        if list_available_languages(video_id):
            sys.exit(0)
        else:
            sys.exit(1)

    try:
        # Get transcript with optional translation
        transcript, actual_language = get_transcript(video_id, language, translate_to)

        # If translation was requested, update the actual language
        if translate_to and actual_language == translate_to:
            actual_language = translate_to

        # Save to file if output is specified
        if output_file:
            save_transcript_to_file(transcript, video_id, actual_language, output_file)
        else:
            # Print the transcript to console
            for entry in transcript:
                # Handle both dictionary-style entries and FetchedTranscriptSnippet objects
                if hasattr(entry, 'text'):
                    # This is a FetchedTranscriptSnippet object
                    print(f"{entry.text}")
                elif isinstance(entry, dict) and 'text' in entry:
                    # This is a dictionary with a 'text' key
                    print(f"{entry['text']}")
                else:
                    # Try to convert to string as a fallback
                    print(f"{str(entry)}")
    except Exception as e:
        print(f"Error: {e}")
        print("Try using --list to see available languages for this video")
        sys.exit(1)

if __name__ == "__main__":
    main()

