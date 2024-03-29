import typing
from dataclasses import asdict, fields
from ui.menu import Menu
from my_dataclasses import Sport, Member, Plays, Group


class UI(object):
    """Class for quick UI shortcuts."""

    def get_member(self):
        print("Enter member info:")
        name = input("Name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        year_of_birth = self.get_int("Year of birth")
        new_member = Member(name, phone, email, year_of_birth)
        print("New member:", new_member)
        return new_member

    def update_member(self, old_member):
        print(f"Update member {old_member}:")
        name = input(f"Old name: {old_member.name}\nNew name: ")
        phone = input(f"Old phone: {old_member.phone}\nNew phone: ")
        email = input(f"Old email: {old_member.email}\nNew email: ")
        print(f"Old year of birth: {old_member.year_of_birth}")
        year_of_birth = self.get_int("New year of birth")
        new_member = Member(name, phone, email, year_of_birth)
        print("Updated member:", new_member, "\n")
        return new_member

    def new_sport(self, message="Create new sport:"):
        print(message)
        name = input("Name: ")
        new_sport = Sport(name)
        print("New sport:", new_sport, "\n")
        return new_sport

    def get_int(self, fieldname):
        field = None
        while field is None:
            try:
                field = int(input(fieldname + ": "))
            except ValueError:
                print(fieldname, "should be a whole number.")
        return field

    def new_group(self, sport):
        print("Enter group info:")
        age_from = self.get_int("Age from")
        age_to = self.get_int("Age to")
        max_size = self.get_int("Max size")
        new_group = Group(sport, age_from, age_to, max_size)
        print("New group", new_group, "\n")
        return new_group

    def choose(self, items: typing.Iterable, message: str = None):
        """Let user pick from list, returns picked item."""
        options = {str(item): item for item in items}
        message = "Choose an item:\n" if message is None else message
        menu = Menu(message, options)
        item_str, item = menu.get_input()
        return item

    def view_info(self, dataclass_instance):
        print(self.get_info(dataclass_instance))

    def get_info(self, dataclass_instance) -> str:
        """Get a string with detailed info about this dataclass instance."""
        item = asdict(dataclass_instance)
        class_type = type(dataclass_instance)
        string = f"Detailed info for this {class_type.__name__}:\n"
        for key, value in item.items():
            key = str(key).replace("_", " ").capitalize()
            string += "\n" + key + ": " + str(value)
        return string + "\n"

    def search(self, dataclass) -> dict:
        """Start a search for specific item, returns search parameters."""
        print(f"Search {dataclass.__name__} repository")
        print("Leave a field blank to not search with it")
        parameters = dict()
        for field in fields(dataclass):
            try:
                parameters[field.name] = field.type(input(field.name + ": "))
            except ValueError:
                parameters[field.name] = None
        print()
        return parameters

    def search_result_choice(self, results, next, back, order_field=None,
                             message=""):
        """Get user choice from search results."""
        options = [("Back", back)] + [(str(item), item) for item in results]
        menu_msg = ""
        if order_field == "sports":
            menu_msg = "Ordered based on the first alphabetically ordered "
            menu_msg += "sport users are registered for. \nUsers not "
            menu_msg += "registered for any sports are hidden.\n"
        if message:
            menu_msg += message
        else:
            menu_msg += "Search results:"
        menu = Menu(menu_msg, options)
        string, item = menu.get_input()
        if string == "Back":
            return None, item
        return item, next

    def operation_result(self, result_message, undo_op, continue_op):
        result_menu = Menu("Operation result:\n" + result_message,
                           {"Undo": undo_op, "Continue": continue_op})
        key, operation = result_menu.get_input()
        return operation
