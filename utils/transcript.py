import re

class TranscriptParser:
    def __init__(self, transcript: str):
        self.transcript = transcript
    
    def parse_transcript_to_map(self) -> dict[tuple[int, int | None], str]:
        timestamp_pattern = re.compile(r"^\d{1,2}:\d{2}$")
        lines = self.transcript.strip().splitlines()

        entries = []
        for i, line in enumerate(lines):
            if timestamp_pattern.match(line.strip()):
                timestamp = line.strip()
                if i + 1 < len(lines):
                    text = lines[i + 1].strip()
                    entries.append((timestamp, text))

        interval_map = {}
        for i in range(len(entries)):
            start_ts = entries[i][0]
            start_sec = TranscriptParser.timestamp_to_seconds(start_ts)
            text = entries[i][1]

            if i + 1 < len(entries):
                end_sec = TranscriptParser.timestamp_to_seconds(entries[i + 1][0])
            else:
                end_sec = None

            interval_map[(start_sec, end_sec)] = text

        return interval_map

    def timestamp_to_seconds(self, timestamp: str) -> int:
        parts = list(map(int, timestamp.split(':')))
        return parts[0] * 60 + parts[1]

    def get_text_from_map(self, query_timestamp: str) -> str | None:
        query_sec = self.timestamp_to_seconds(query_timestamp)

        for (start, end), text in self.interval_map.items():
            if end is None:
                if query_sec >= start:
                    return text
            else:
                if start <= query_sec < end:
                    return text
        return None

