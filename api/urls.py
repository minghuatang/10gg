apps = [
]

urls = [
    (r'/alert', 'api.AlertHandler'),
    (r'/log/pull', 'api.LogPullHandler'),
    (r'/log/tips', 'api.LogTipsHandler'),
    (r'/log', 'api.LogFilterHandler'),
]
