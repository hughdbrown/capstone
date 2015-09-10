from urlparse import urlparse


def is_website_collateral(long_url):
    """
    Boolean method for whether a URL is a skippable web asset
    """
    p = urlparse(long_url)
    collateral = (
        '.jpg', '.jpeg', '.png', '.gif',
        '.tif', '.tiff',
        '.jif', '.jfif',
        '.jp2', '.jpx', '.j2k', '.j2c',
        '.fpx',
        '.pcd',
        '.pdf',
        '.css', '.js',
    )
    streaming_data = (
        '.3gp', '.3g2',
        '.nsv', '.m4v',
        '.mpg', '.mpeg', '.m2v',
        '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv',
        '.asf',
        '.rm',
        '.wmv',
        '.mov', '.qt',
        '.avi',
        '.ogv', '.ogg',
        '.flv',
        '.mkv',
        '.webm',
        '.vob',
    )
    archive = (
        '.zip', '.gz', '.tar', '.apk', '.iso', '.rar',
        '.cpio', '.shar', '.bz2', '.lz', '.xz', '.7z', '.s7z',
        '.cab', '.dmg',
        '.jar', '.war',
        '.zoo',
        '.pak',
        '.tgz', '.lzma',
    )
    return (
        'stream' in long_url or
        any(p.path.endswith(x) for x in (collateral, streaming_data, archive))
    )
