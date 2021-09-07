class URLConstructor:

    def __init__(self, url):
        self.url_base = url.split("?")[0]
        self.url_object = self.init_url_object(url)

    def init_url_object(self, url):

        second_half = url.split("?")[1]

        url_object = {}

        for parameter in second_half.split("&"):
            
            param_array = parameter.split("=")

            if len(param_array) == 1:
                url_object[param_array[0]] = ""
            else:
                url_object[param_array[0]] = param_array[1]

        return url_object

    def get_url(self):

        full_url = self.url_base + "?"

        for key in self.url_object:
            full_url += "&"

            full_url += (key + "=" + self.url_object[key])

        return full_url

    def set_param(self, param_value_dict):

        for key in param_value_dict:
            try:
                self.url_object[key] = param_value_dict[key]
            except KeyError:
                print("wrong key: " + key)

        return self.get_url()

url_constructor = URLConstructor
