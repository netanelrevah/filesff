from dataclasses import dataclass
from io import BytesIO
from typing import BinaryIO, cast

from boto3 import Session, resource
from mypy_boto3_s3.service_resource import Object

from filesff.core.files import AccessibleFileHandle, FilePointer


@dataclass
class S3ObjectPointer(FilePointer):
    s3_object: Object

    @classmethod
    def from_s3_url(cls, s3_url, session: Session | None = None, **resource_kwargs) -> "S3ObjectPointer":
        s3_resource = session.resource("s3", **resource_kwargs) if session else resource("s3", **resource_kwargs)
        bucket_name, key = s3_url.replace("s3://").split("/", 1)
        return cls(s3_resource.Object(bucket_name, key))


class S3BinaryWriter(BytesIO):
    def __init__(self, s3_object: Object):
        super().__init__()
        self.s3_object = s3_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.s3_object.upload_fileobj(Fileobj=self)


@dataclass
class S3ObjectFileHandle(AccessibleFileHandle):
    pointer: S3ObjectPointer

    def create_binary_reader(self) -> BinaryIO:
        return cast(BinaryIO, self.pointer.s3_object.get()["Body"])

    def create_binary_writer(self) -> BinaryIO:
        return S3BinaryWriter(self.pointer.s3_object)
