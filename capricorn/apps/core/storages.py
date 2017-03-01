from storages.backends.s3boto import S3BotoStorage

def filename_extractor(filename):
    _filename, _ext = filename.split('.')
    _ext = _ext.lower()

    return _filename, _ext

StaticRootS3BotoStorage = lambda: S3BotoStorage(location='assets/static', acl='public-read', querystring_auth=False)
MediaRootS3BotoStorage = lambda: S3BotoStorage(location='assets/media', acl='public-read', querystring_auth=False)
