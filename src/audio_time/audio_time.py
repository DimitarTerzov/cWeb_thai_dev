import re
import io
import datetime

def build_sync_times(filepath):
    sync_t = {}

    last_sync = u""

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1

            line = line.rstrip("\r\n")
            if re.match(ur"<Sync time=\"[\s\d\.]+\"/>", line, re.UNICODE):
                last_sync = line

            sync_t[ln] = last_sync.encode('utf')

    return sync_t


def build_audio_times(sync_times):
    audio_times = {}

    for key, value in sync_times.iteritems():
        if value:
            audio_times[key] = get_audio_time(value)
        else:
            audio_times[key] = value

    return audio_times


def get_audio_time(sync_time):
    time = re.search(r'\d+', sync_time).group()
    return str(datetime.timedelta(seconds=int(time)))


if __name__ == '__main__':
    sync_times = build_sync_times('../files/AsiaWaveNews_01_sample_chawankorn.trs')
    audio_times = build_audio_times(sync_times)
    for key in sorted(audio_times.keys()):
        print(key, audio_times[key])
