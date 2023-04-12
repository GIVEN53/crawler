def mapping_new_info(crawl_result: dict):
    message = '---------------------------------------\n'
    for key, value in crawl_result.items():
        if key == 'number':
            continue
        message += f'{key}: {value}\n'
    message += '---------------------------------------'
    return message