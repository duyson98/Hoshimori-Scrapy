def get_raw_image(url):

    splitted = url.split('?')
    if len(splitted) == 2:
        return "?".join(["/".join(splitted[0].split("/")[0:-2])] + [splitted[1]])
    elif len(splitted) == 1:
        return url
    else:
        raise ValueError('Not a resized Vignette image url: %s' %url)