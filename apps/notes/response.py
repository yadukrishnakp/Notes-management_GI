


class ResponseInfo(object):
    def __init__(self, user=None, **args):
        self.response = {
            "status": args.get('status', True),
            "status_code": args.get('status_code', 200),
            "message": args.get('message', ''),
            "data": args.get('data', {}),
            "errors": args.get('errors', {}),
        }
