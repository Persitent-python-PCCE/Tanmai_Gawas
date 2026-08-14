class QuerySpec:
    def __init__(self, filters=None, search=None, sort_by=None, sort_dir="ASC", page=1, page_size=20):
        self.filters = filters or {}
        self.search = search
        self.sort_by = sort_by
        self.sort_dir = sort_dir.upper() if sort_dir and sort_dir.upper() in ("ASC", "DESC") else "ASC"
        self.page = max(page, 1)
        self.page_size = min(max(page_size, 1), 100)

    @property
    def offset(self):
        return (self.page - 1) * self.page_size


class PageResult:
    def __init__(self, items, total, page, page_size):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = max((total + page_size - 1) // page_size, 1)