class Paginator:
    def __init__(self, items, page_size):
        self.items = items
        self.page_size = page_size
        self.total_items = len(items)
        self.total_pages = (self.total_items + page_size - 1) // page_size  # Округление вверх

    def get_page(self, page_number):
        if page_number < 1 or page_number > self.total_pages:
            raise ValueError("Номер страницы вне диапазона.")
        
        start_index = (page_number - 1) * self.page_size
        end_index = start_index + self.page_size
        return self.items[start_index:end_index]

    def get_navigation(self, current_page):
        return {
            "has_previous": current_page > 1,
            "has_next": current_page < self.total_pages,
            "previous_page": current_page - 1 if current_page > 1 else None,
            "next_page": current_page + 1 if current_page < self.total_pages else None,
        }
