def getHeader(request_id, message, status, error_list):
    header = {}
    header['request_id'] = request_id
    header['message'] = message
    header['status'] = status
    header['error'] = error_list
    return header