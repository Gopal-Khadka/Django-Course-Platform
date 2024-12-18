def get_cloudinary_image_object(
    instance, field_name="thumbnail", as_html=False, width=200
):
    if not hasattr(instance, field_name):
        return ""
    image_obj = getattr(instance, field_name)
    if not image_obj:
        return ""
    image_options = {"width": width}
    if as_html:
        # refer to cloudinary docs
        return image_obj.image(**image_options)
    url = image_obj.build_url(**image_options)
    return url


def get_cloudinary_video_object(
    instance,
    field_name="video",
    as_html=False,
    width=None,
    sign_url=False, # for private videos
    fetch_format="auto",
    quality="auto",
):
    if not hasattr(instance, field_name):
        return ""
    video_obj = getattr(instance, field_name)
    if not video_obj:
        return ""
    video_options = {
        "sign_url": sign_url,
        "fetch_format": fetch_format,
        quality: quality,
    }
    if width:
        video_options["width"] = width
    if as_html:
        # refer to cloudinary docs
        return video_obj.video(**video_options)
    url = video_obj.build_url(**video_options)
    return url
