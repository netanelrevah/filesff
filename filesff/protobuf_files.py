from google.protobuf.json_format import MessageToJson, Parse

from filesff.formatted_files import FileAccessor


class ProtoJsonFile(FileAccessor):
    def load(self, message):
        return Parse(self.handle.create_unicode_reader().read(), message=message)

    def dump(self, message):
        return self.handle.create_unicode_writer().write(MessageToJson(message))
