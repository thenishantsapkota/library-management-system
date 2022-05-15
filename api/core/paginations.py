import typing as t


def paginate(base_url: t.Optional[str], data, page_num: int = 1, page_size: int = 5):
    start = (page_num - 1) * page_size
    end = start + page_size

    response = {
        "pagination": {
            "total": len(data),
            "count": len(data[start:end]),
        },
        "data": data[start:end],
    }

    if end >= len(data):
        response["pagination"]["next"] = None
        if page_num > 1:
            response["pagination"][
                "previous"
            ] = f"/{base_url}/?page_num={page_num - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"][
                "previous"
            ] = f"/{base_url}?page_num={page_num - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None
        response["pagination"][
            "next"
        ] = f"/{base_url}?page_num={page_num +1}&page_size={page_size}"

    return response
