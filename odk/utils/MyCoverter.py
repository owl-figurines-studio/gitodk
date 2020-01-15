from werkzeug.routing import BaseConverter


class MyCoverter(BaseConverter):
    def __init__(self,url_map,*args):
        super().__init__(url_map)
        # print("&&&&&&&&&&&&&&&&&&")
        # print(args[0])
        self.regex = args[0]
    # regex = r'\d{5}'